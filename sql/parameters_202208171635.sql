INSERT INTO ads.parameters (id,name,solution_id,description,example,show_on_ui,`type`,default_value) VALUES
	 ('adh_audience_dataset_id','adh_audience_dataset_id','lego','s','adh_audience',0,'string','adh_audience'),
	 ('adh_branding_dataset_id','adh_branding_dataset_id','lego','The id of adh branding dataset','adh_branding',0,'string','adh_branding'),
	 ('adh_customer_id','adh_customer_id','lego','Ads Data Hub customer id','123',1,'string',NULL),
	 ('adh_lego_dataset_id','adh_lego_dataset_id','lego','The id of adh lego dataset','adh_apps_data',0,'string','adh_apps_data'),
	 ('ads_report_dataset_id','ads_report_dataset_id','lego','The id of general lego report dataset','ads_reports_data_v4',0,'string','ads_reports_data_v4'),
	 ('appengine_location','appengine_location','baremetal',' ',' ',0,'string','us-central'),
	 ('bucket','Bucket Name','baremetal','GCS bucket to store input data.','my-bucket-id',1,'string',NULL),
	 ('client_id','Client ID','baremetal','Client ID','xxxxx',1,'string',NULL),
	 ('client_id','Client ID','lego','Client ID','xxxxx',1,'string',NULL),
	 ('client_secret','Client Secret','baremetal','Client Secret','xxxxxx',1,'string',NULL);
INSERT INTO ads.parameters (id,name,solution_id,description,example,show_on_ui,`type`,default_value) VALUES
	 ('client_secret','Client Secret','lego','Client Secret','xxxxx',1,'string',NULL),
	 ('config_dataset_id','config_dataset_id','lego','The id of config dataset','ads_report_configs',0,'string','ads_report_configs'),
	 ('developer_token','developer_token','baremetal',' ','0qxFO_azpn5Sn4_QCeWt7g',1,'string',NULL),
	 ('developer_token','developer_token','lego','Google Ads developer token','0qxFO_azpn5Sn4_QCeWt7g',1,'string',NULL),
	 ('fx_rate_spreadsheet_id','fx_rate_spreadsheet_id','lego','The google spreadsheet id','1K438j6BExEnx0emeg8YD6HeYRhnpI9wlH1yJ_-L2Xhk',1,'string',NULL),
	 ('gcs_location','gcs_location','baremetal',' ',' ',0,'string','US'),
	 ('login_customer_id','login_customer_id','baremetal','Ten digit customer id','1234567890',1,'string',NULL),
	 ('mcc_ids','mcc_ids','lego','MCC Ids separated by \\\\n','123456789\\\\n456789123',1,'string',NULL),
	 ('namespace','namespace','lego','The lego namespace','lego',0,'string','lego'),
	 ('network','GCP Network','vm-test','GCP Network','default',1,'string',NULL);
INSERT INTO ads.parameters (id,name,solution_id,description,example,show_on_ui,`type`,default_value) VALUES
	 ('notification_email','notification_email','baremetal','"[Optional]A list of email addresses separated by comma.
Daily summary stats will be sent by email if not empty"',' ',1,'string',NULL),
	 ('project_id','Project ID','baremetal','GCP Project ID','pangu-test-1',1,'string',NULL),
	 ('project_id','Project ID','lego','GCP Project ID','lego-chjerry-lab',1,'string',NULL),
	 ('project_id','Project ID','vm-test','GCP Project ID','pangu-test-1',1,'string',NULL),
	 ('refresh_token','refresh_token','baremetal',' ',' ',1,'string',NULL),
	 ('region','region','baremetal',' ',' ',0,'string','us-central1'),
	 ('region','region','lego','GCP region','us-central1',0,'string','us-central1'),
	 ('storage_location','storage_location','lego','GCS storage Location','US',0,'string','US'),
	 ('tentacles_outbound','tentacles_outbound','lego','Hard to explain, tech infra value.','outbound/',0,'string','outbound/'),
	 ('time_zone','time_zone','baremetal',' ',' ',0,'string','Asia/Shanghai');
INSERT INTO ads.parameters (id,name,solution_id,description,example,show_on_ui,`type`,default_value) VALUES
	 ('timezone','timezone','lego','The timezone for cloud scheduler setup.','Asia/Shanghai',0,'string','Asia/Shanghai'),
	 ('zone','zone','baremetal',' ',' ',0,'string','us-central1-c');
