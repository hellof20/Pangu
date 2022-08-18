#!/bin/bash

cd /tmp/$DEPLOY_ID/$solution_id/$tf_path
git pull > git.log 2>&1
terraform apply -auto-approve -var-file="terraform.tfvars" -var="access_token=$access_token" -no-color > /tmp/$DEPLOY_ID/$solution_id/deploy.log 2>&1
if [ $? -eq 0 ]; then
    mysql --host=$host --user=$user --password=$password --database="ads" --execute="update deploy set status='success' where id='$DEPLOY_ID';"
else
    mysql --host=$host --user=$user --password=$password --database="ads" --execute="update deploy set status='failed' where id='$DEPLOY_ID';"
fi