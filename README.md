# Pangu project

Deploy on Ubuntu 20.04

### MySQL
1. Create MySQL Database
```
CREATE DATABASE `ads` DEFAULT CHARACTER SET utf8mb4;
```
2. init database tables
```
mysql -u user -p password ads < sql/ads.sql
```


### prepare client_secret.json
1. Generate client_secret.json
2. Put your client_secret.json to google-ads-solution folder

### Deploy on k8s
- create namespace
```
kubectl create ns pangu
```

- create secret for client_secret.json
```
kubectl -n pangu create configmap pangu-dev-client-secret --from-file=client_secret.json
```

- create TLS (You need your tls certificate)
```
kubectl -n pangu create secret tls joey618-top --key privkey.pem --cert fullchain.pem
```

- create mysql configmap
```
kubectl -n pangu create configmap mysql-config --from-literal=host=mysql --from-literal=user=root --from-literal=password=password --from-literal=db=ads
```

- deploy
```
kubectl apply -f pangu.yaml
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
