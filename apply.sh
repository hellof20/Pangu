#!/bin/bash

deploy_path="/data/pangu"
mkdir -p $deploy_path/$DEPLOY_ID

cd $deploy_path/$DEPLOY_ID
rm -rf $solution_id
echo "--------------------------------------------------" > $deploy_path/$DEPLOY_ID/deploy.log
echo "Begin to clone deploy from $url" >> $deploy_path/$DEPLOY_ID/deploy.log
git clone $url $solution_id >> $deploy_path/$DEPLOY_ID/deploy.log 2>&1
echo "Clone finish" >> $deploy_path/$DEPLOY_ID/deploy.log
echo "--------------------------------------------------" >> $deploy_path/$DEPLOY_ID/deploy.log
cd $solution_id
if [ -n "$version" ];then
echo "Checkout to version: $version" >> $deploy_path/$DEPLOY_ID/deploy.log
git checkout $version >> $deploy_path/$DEPLOY_ID/deploy.log 2>&1
echo "Checkout finish" >> $deploy_path/$DEPLOY_ID/deploy.log 2>&1
fi
customer_input=$(mysql --host=$host --user=$user --password=$password --database="ads" -N --execute="select parameters from deploy where id='$DEPLOY_ID';")

if [[ $deploy_type == "Terraform" ]]
then
    echo "Begin to use Terraform to Deploy" >> $deploy_path/$DEPLOY_ID/deploy.log
    cd $tf_path
    echo $customer_input | jq -r 'to_entries[] | .key + "=\"" + .value +"\""' > ./pangu.tfvars
    echo "--------------------------------------------------" >> $deploy_path/$DEPLOY_ID/deploy.log
    echo "cat pangu.tfvars" >> $deploy_path/$DEPLOY_ID/deploy.log
    cat pangu.tfvars >> $deploy_path/$DEPLOY_ID/deploy.log
    echo "--------------------------------------------------" >> $deploy_path/$DEPLOY_ID/deploy.log
    mysql --host=$host --user=$user --password=$password --database="ads" -N --execute="select CONCAT(id,'=\"',default_value,'\"') from parameters where solution_id='$solution_id' and show_on_ui=0 ;" >> ./pangu.tfvars
    terraform init >> $deploy_path/$DEPLOY_ID/deploy.log 2>&1
    terraform apply -auto-approve -var-file="pangu.tfvars" -var="access_token=$access_token" -no-color -state=$deploy_path/$DEPLOY_ID/terraform.tfstate >> $deploy_path/$DEPLOY_ID/deploy.log 2>&1
    if [ $? -eq 0 ]; then
        mysql --host=$host --user=$user --password=$password --database="ads" --execute="update deploy set status='deploy_success' where id='$DEPLOY_ID';"
    else
        mysql --host=$host --user=$user --password=$password --database="ads" --execute="update deploy set status='deploy_failed' where id='$DEPLOY_ID';"
    fi
else
    echo "Begin to use Bash to Deploy" >> $deploy_path/$DEPLOY_ID/deploy.log
    cd $bash_path
    echo $customer_input | jq -r 'to_entries[] | "export " + .key + "=\"" + .value +"\""' > ./pangu.env
    source ./pangu.env
    echo "--------------------------------------------------" >> $deploy_path/$DEPLOY_ID/deploy.log
    cat pangu.env >> $deploy_path/$DEPLOY_ID/deploy.log
    echo "--------------------------------------------------" >> $deploy_path/$DEPLOY_ID/deploy.log
    CLOUDSDK_AUTH_ACCESS_TOKEN=$access_token bash deploy.sh >> $deploy_path/$DEPLOY_ID/deploy.log 2>&1
    if [ $? -eq 0 ]; then
        mysql --host=$host --user=$user --password=$password --database="ads" --execute="update deploy set status='deploy_success' where id='$DEPLOY_ID';"
    else
        mysql --host=$host --user=$user --password=$password --database="ads" --execute="update deploy set status='deploy_failed' where id='$DEPLOY_ID';"
    fi    
fi