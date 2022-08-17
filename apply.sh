#!/bin/bash
echo '+++++++++++++++++++++++++++++++++'
echo $DEPLOY_ID
echo $url
echo $tf_path

mkdir -p /tmp/$DEPLOY_ID
cd /tmp/$DEPLOY_ID
git clone $url $solution_id > git.log 2>&1
cd /tmp/$DEPLOY_ID/$solution_id/$tf_path
terraform init >> /tmp/$DEPLOY_ID/$solution_id/deploy.log 2>&1
customer_input=$(mysql --host=$host --user=$user --password=$password --database="ads" -N --execute="select parameters from deploy where id='$DEPLOY_ID';")
echo $customer_input | jq -r 'to_entries[] | .key + "=\"" + .value +"\""' > ./terraform.tfvars
mysql --host=$host --user=$user --password=$password --database="ads" -N --execute="select CONCAT(id,'=\"',default_value,'\"') from parameters where solution_id='$solution_id' and show_on_ui=0 ;" >> ./terraform.tfvars

terraform apply -auto-approve -var-file="terraform.tfvars" -var="access_token=$access_token" -no-color >> /tmp/$DEPLOY_ID/$solution_id/deploy.log 2>&1
if [ $? -eq 0 ]; then
    mysql --host=$host --user=$user --password=$password --database="ads" --execute="update deploy set status='success' where id='$DEPLOY_ID';"
else
    mysql --host=$host --user=$user --password=$password --database="ads" --execute="update deploy set status='failed' where id='$DEPLOY_ID';"
fi