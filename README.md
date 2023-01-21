# Pangu project

Deploy on Ubuntu 20.04

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


### prepare client_secret.json
1. Generate client_secret.json
2. Put your client_secret.json to google-ads-solution folder

### Deploy on k8s
- create secret for client_secret.json
```
kubectl create configmap ads-dev-client-secret --from-file=client_secret.json
```

- create TLS (You need your tls certificate)
```
kubectl create secret tls joey618-top --key privkey.pem --cert fullchain.pem
```

- create mysql configmap
```
kubectl create configmap mysql-config --from-literal=host=192.168.158.3 --from-literal=user=root --from-literal=password=pangu__123 --from-literal=db=ads
```

- deploy
```
kubectl apply -f ads.yaml
```

### configure OAuth consent screen

### configure Authorized redirect URIs
- get external ip address
```
kubectl get ingress
```

- domain resolve

- add you redict url to client secret
```
https://your_dns_record/oauth2callback
```

### Access the application


- access
https://your_dns_record
