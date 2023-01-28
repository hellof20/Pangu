-- MySQL dump 10.13  Distrib 8.0.31, for Linux (x86_64)
--
-- Host: localhost    Database: ads
-- ------------------------------------------------------
-- Server version	8.0.31-0ubuntu0.20.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admin_user`
--

DROP TABLE IF EXISTS `admin_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin_user` (
  `name` varchar(100) NOT NULL,
  `email` varchar(100) CHARACTER SET utf8mb4 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin_user`
--

LOCK TABLES `admin_user` WRITE;
/*!40000 ALTER TABLE `admin_user` DISABLE KEYS */;
INSERT INTO `admin_user` VALUES ('pwm@','admin@pwm.altostrat.com');
/*!40000 ALTER TABLE `admin_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `deploy`
--

DROP TABLE IF EXISTS `deploy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `deploy` (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `status` varchar(100) NOT NULL,
  `solution_id` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `parameters` json NOT NULL,
  `project_id` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=113 DEFAULT CHARSET=utf8mb4 ;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `deploy`
--

LOCK TABLES `deploy` WRITE;
/*!40000 ALTER TABLE `deploy` DISABLE KEYS */;
INSERT INTO `deploy` VALUES (93,'2022-12-12 07:39:35','2022-12-21 15:17:16','deploy_success','vm-test','admin@pwm.altostrat.com','{\"network\": \"myvpc\", \"version\": \"\", \"vm_name\": \"ppp2\", \"project_id\": \"speedy-victory-336109\", \"subnetwork\": \"myvpc\", \"deploy_type\": \"Terraform\"}','speedy-victory-336109'),(96,'2022-12-14 10:57:41','2022-12-16 06:37:26','destroy_success','redis-cluster-gke','admin@pwm.altostrat.com','{\"name\": \"redis\", \"zone\": \"us-central1-a\", \"network\": \"myvpc\", \"version\": \"\", \"project_id\": \"speedy-victory-336109\", \"deploy_type\": \"Bash\", \"redis_version\": \"6.2.8\", \"redis_password\": \"pwm123456\"}','speedy-victory-336109'),(97,'2022-12-14 14:38:55','2022-12-14 16:28:05','destroy_success','ververica','admin@pwm.altostrat.com','{\"name\": \"vvp2\", \"zone\": \"us-central1-a\", \"bucket\": \"vvp2\", \"network\": \"myvpc\", \"version\": \"\", \"project_id\": \"speedy-victory-336109\", \"deploy_type\": \"Bash\"}','speedy-victory-336109'),(101,'2022-12-20 10:42:33','2022-12-20 11:01:59','destroy_success','vm-test','admin@pwm.altostrat.com','{\"network\": \"project2vpc\", \"version\": \"\", \"vm_name\": \"ppp5\", \"project_id\": \"my-project-2-337005\", \"subnetwork\": \"lowasubnet\", \"deploy_type\": \"Bash\"}','my-project-2-337005'),(103,'2022-12-20 15:18:09','2022-12-20 15:21:40','destroy_success','auto-label','admin@pwm.altostrat.com','{\"version\": \"\", \"project_id\": \"speedy-victory-336109\", \"deploy_type\": \"Bash\", \"ORGANIZATION_ID\": \"235918811881\"}','speedy-victory-336109'),(104,'2022-12-20 15:24:17','2022-12-21 15:15:32','deploy_success','auto-label','wenming@pwm.altostrat.com','{\"version\": \"\", \"project_id\": \"my-project-2-337005\", \"deploy_type\": \"Bash\", \"ORGANIZATION_ID\": \"235918811881\"}','my-project-2-337005'),(107,'2022-12-21 12:50:46','2022-12-21 13:11:24','destroy_success','redis-cluster-gke','admin@pwm.altostrat.com','{\"name\": \"myredis\", \"zone\": \"us-central1-a\", \"network\": \"myvpc\", \"version\": \"\", \"project_id\": \"speedy-victory-336109\", \"deploy_type\": \"Bash\", \"redis_version\": \"6.2.8\", \"redis_password\": \"pwm123456\"}','speedy-victory-336109'),(108,'2022-12-21 12:51:58','2023-01-13 10:05:06','deploy_success','baremetal','admin@pwm.altostrat.com','{\"bucket\": \"pwmaaaaaaa\", \"version\": \"\", \"client_id\": \"a\", \"project_id\": \"pangu-test-1\", \"deploy_type\": \"Bash\", \"client_secret\": \"a\", \"refresh_token\": \"a\", \"developer_token\": \"a\", \"login_customer_id\": \"a\", \"notification_email\": \"a\"}','pangu-test-1'),(110,'2023-01-09 06:40:18','2023-01-09 07:53:47','destroy_success','wow','admin@pwm.altostrat.com','{\"name\": \"mygame\", \"zone\": \"us-central1-a\", \"version\": \"\", \"project_id\": \"speedy-victory-336109\", \"deploy_type\": \"Bash\"}','speedy-victory-336109'),(112,'2023-01-28 06:09:28','2023-01-28 12:47:58','deploy_success','vm-test','admin@pwm.altostrat.com','{\"network\": \"myvpc\", \"version\": \"\", \"vm_name\": \"ppp9\", \"disclaimer\": \"on\", \"project_id\": \"speedy-victory-336109\", \"subnetwork\": \"myvpc\", \"deploy_type\": \"Bash\"}','speedy-victory-336109');
/*!40000 ALTER TABLE `deploy` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `parameters`
--

DROP TABLE IF EXISTS `parameters`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `parameters` (
  `id` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `solution_id` varchar(100) NOT NULL,
  `description` text CHARACTER SET utf8mb4 NOT NULL,
  `example` varchar(100) CHARACTER SET utf8mb4 NOT NULL,
  `show_on_ui` tinyint(1) NOT NULL,
  `type` varchar(100) NOT NULL,
  `default_value` varchar(100) CHARACTER SET utf8mb4 DEFAULT NULL,
  PRIMARY KEY (`id`,`solution_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parameters`
--

LOCK TABLES `parameters` WRITE;
/*!40000 ALTER TABLE `parameters` DISABLE KEYS */;
INSERT INTO `parameters` VALUES ('ADH_CID','ADH_CID','lego','ADH_CID','',1,'string',''),('appengine_location','appengine_location','baremetal',' ',' ',0,'string','us-central'),('bucket','Bucket Name','baremetal','GCS bucket to store input data.','my-bucket-id',1,'string',NULL),('bucket','Bucket Name','ververica','Bucket Name','xxxxx',1,'string',''),('client_id','Client ID','baremetal','Client ID','xxxxx',1,'string',NULL),('CLIENT_ID','Client ID','lego','Client ID','xxxxx',1,'string',NULL),('client_secret','Client Secret','baremetal','Client Secret','xxxxxx',1,'string',NULL),('CLIENT_SECRET','Client Secret','lego','Client Secret','xxxxx',1,'string',NULL),('cluster_machine_type','Machine Type','clickhouse','the machine type in clickhouse cluster','n2-standard-16',1,'string',NULL),('cluster_network','GCP Network','clickhouse','the network to attach resources to','default',1,'string',NULL),('cluster_size','Cluster Size','clickhouse','number of nodes in clickhouse cluster','4',1,'int',NULL),('cluster_subnetwork','Sub Network','clickhouse','the subnetwork to attach resources to','default',1,'string',NULL),('data_disksize','Disk size','clickhouse','size of the data disk, in GB','30',1,'int',NULL),('data_disktype','Disk Type','clickhouse','the data disk used in clickhouse cluster','pd-ssd',0,'string',NULL),('deploy_type','Deploy type','auto-label','Deploy_type','Bash',1,'select',NULL),('deploy_type','Deploy type','baremetal','Terraform or Bash','Terraform',1,'select',NULL),('deploy_type','Deploy type','clickhouse','Deploy_type','Terraform',1,'select',NULL),('deploy_type','Deploy type','lego','Terraform or Bash','Terraform',1,'select',NULL),('deploy_type','Deploy type','redis-cluster-gke','Terraform or Bash','Terraform',1,'select',NULL),('deploy_type','Deploy type','ververica','Deploy_type','Bash',1,'select',NULL),('deploy_type','Deploy type','vm-test','Deploy_type','',1,'select',NULL),('deploy_type','Deploy type','wow','Deploy_type','Bash',1,'select',NULL),('developer_token','developer_token','baremetal',' ','0qxFO_azpn5Sn4_QCeWt7g',1,'string',NULL),('developer_token','developer_token','lego',' ','0qxFO_azpn5Sn4_QCeWt7g',1,'string',NULL),('gcs_location','gcs_location','baremetal',' ',' ',0,'string','US'),('INSTALLED_ADH_AUDIENCE_WORKFLOW','INSTALLED_ADH_AUDIENCE_WORKFLOW','lego','INSTALLED_ADH_AUDIENCE_WORKFLOW','N',1,'string','N'),('INSTALLED_ADH_BRANDING_WORKFLOW','INSTALLED_ADH_BRANDING_WORKFLOW','lego','INSTALLED_ADH_BRANDING_WORKFLOW','N',1,'string','N'),('INSTALLED_ADH_CREATIVE_WORKFLOW','INSTALLED_ADH_CREATIVE_WORKFLOW','lego','INSTALLED_ADH_CREATIVE_WORKFLOW','N',1,'string','N'),('INSTALLED_BACKFILL_WORKFLOW_TRIGGER','INSTALLED_BACKFILL_WORKFLOW_TRIGGER','lego','INSTALLED_BACKFILL_WORKFLOW_TRIGGER','N',1,'string','N'),('INSTALLED_CPP_WORKFLOW','INSTALLED_CPP_WORKFLOW','lego','INSTALLED_CPP_WORKFLOW','N',1,'string','N'),('INSTALLED_TRDPTY_TRIX_DATA','INSTALLED_TRDPTY_TRIX_DATA','lego','INSTALLED_TRDPTY_TRIX_DATA','N',1,'string','N'),('INSTALLED_WORKFLOW','INSTALLED_WORKFLOW','lego','INSTALLED_WORKFLOW','App + NonApp',1,'string','App + NonApp'),('login_customer_id','login_customer_id','baremetal','Ten digit customer id','1234567890',1,'string',NULL),('MCC_CIDS','MCC_CIDS','lego','MCC_CIDS','',1,'string',''),('name','GKE Cluster Name','redis-cluster-gke','GKE Cluster Name','xxxx',1,'string',NULL),('name','GKE Name','ververica','VM Name','xxxx',1,'string',NULL),('name','GKE Name','wow','VM Name','xxxx',1,'string',NULL),('network','GCP Network','redis-cluster-gke','GCP Network','default',1,'string',NULL),('network','GCP Network','ververica','GCP Network','default',1,'string',NULL),('network','GCP Network','vm-test','GCP Network','default',1,'string',NULL),('notification_email','notification_email','baremetal','\"[Optional]A list of email addresses separated by comma.\nDaily summary stats will be sent by email if not empty\"',' ',1,'string',NULL),('ORGANIZATION_ID','ORGANIZATION ID','auto-label','ORGANIZATION ID','xxxxxxxxxxxxx',1,'string',NULL),('project_id','Project ID','auto-label','GCP Project ID','pangu-test-1',1,'string',NULL),('project_id','Project ID','baremetal','GCP Project ID','pangu-test-1',1,'string',NULL),('project_id','Project ID','clickhouse','the Google Cloud project id to use','xxxxx',1,'string',NULL),('project_id','Project ID','lego','GCP Project ID','lego-chjerry-lab',1,'string',NULL),('project_id','Project ID','redis-cluster-gke','GCP Project ID','pangu-test-1',1,'select',NULL),('project_id','Project ID','ververica','GCP Project ID','pangu-test-1',1,'string',NULL),('project_id','Project ID','vm-test','GCP Project ID','pangu-test-1',1,'select',NULL),('project_id','Project ID','wow','GCP Project ID','pangu-test-1',1,'string',NULL),('redis_password','Redis Password','redis-cluster-gke','Redis Password','pwm123',1,'string',''),('redis_version','Redis Version','redis-cluster-gke','Redis Version','7.0.6',1,'string',''),('refresh_token','refresh_token','baremetal',' ',' ',1,'string',NULL),('REFRESH_TOKEN','REFRESH_TOKEN','lego','REFRESH_TOKEN','',1,'string',''),('region','region','baremetal',' ',' ',0,'string','us-central1'),('region','GCP Region','clickhouse','the Google Cloud region to provision resources in','us-central1',1,'string',NULL),('REGION','REGION','lego','GCP region','us-central1',1,'string','us-central1'),('REGION_FOR_DS','REGION_FOR_DS','lego','GCP region for ds','us',1,'string','us'),('subnetwork','Subnet','vm-test','Subnet',' ',1,'string',NULL),('time_zone','time_zone','baremetal',' ',' ',0,'string','Asia/Shanghai'),('version','Version','auto-label','Version','v1',1,'select',NULL),('version','Version','baremetal','Version','v3',1,'select',NULL),('version','Version','clickhouse','Version','v1',1,'select',NULL),('version','Version','lego','Version','v3',1,'select',NULL),('version','Version','redis-cluster-gke','Version','v1',1,'select',NULL),('version','Version','ververica','Version','v1',1,'select',NULL),('version','Version','vm-test','Version','v1',1,'select',NULL),('version','Version','wow','Version','v1',1,'select',NULL),('vm_name','VM Name','vm-test','VM Name','xxxx',1,'string',NULL),('zone','zone','baremetal',' ',' ',0,'string','us-central1-c'),('zone','Zone','clickhouse','the Google Cloud zone to provision zonal resources in','us-central1-a',1,'string',NULL),('zone','Zone','redis-cluster-gke','Zone','us-central1-a',1,'string',''),('zone','Zone','ververica','Zone','us-central1-a',1,'string','us-central1-c'),('zone','Zone','vm-test','Zone','us-central1-a',0,'string','us-central1-c'),('zone','Zone','wow','Zone','us-central1-a',1,'string','us-central1-c');
/*!40000 ALTER TABLE `parameters` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `permission`
--

DROP TABLE IF EXISTS `permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `permission` (
  `scope` text CHARACTER SET utf8mb4 NOT NULL,
  `solution_id` varchar(100) NOT NULL,
  PRIMARY KEY (`solution_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permission`
--

LOCK TABLES `permission` WRITE;
/*!40000 ALTER TABLE `permission` DISABLE KEYS */;
INSERT INTO `permission` VALUES ('https://www.googleapis.com/auth/userinfo.email,https://www.googleapis.com/auth/compute,https://www.googleapis.com/auth/cloud-platform','auto-label'),('openid,https://www.googleapis.com/auth/userinfo.email,https://www.googleapis.com/auth/compute,https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/drive,https://www.googleapis.com/auth/appengine.admin,https://www.googleapis.com/auth/datastore,https://www.googleapis.com/auth/adsdatahub','baremetal'),('https://www.googleapis.com/auth/userinfo.email,https://www.googleapis.com/auth/compute,https://www.googleapis.com/auth/cloud-platform','clickhouse'),('openid,https://www.googleapis.com/auth/userinfo.email,https://www.googleapis.com/auth/compute,https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/drive,https://www.googleapis.com/auth/appengine.admin,https://www.googleapis.com/auth/datastore,https://www.googleapis.com/auth/adsdatahub','lego'),('https://www.googleapis.com/auth/userinfo.email,https://www.googleapis.com/auth/compute,https://www.googleapis.com/auth/cloud-platform','redis-cluster-gke'),('https://www.googleapis.com/auth/userinfo.email,https://www.googleapis.com/auth/compute,https://www.googleapis.com/auth/cloud-platform','ververica'),('https://www.googleapis.com/auth/userinfo.email,https://www.googleapis.com/auth/compute,https://www.googleapis.com/auth/cloud-platform','vm-test'),('https://www.googleapis.com/auth/userinfo.email,https://www.googleapis.com/auth/compute,https://www.googleapis.com/auth/cloud-platform','wow');
/*!40000 ALTER TABLE `permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `solution`
--

DROP TABLE IF EXISTS `solution`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `solution` (
  `id` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `url` varchar(255) NOT NULL,
  `deploy_path` varchar(100) CHARACTER SET utf8mb4 NOT NULL,
  `if_need_oauth` tinyint(1) NOT NULL,
  `deploy_type` varchar(100) NOT NULL,
  `author` varchar(100) DEFAULT NULL,
  `guide_url` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`,`deploy_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `solution`
--

LOCK TABLES `solution` WRITE;
/*!40000 ALTER TABLE `solution` DISABLE KEYS */;
INSERT INTO `solution` VALUES ('auto-label','Auto Label Resource','https://github.com/hellof20/GoogleCloudPlatform-community.git','tutorials/cloud-asset-inventory-auto-label-resources',0,'Bash','pwm@google.com','https://cloud.google.com/community/tutorials/cloud-asset-inventory-auto-label-resources'),('baremetal','Bare Metal','https://professional-services.googlesource.com/solutions/ads-bare-metal','./',1,'Bash','chii@google.com',NULL),('baremetal','Bare Metal','https://professional-services.googlesource.com/solutions/ads-bare-metal','terraform/',1,'Terraform','chii@google.com',NULL),('clickhouse','Clickhouse','https://github.com/hellof20/clickhouse-on-gce.git','terraform/',0,'Terraform','jscheng@google.com','https://docs.google.com/document/d/1glJ9j0EwWI93dhrbh-neAWqnwTlF9CRQhcW4zQ58UF0/'),('lego','LEGO','https://professional-services.googlesource.com/solutions/ads-bi-suite','deploy_with_no_interaction',1,'Bash','chjerry@google.com',NULL),('redis-cluster-gke','Redis Cluster on GKE','https://github.com/hellof20/redis-cluster-gke.git','./',0,'Bash','pwm@google.com',NULL),('ververica','Ververica Platform','https://github.com/hellof20/ververica-gke','./',0,'Bash','pwm@google.com','https://docs.ververica.com/installation/hosted_k8s_quickstart/gcp_gke.html'),('vm-test','VM Test','https://github.com/hellof20/tf-tutorial.git','./',0,'Bash','pwm@google.com',NULL),('vm-test','VM Test','https://github.com/hellof20/tf-tutorial.git','terraform/',0,'Terraform','pwm@google.com',NULL),('wow','TrinityCore on GKE','https://github.com/hellof20/TrinityCore-on-GCP-GKE','./',0,'Bash','pwm@google.com',NULL);
/*!40000 ALTER TABLE `solution` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-01-28 20:50:46
