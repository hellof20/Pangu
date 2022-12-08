#!/bin/bash

data_dir=/data/pangu
cd $data_dir/$DEPLOY_ID/$solution_id/$deploy_path
echo "--------------------------------------------------" > $data_dir/$DEPLOY_ID/deploy.log
if [[ $deploy_type == "Terraform" ]]
then
    echo $parameters | jq -r 'to_entries[] | .key + "=\"" + .value +"\""' > ./pangu.tfvars
    mysql --host=$host --user=$user --password=$password --database="ads" -N --execute="select CONCAT(id,'=\"',default_value,'\"') from parameters where solution_id='$solution_id' and show_on_ui=0 ;" >> ./pangu.tfvars
    cat pangu.tfvars >> $data_dir/$DEPLOY_ID/deploy.log
    echo "--------------------------------------------------" >> $data_dir/$DEPLOY_ID/deploy.log
    terraform apply -destroy -auto-approve -var-file="pangu.tfvars" -var="access_token=$access_token" -no-color -state=$data_dir/$DEPLOY_ID/terraform.tfstate >> $data_dir/$DEPLOY_ID/deploy.log 2>&1
    if [ $? -eq 0 ]; then
        mysql --host=$host --user=$user --password=$password --database="ads" --execute="update deploy set status='destroy_success' where id='$DEPLOY_ID';"
    else
        mysql --host=$host --user=$user --password=$password --database="ads" --execute="update deploy set status='destroy_failed' where id='$DEPLOY_ID';"
    fi
else
    echo $parameters | jq -r 'to_entries[] | "export " + .key + "=\"" + .value +"\""' > ./pangu.env
    mysql --host=$host --user=$user --password=$password --database="ads" -N --execute="select CONCAT('export ',id,'=\"',default_value,'\"') from parameters where solution_id='$solution_id' and show_on_ui=0 ;" >> ./pangu.env
    source ./pangu.env
    cat pangu.env >> $data_dir/$DEPLOY_ID/deploy.log
    echo "--------------------------------------------------" >> $data_dir/$DEPLOY_ID/deploy.log
    ls
    CLOUDSDK_AUTH_ACCESS_TOKEN=$access_token bash destroy.sh > $data_dir/$DEPLOY_ID/deploy.log 2>&1
    if [ $? -eq 0 ]; then
        mysql --host=$host --user=$user --password=$password --database="ads" --execute="update deploy set status='destroy_success' where id='$DEPLOY_ID';"
    else
        mysql --host=$host --user=$user --password=$password --database="ads" --execute="update deploy set status='destroy_failed' where id='$DEPLOY_ID';"
    fi    
fi