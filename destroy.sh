#!/bin/bash

deploy_path=/data/pangu
cd $deploy_path/$DEPLOY_ID/$solution_id
echo "--------------------------------------------------" > $deploy_path/$DEPLOY_ID/deploy.log

if [[ $deploy_type == "Terraform" ]]
then
    cd $tf_path
    cat pangu.tfvars >> $deploy_path/$DEPLOY_ID/deploy.log
    echo "--------------------------------------------------" >> $deploy_path/$DEPLOY_ID/deploy.log
    terraform apply -destroy -auto-approve -var-file="pangu.tfvars" -var="access_token=$access_token" -no-color -state=$deploy_path/$DEPLOY_ID/terraform.tfstate >> $deploy_path/$DEPLOY_ID/deploy.log 2>&1

    if [ $? -eq 0 ]; then
        mysql --host=$host --user=$user --password=$password --database="ads" --execute="update deploy set status='destroy_success' where id='$DEPLOY_ID';"
    else
        mysql --host=$host --user=$user --password=$password --database="ads" --execute="update deploy set status='destroy_failed' where id='$DEPLOY_ID';"
    fi
else
    cd $bash_path
    source ./pangu.env
    cat pangu.env >> $deploy_path/$DEPLOY_ID/deploy.log
    echo "--------------------------------------------------" >> $deploy_path/$DEPLOY_ID/deploy.log    
    CLOUDSDK_AUTH_ACCESS_TOKEN=$access_token bash destroy.sh > $deploy_path/$DEPLOY_ID/deploy.log 2>&1
    if [ $? -eq 0 ]; then
        mysql --host=$host --user=$user --password=$password --database="ads" --execute="update deploy set status='destroy_success' where id='$DEPLOY_ID';"
    else
        mysql --host=$host --user=$user --password=$password --database="ads" --execute="update deploy set status='destroy_failed' where id='$DEPLOY_ID';"
    fi    
fi