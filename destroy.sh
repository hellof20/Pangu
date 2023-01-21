#!/bin/bash
echo "Begin to use $deploy_type to Destroy"

echo '{
    "client_id": "'$client_id'",
    "client_secret": "'$client_secret'",
    "refresh_token": "'$refresh_token'",
    "scopes": "'$scopes'",    
    "type": "authorized_user"
}' > client_secret.json

echo "---------------------------------------------"
echo "Begin to clone deploy from $url"
git clone $url $solution_id > /dev/null 2>&1
echo "Clone finish"
cd $solution_id

version=$(echo $parameters | jq .version)
if [[ $version != '""' ]];then
    echo "Checkout to version: $version"
    git checkout $version
    echo "Checkout finish"
fi

cd $deploy_path
if [[ $deploy_type == "Terraform" ]]
then
    echo $parameters | jq -r 'to_entries[] | .key + "=\"" + .value +"\""' > ./pangu.tfvars
    mysql --host=$host --user=$user --password=$password --database="ads" -N --execute="select CONCAT(id,'=\"',default_value,'\"') from parameters where solution_id='$solution_id' and show_on_ui=0 ;" >> ./pangu.tfvars
    echo "-------------- parameters env ---------------"
    cat pangu.tfvars
    echo "-------------- parameters env ---------------"
    terraform init -backend-config="address=$consul_ip:8500" -backend-config="path=ads_dev/$DEPLOY_ID/terraform_state" -backend-config="scheme=http"
    terraform apply -destroy -auto-approve -var-file="pangu.tfvars" -no-color
    if [ $? -eq 0 ]; then
        mysql --host=$host --user=$user --password=$password --database="ads" --execute="update deploy set status='destroy_success' where id='$DEPLOY_ID';"
    else
        mysql --host=$host --user=$user --password=$password --database="ads" --execute="update deploy set status='destroy_failed' where id='$DEPLOY_ID';"
    fi
else
    echo $parameters | jq -r 'to_entries[] | "export " + .key + "=\"" + .value +"\""' > ./pangu.env
    mysql --host=$host --user=$user --password=$password --database="ads" -N --execute="select CONCAT('export ',id,'=\"',default_value,'\"') from parameters where solution_id='$solution_id' and show_on_ui=0 ;" >> ./pangu.env
    source ./pangu.env
    echo "---------------------------------------------"
    echo "Run the following command to deploy from your Cloud Shell:"
    cat pangu.env
    # echo "git clone $url $solution_id"
    # echo "cd $solution_id/$deploy_path"
    echo 'CLOUDSDK_AUTH_ACCESS_TOKEN=$(gcloud auth application-default print-access-token) bash destroy.sh'
    echo "---------------------------------------------"  
    bash destroy.sh
    if [ $? -eq 0 ]; then
        mysql --host=$host --user=$user --password=$password --database="ads" --execute="update deploy set status='destroy_success' where id='$DEPLOY_ID';"
    else
        mysql --host=$host --user=$user --password=$password --database="ads" --execute="update deploy set status='destroy_failed' where id='$DEPLOY_ID';"
    fi    
fi