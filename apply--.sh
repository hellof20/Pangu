#!/bin/bash

data_dir="/data/pangu"
mkdir -p $data_dir/$DEPLOY_ID

cd $data_dir/$DEPLOY_ID
sudo rm -rf $solution_id

echo "--------------------------------------------------" > $data_dir/$DEPLOY_ID/deploy.log
echo "Begin to clone deploy from $url" >> $data_dir/$DEPLOY_ID/deploy.log
git clone $url $solution_id 
echo "Clone finish" >> $data_dir/$DEPLOY_ID/deploy.log
echo "--------------------------------------------------" >> $data_dir/$DEPLOY_ID/deploy.log
cd $solution_id

version=$(echo $parameters | jq .version)
if [[ $version != '""' ]];then
    echo "Checkout to version: $version" >> $data_dir/$DEPLOY_ID/deploy.log
    git checkout $version >> $data_dir/$DEPLOY_ID/deploy.log 2>&1
    echo "Checkout finish" >> $data_dir/$DEPLOY_ID/deploy.log 2>&1
fi

cd $deploy_path
if [[ $deploy_type == "Terraform" ]]
then
    echo "Begin to use Terraform to Deploy" >> $data_dir/$DEPLOY_ID/deploy.log
    
    echo $parameters | jq -r 'to_entries[] | .key + "=\"" + .value +"\""' > ./pangu.tfvars
    mysql --host=$host --user=$user --password=$password --database="ads" -N --execute="select CONCAT(id,'=\"',default_value,'\"') from parameters where solution_id='$solution_id' and show_on_ui=0 ;" >> ./pangu.tfvars
    echo "--------------------------------------------------" >> $data_dir/$DEPLOY_ID/deploy.log
    echo "cat pangu.tfvars" >> $data_dir/$DEPLOY_ID/deploy.log
    cat pangu.tfvars >> $data_dir/$DEPLOY_ID/deploy.log
    echo "--------------------------------------------------" >> $data_dir/$DEPLOY_ID/deploy.log
    terraform init >> $data_dir/$DEPLOY_ID/deploy.log 2>&1
    terraform apply -auto-approve -var-file="pangu.tfvars" -var="access_token=$access_token" -no-color -state=$data_dir/$DEPLOY_ID/terraform.tfstate >> $data_dir/$DEPLOY_ID/deploy.log 2>&1
    if [ $? -eq 0 ]; then
        mysql --host=$host --user=$user --password=$password --database="ads" --execute="update deploy set status='deploy_success' where id='$DEPLOY_ID';"
    else
        mysql --host=$host --user=$user --password=$password --database="ads" --execute="update deploy set status='deploy_failed' where id='$DEPLOY_ID';"
    fi
else
    echo "Begin to use Bash to Deploy" >> $data_dir/$DEPLOY_ID/deploy.log
    echo $parameters | jq -r 'to_entries[] | "export " + .key + "=\"" + .value +"\""' > ./pangu.env
    mysql --host=$host --user=$user --password=$password --database="ads" -N --execute="select CONCAT('export ',id,'=\"',default_value,'\"') from parameters where solution_id='$solution_id' and show_on_ui=0 ;" >> ./pangu.env
    source ./pangu.env
    echo "--------------------------------------------------" >> $data_dir/$DEPLOY_ID/deploy.log
    cat pangu.env >> $data_dir/$DEPLOY_ID/deploy.log
    echo "--------------------------------------------------" >> $data_dir/$DEPLOY_ID/deploy.log
    CLOUDSDK_AUTH_ACCESS_TOKEN=$access_token bash deploy.sh >> $data_dir/$DEPLOY_ID/deploy.log 2>&1
    if [ $? -eq 0 ]; then
        mysql --host=$host --user=$user --password=$password --database="ads" --execute="update deploy set status='deploy_success' where id='$DEPLOY_ID';"
    else
        mysql --host=$host --user=$user --password=$password --database="ads" --execute="update deploy set status='deploy_failed' where id='$DEPLOY_ID';"
    fi    
fi