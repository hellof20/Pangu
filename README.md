# Google Ads Solution

Tested on Ubuntu 20.04

### MySQL
1. Create MySQL Database
```
CREATE DATABASE `ads` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
```
2. set timezone
```
default_time_zone = +08:00
```
3. init database tables
```
mysql -u user -p password ads < sql/ads.sql
```
4. insert test data
```
INSERT INTO ads.solution (id,name,url) VALUES('vm-test','VM-test','https://github.com/hellof20/tf-tutorial.git');
INSERT INTO ads.parameters (id,name,solution_id,description,example,show_on_ui,`type`,default_value) VALUES('network','GCP Network','vm-test','GCP Network','default',1,'string',NULL),('project_id','Project ID','vm-test','GCP Project ID','pangu-test-1',1,'string',NULL);
INSERT INTO ads.permission (scope) VALUES ('openid'),('https://www.googleapis.com/auth/userinfo.email'),('https://www.googleapis.com/auth/compute'),('https://www.googleapis.com/auth/cloud-platform'),('https://www.googleapis.com/auth/drive'),('https://www.googleapis.com/auth/appengine.admin');
```

### Server init
```
sudo -i
apt update
apt install -y git mysql-client-core-8.0 python3-pip jq
mkdir -p /data/pangu
git clone -b main --depth=1 https://github.com/hellof20/google-ads-solution.git
cd google-ads-solution
pip3 install -r requirements.txt
export host=your mysql ip address
export user=your username
export password=your mysql password
export db=your db name
```

### prepare client_secret.json
1. Generate client_secret.json
2. Put your client_secret.json to google-ads-solution folder

### Install Terraform
https://www.terraform.io/downloads

### Run backend server
```
python3 main.py
```

### Access the application
http://external_ip_address:8080
