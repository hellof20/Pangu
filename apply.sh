#!/bin/bash

echo "--------------------------------------------------"
echo "Begin to clone deploy from $url"
git clone $url $solution_id > /dev/null
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
    echo "cat pangu.tfvars"
    cat pangu.tfvars
    echo "--------------------------------------------------"
    terraform init 
    terraform apply -auto-approve -var-file="pangu.tfvars" -var="access_token=$access_token" -no-color -state=$data_dir/$DEPLOY_ID/terraform.tfstate 
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
    CLOUDSDK_AUTH_ACCESS_TOKEN=$access_token bash deploy.sh 
    if [ $? -eq 0 ]; then
        mysql --host=$host --user=$user --password=$password --database="ads" --execute="update deploy set status='deploy_success' where id='$DEPLOY_ID';"
    else
        mysql --host=$host --user=$user --password=$password --database="ads" --execute="update deploy set status='deploy_failed' where id='$DEPLOY_ID';"
    fi    
fi