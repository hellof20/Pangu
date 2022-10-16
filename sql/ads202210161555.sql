-- MySQL dump 10.13  Distrib 8.0.30, for Linux (x86_64)
--
-- Host: localhost    Database: ads
-- ------------------------------------------------------
-- Server version	8.0.30-0ubuntu0.20.04.2

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
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `deploy`
--

LOCK TABLES `deploy` WRITE;
/*!40000 ALTER TABLE `deploy` DISABLE KEYS */;
INSERT INTO `deploy` VALUES (52,'2022-10-14 06:21:10','2022-10-14 07:36:07','destroy_success','vm-test','admin@pwm.altostrat.com','{\"zone\": \"us-central1-a\", \"network\": \"myvpc\", \"version\": \"v1\", \"vm_name\": \"ppp3\", \"project_id\": \"speedy-victory-336109\", \"subnetwork\": \"myvpc\", \"deploy_type\": \"Terraform\"}','speedy-victory-336109'),(53,'2022-10-14 06:24:22','2022-10-14 07:33:11','destroy_success','vm-test','admin@pwm.altostrat.com','{\"zone\": \"us-central1-b\", \"network\": \"myvpc\", \"version\": \"v3\", \"vm_name\": \"ppp2\", \"project_id\": \"speedy-victory-336109\", \"subnetwork\": \"myvpc\", \"deploy_type\": \"Bash\"}','speedy-victory-336109'),(54,'2022-10-14 07:42:47',NULL,'new','clickhouse','admin@pwm.altostrat.com','{\"zone\": \"1\", \"region\": \"1\", \"project_id\": \"1\", \"cluster_size\": \"1\", \"data_disksize\": \"1\", \"data_disktype\": \"1\", \"cluster_network\": \"1\", \"cluster_subnetwork\": \"1\", \"cluster_machine_type\": \"1\"}','1'),(55,'2022-10-14 07:56:59','2022-10-14 08:21:39','deploy_success','vm-test','admin@pwm.altostrat.com','{\"zone\": \"us-central1-a\", \"network\": \"myvpc\", \"version\": \"v1\", \"vm_name\": \"ppp4\", \"project_id\": \"speedy-victory-336109\", \"subnetwork\": \"myvpc\", \"deploy_type\": \"Terraform\"}','speedy-victory-336109');
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
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `example` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `show_on_ui` tinyint(1) NOT NULL,
  `type` varchar(100) NOT NULL,
  `default_value` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`id`,`solution_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parameters`
--

LOCK TABLES `parameters` WRITE;
/*!40000 ALTER TABLE `parameters` DISABLE KEYS */;
INSERT INTO `parameters` VALUES ('adh_audience_dataset_id','adh_audience_dataset_id','lego','s','adh_audience',0,'string','adh_audience'),('adh_branding_dataset_id','adh_branding_dataset_id','lego','The id of adh branding dataset','adh_branding',0,'string','adh_branding'),('adh_customer_id','adh_customer_id','lego','Ads Data Hub customer id','123',1,'string',NULL),('adh_lego_dataset_id','adh_lego_dataset_id','lego','The id of adh lego dataset','adh_apps_data',0,'string','adh_apps_data'),('ads_report_dataset_id','ads_report_dataset_id','lego','The id of general lego report dataset','ads_reports_data_v4',0,'string','ads_reports_data_v4'),('appengine_location','appengine_location','baremetal',' ',' ',0,'string','us-central'),('bucket','Bucket Name','baremetal','GCS bucket to store input data.','my-bucket-id',1,'string',NULL),('client_id','Client ID','baremetal','Client ID','xxxxx',1,'string',NULL),('client_id','Client ID','lego','Client ID','xxxxx',1,'string',NULL),('client_secret','Client Secret','baremetal','Client Secret','xxxxxx',1,'string',NULL),('client_secret','Client Secret','lego','Client Secret','xxxxx',1,'string',NULL),('cluster_machine_type','cluster_machine_type','clickhouse','the machine type in clickhouse cluster','n2-standard-16',1,'string',NULL),('cluster_network','cluster_network','clickhouse','the network to attach resources to','default',1,'string',NULL),('cluster_size','cluster_size','clickhouse','number of nodes in clickhouse cluster','4',1,'int',NULL),('cluster_subnetwork','cluster_subnetwork','clickhouse','the subnetwork to attach resources to','default',1,'string',NULL),('config_dataset_id','config_dataset_id','lego','The id of config dataset','ads_report_configs',0,'string','ads_report_configs'),('data_disksize','data_disksize','clickhouse','size of the data disk, in GB','30',1,'int',NULL),('data_disktype','data_disktype','clickhouse','the data disk used in clickhouse cluster','pd-ssd',1,'string',NULL),('deploy_type','deploy_type','baremetal','Terraform or Bash','Terraform',1,'select',NULL),('deploy_type','Deploy_type','vm-test','Deploy_type','Terraform',1,'select',NULL),('developer_token','developer_token','baremetal',' ','0qxFO_azpn5Sn4_QCeWt7g',1,'string',NULL),('developer_token','developer_token','lego','s','0qxFO_azpn5Sn4_QCeWt7g',1,'string',NULL),('fx_rate_spreadsheet_id','fx_rate_spreadsheet_id','lego','The google spreadsheet id','1K438j6BExEnx0emeg8YD6HeYRhnpI9wlH1yJ_-L2Xhk',1,'string',NULL),('gcs_location','gcs_location','baremetal',' ',' ',0,'string','US'),('login_customer_id','login_customer_id','baremetal','Ten digit customer id','1234567890',1,'string',NULL),('mcc_ids','mcc_ids','lego','MCC Ids separated by \\\\n','123456789\\\\n456789123',1,'string',NULL),('namespace','namespace','lego','The lego namespace','lego',0,'string','lego'),('network','GCP Network','vm-test','GCP Network','default',1,'string',NULL),('notification_email','notification_email','baremetal','\"[Optional]A list of email addresses separated by comma.\nDaily summary stats will be sent by email if not empty\"',' ',1,'string',NULL),('project_id','Project ID','baremetal','GCP Project ID','pangu-test-1',1,'string',NULL),('project_id','project_id','clickhouse','the Google Cloud project id to use','xxxxx',1,'string',NULL),('project_id','Project ID','lego','GCP Project ID','lego-chjerry-lab',1,'string',NULL),('project_id','Project ID','vm-test','GCP Project ID','pangu-test-1',1,'string',NULL),('refresh_token','refresh_token','baremetal',' ',' ',1,'string',NULL),('region','region','baremetal',' ',' ',0,'string','us-central1'),('region','region','clickhouse','the Google Cloud region to provision resources in','us-central1',1,'string',NULL),('region','region','lego','GCP region','us-central1',0,'string','us-central1'),('storage_location','storage_location','lego','GCS storage Location','US',0,'string','US'),('subnetwork','Subnet','vm-test','Subnet',' ',1,'string',NULL),('tentacles_outbound','tentacles_outbound','lego','Hard to explain, tech infra value.','outbound/',0,'string','outbound/'),('time_zone','time_zone','baremetal',' ',' ',0,'string','Asia/Shanghai'),('timezone','timezone','lego','The timezone for cloud scheduler setup.','Asia/Shanghai',0,'string','Asia/Shanghai'),('version','Version','baremetal','Version','v3',1,'select',NULL),('version','Version','vm-test','Version','v1',1,'select',NULL),('vm_name','VM Name','vm-test','VM Name','xxxx',1,'string',NULL),('zone','zone','baremetal',' ',' ',0,'string','us-central1-c'),('zone','zone','clickhouse','the Google Cloud zone to provision zonal resources in','us-central1-a',1,'string',NULL),('zone','Zone','vm-test','Zone','us-central1-a',1,'string',NULL);
/*!40000 ALTER TABLE `parameters` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `permission`
--

DROP TABLE IF EXISTS `permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `permission` (
  `scope` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permission`
--

LOCK TABLES `permission` WRITE;
/*!40000 ALTER TABLE `permission` DISABLE KEYS */;
INSERT INTO `permission` VALUES ('openid'),('https://www.googleapis.com/auth/userinfo.email'),('https://www.googleapis.com/auth/compute'),('https://www.googleapis.com/auth/cloud-platform'),('https://www.googleapis.com/auth/drive'),('https://www.googleapis.com/auth/appengine.admin');
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
  `tf_path` varchar(100) NOT NULL,
  `scope` text,
  `if_need_oauth` tinyint(1) NOT NULL,
  `version` varchar(100) NOT NULL,
  `deploy_type` varchar(100) NOT NULL,
  `bash_path` varchar(100) NOT NULL,
  PRIMARY KEY (`id`,`version`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `solution`
--

LOCK TABLES `solution` WRITE;
/*!40000 ALTER TABLE `solution` DISABLE KEYS */;
INSERT INTO `solution` VALUES ('baremetal','Bare Metal','https://professional-services.googlesource.com/solutions/ads-bare-metal','terraform/','https://www.googleapis.com/auth/gmail.readonly',1,'v1','Terraform',''),('clickhouse','ClickHouse','https://github.com/hellof20/clickhouse-on-gce','terraform/',NULL,0,'v1','Terraform',''),('lego','LEGO','https://professional-services.googlesource.com/solutions/ads-bi-suite','terraform/','https://www.googleapis.com/auth/gmail.readonly',1,'v1','Terraform',''),('vm-test','VM Test','https://github.com/hellof20/tf-tutorial.git','/',NULL,0,'v1','Terraform',''),('vm-test','VM Test','https://github.com/hellof20/tf-tutorial.git','',NULL,0,'v3','Bash','/');
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

-- Dump completed on 2022-10-16 15:56:50
