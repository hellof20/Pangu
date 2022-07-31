# Google Ads Solution

### OAuth 2.0 Client and OAuth consent screen
todo

### MySQL
1. Create MySQL Database
2. set flags
```
default_time_zone = +08:00
```
3. init database
  run sql
4. add solution
```
insert into ads.solution(id,name,url) values('baremetal','Bare Metal','https://github.com/hellof20/tf-tutorial.git');
```

### Server init
```
sudo -i
apt update
apt install -y git mysql-client-core-8.0 python3-pip
mkdir -p /data/pangu
git clone --depth=1 https://github.com/hellof20/google-ads-solution.git /data/pangu
cd /data/pangu
pip3 install -r requirements.txt
gsutil cp gs://pangu-hk/client_secret.json .
export host=your mysql ip address
export user=your username
export password=your mysql password
```

### Install Terraform
https://www.terraform.io/downloads

### Run backend server
```
python3 main.py
```
