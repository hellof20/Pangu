#!/bin/bash

echo '{
    "client_id": "'$client_id'",
    "client_secret": "'$client_secret'",
    "refresh_token": "'$refresh_token'",
    "scopes": "'$scopes'",    
    "type": "authorized_user"
}' > client_secret.json

echo "--------------------------------------------------"
echo "Begin to clone deploy from $url"
git clone $url $solution_id > /dev/null 2>&1
echo "Clone finish"
echo "--------------------------------------------------"
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
    echo "Begin to use Terraform to Deploy"
    echo $parameters | jq -r 'to_entries[] | .key + "=\"" + .value +"\""' > ./pangu.tfvars
    mysql --host=$host --user=$user --password=$password --database="ads" -N --execute="select CONCAT(id,'=\"',default_value,'\"') from parameters where solution_id='$solution_id' and show_on_ui=0 ;" >> ./pangu.tfvars
    echo "--------------------------------------------------"
    cat pangu.tfvars
    echo "--------------------------------------------------"
    # terraform init -backend-config="bucket=pangu-terraform-state" -backend-config="prefix=pangu-dev-$DEPLOY_ID"
    terraform init -backend-config="address=192.168.156.2:8500" -backend-config="path=ads_dev/$DEPLOY_ID/terraform_state" -backend-config="scheme=http"
    terraform apply -auto-approve -var-file="pangu.tfvars" -no-color
    if [ $? -eq 0 ]; then
        mysql --host=$host --user=$user --password=$password --database="ads" --execute="update deploy set status='deploy_success' where id='$DEPLOY_ID';"
    else
        mysql --host=$host --user=$user --password=$password --database="ads" --execute="update deploy set status='deploy_failed' where id='$DEPLOY_ID';"
    fi
else
    echo "Begin to use Bash to Deploy"
    echo $parameters | jq -r 'to_entries[] | "export " + .key + "=\"" + .value +"\""' > ./pangu.env
    mysql --host=$host --user=$user --password=$password --database="ads" -N --execute="select CONCAT('export ',id,'=\"',default_value,'\"') from parameters where solution_id='$solution_id' and show_on_ui=0 ;" >> ./pangu.env
    source ./pangu.env
    echo "--------------------------------------------------"
    cat pangu.env
    echo "--------------------------------------------------"
    bash deploy.sh
    if [ $? -eq 0 ]; then
        mysql --host=$host --user=$user --password=$password --database="ads" --execute="update deploy set status='deploy_success' where id='$DEPLOY_ID';"
    else
        mysql --host=$host --user=$user --password=$password --database="ads" --execute="update deploy set status='deploy_failed' where id='$DEPLOY_ID';"
    fi    
fi