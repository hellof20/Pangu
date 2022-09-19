#!/bin/bash

deploy_path=/data/pangu

pwd
mkdir -p $deploy_path/$DEPLOY_ID
cd $deploy_path/$DEPLOY_ID
if [ ! -d $solution_id ]; then
    git clone $url $solution_id > git.log 2>&1
else
    git -C $solution_id pull > ../git.log 2>&1
fi
cd $solution_id/$tf_path

customer_input=$(mysql --host=$host --user=$user --password=$password --database="ads" -N --execute="select parameters from deploy where id='$DEPLOY_ID';")
echo $customer_input | jq -r 'to_entries[] | .key + "=\"" + .value +"\""' > ./pangu.tfvars
mysql --host=$host --user=$user --password=$password --database="ads" -N --execute="select CONCAT(id,'=\"',default_value,'\"') from parameters where solution_id='$solution_id' and show_on_ui=0 ;" >> ./pangu.tfvars

terraform init > $deploy_path/$DEPLOY_ID/deploy.log 2>&1
terraform apply -auto-approve -var-file="pangu.tfvars" -var="access_token=$access_token" -no-color >> $deploy_path/$DEPLOY_ID/deploy.log 2>&1
if [ $? -eq 0 ]; then
    mysql --host=$host --user=$user --password=$password --database="ads" --execute="update deploy set status='success' where id='$DEPLOY_ID';"
else
    mysql --host=$host --user=$user --password=$password --database="ads" --execute="update deploy set status='failed' where id='$DEPLOY_ID';"
fi