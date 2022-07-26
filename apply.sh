#!/bin/bash
echo $DEPLOY_ID
echo $url

mkdir -p /tmp/$DEPLOY_ID
cd /tmp/$DEPLOY_ID
git clone $url > tf.log 2>&1
cd /tmp/$DEPLOY_ID/tf-tutorial
terraform init
terraform apply -auto-approve -var="project=$PROJECT_ID" -var="access_token=$access_token" -no-color >> tf.log 2>&1
if [ $? -eq 0 ]; then
    mysql --user="pwm" --password="szcb__123" --database="ads" --execute="update deploy set status='success' where id='$DEPLOY_ID';"
else
    mysql --user="pwm" --password="szcb__123" --database="ads" --execute="update deploy set status='failed' where id='$DEPLOY_ID';"
fi