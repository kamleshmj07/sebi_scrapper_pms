
CREATE TABLE `Organization` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	is_active BOOL NOT NULL, 
	created_by_id INTEGER, 
	created_at DATETIME, 
	modified_by_id INTEGER, 
	modified_at DATETIME, 
	name VARCHAR(100) NOT NULL, 
	license_expiry_date DATE NOT NULL, 
	user_count INTEGER NOT NULL, 
	api_count INTEGER NOT NULL, 
	admin_name VARCHAR(100) NOT NULL, 
	admin_email VARCHAR(50) NOT NULL, 
	admin_mobile VARCHAR(20) NOT NULL, 
	has_api BOOL NOT NULL, 
	is_whitelabelled BOOL NOT NULL, 
	can_restrict_view BOOL NOT NULL, 
	can_restrict_data BOOL NOT NULL, 
	can_export BOOL NOT NULL, 
	export_fund_count INTEGER NOT NULL, 
	can_create_screener BOOL NOT NULL, 
	can_transact BOOL NOT NULL, 
	PRIMARY KEY (id)
)


CREATE INDEX `ix_Organization_modified_by_id` ON `Organization` (modified_by_id)
CREATE INDEX `ix_Organization_created_by_id` ON `Organization` (created_by_id)

CREATE TABLE `SubRole` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	is_active BOOL NOT NULL, 
	created_by_id INTEGER, 
	created_at DATETIME, 
	modified_by_id INTEGER, 
	modified_at DATETIME, 
	name VARCHAR(100) NOT NULL, 
	organization_id INTEGER, 
	can_export BOOL, 
	can_view_fund BOOL, 
	view_fund_include_list JSON COMMENT 'list of amc and/or fund', 
	view_fund_exclude_list JSON COMMENT 'list of amc and/or fund', 
	can_access_screener BOOL, 
	screener_include_list JSON COMMENT 'list of amc and/or fund', 
	screener_exclude_list JSON COMMENT 'list of amc and/or fund', 
	can_transact_fund BOOL, 
	transaction_fund_include_list JSON COMMENT 'list of amc and/or fund', 
	transaction_fund_exclude_list JSON COMMENT 'list of amc and/or fund', 
	PRIMARY KEY (id)
)


CREATE INDEX `ix_SubRole_organization_id` ON `SubRole` (organization_id)
CREATE INDEX `ix_SubRole_created_by_id` ON `SubRole` (created_by_id)
CREATE INDEX `ix_SubRole_modified_by_id` ON `SubRole` (modified_by_id)

CREATE TABLE `User` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	is_active BOOL NOT NULL, 
	created_by_id INTEGER, 
	created_at DATETIME, 
	modified_by_id INTEGER, 
	modified_at DATETIME, 
	name VARCHAR(100) NOT NULL, 
	display_name VARCHAR(100) NOT NULL, 
	email VARCHAR(50) NOT NULL, 
	mobile VARCHAR(20) NOT NULL, 
	organization_id INTEGER, 
	role_id VARCHAR(20) COMMENT 'this will be visible only to super admin.', 
	sub_role_id INTEGER COMMENT 'by default this will be visible to org-admin.', 
	designation VARCHAR(50), 
	address VARCHAR(500), 
	city VARCHAR(100), 
	state VARCHAR(100), 
	pin_code VARCHAR(10), 
	birth_date DATE NOT NULL, 
	is_locked BOOL NOT NULL, 
	last_login_at DATETIME NOT NULL, 
	referred_by_id INTEGER, 
	reference_code VARCHAR(50), 
	login_count INTEGER, 
	activation_code VARCHAR(50), 
	otp INTEGER, 
	session_id VARCHAR(50), 
	`Account_Locked_Till_Date` DATE, 
	`Salutation` VARCHAR(5) NOT NULL, 
	`First_Name` VARCHAR(20) NOT NULL, 
	`Middle_Name` VARCHAR(20) NOT NULL, 
	`Last_Name` VARCHAR(20) NOT NULL, 
	`Gender` SMALLINT NOT NULL, 
	`Marital_Status` SMALLINT NOT NULL, 
	`Secret_Question_Id` BIGINT, 
	`Hint_Word` VARCHAR(50), 
	`Secret_Answer` VARCHAR(100), 
	`Login_Failed_Attempts` SMALLINT NOT NULL, 
	PRIMARY KEY (id)
)


CREATE INDEX `ix_User_created_by_id` ON `User` (created_by_id)
CREATE INDEX `ix_User_modified_by_id` ON `User` (modified_by_id)
CREATE INDEX `ix_User_sub_role_id` ON `User` (sub_role_id)
CREATE INDEX `ix_User_organization_id` ON `User` (organization_id)

CREATE TABLE `Screener` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	is_active BOOL NOT NULL, 
	created_by_id INTEGER, 
	created_at DATETIME, 
	modified_by_id INTEGER, 
	modified_at DATETIME, 
	name VARCHAR(100), 
	query_json TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(created_by_id) REFERENCES `User` (id), 
	FOREIGN KEY(modified_by_id) REFERENCES `User` (id)
)


CREATE INDEX `ix_Screener_created_by_id` ON `Screener` (created_by_id)
CREATE INDEX `ix_Screener_modified_by_id` ON `Screener` (modified_by_id)

CREATE TABLE `FundTransaction` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	is_active BOOL NOT NULL, 
	created_by_id INTEGER, 
	created_at DATETIME, 
	modified_by_id INTEGER, 
	modified_at DATETIME, 
	amc_id INTEGER, 
	fund_id INTEGER, 
	can_transact BOOL, 
	is_pms_bazaar_distributor BOOL, 
	transaction_settings JSON, 
	PRIMARY KEY (id), 
	FOREIGN KEY(created_by_id) REFERENCES `User` (id), 
	FOREIGN KEY(modified_by_id) REFERENCES `User` (id)
)


CREATE INDEX `ix_FundTransaction_fund_id` ON `FundTransaction` (fund_id)
CREATE INDEX `ix_FundTransaction_created_by_id` ON `FundTransaction` (created_by_id)
CREATE INDEX `ix_FundTransaction_amc_id` ON `FundTransaction` (amc_id)
CREATE INDEX `ix_FundTransaction_modified_by_id` ON `FundTransaction` (modified_by_id)

CREATE TABLE `OrganizationSettings` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	is_active BOOL NOT NULL, 
	created_by_id INTEGER, 
	created_at DATETIME, 
	modified_by_id INTEGER, 
	modified_at DATETIME, 
	organization_id INTEGER, 
	white_label_settings JSON COMMENT 'has logo, app name, color schemes, fonts, disclaimer etc', 
	empanelment_settings JSON COMMENT 'list of amc and/or fund for which fund is empanelled', 
	export_settings JSON COMMENT 'list of funds that can be exported. upper limit defined by Organization.export_fund_count', 
	PRIMARY KEY (id), 
	FOREIGN KEY(created_by_id) REFERENCES `User` (id), 
	FOREIGN KEY(modified_by_id) REFERENCES `User` (id), 
	FOREIGN KEY(organization_id) REFERENCES `Organization` (id)
)


CREATE INDEX `ix_OrganizationSettings_modified_by_id` ON `OrganizationSettings` (modified_by_id)
CREATE INDEX `ix_OrganizationSettings_created_by_id` ON `OrganizationSettings` (created_by_id)
CREATE INDEX `ix_OrganizationSettings_organization_id` ON `OrganizationSettings` (organization_id)

CREATE TABLE `APIKey` (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	is_active BOOL NOT NULL, 
	created_by_id INTEGER, 
	created_at DATETIME, 
	modified_by_id INTEGER, 
	modified_at DATETIME, 
	name VARCHAR(100) NOT NULL, 
	organization_id INTEGER, 
	api_key VARCHAR(100) NOT NULL COMMENT 'this has to be stored after hashing as this is like password.', 
	sub_role_id INTEGER COMMENT 'by default this will be visible to org-admin.', 
	is_locked BOOL NOT NULL, 
	last_accessed_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(created_by_id) REFERENCES `User` (id), 
	FOREIGN KEY(modified_by_id) REFERENCES `User` (id), 
	FOREIGN KEY(organization_id) REFERENCES `Organization` (id), 
	FOREIGN KEY(sub_role_id) REFERENCES `SubRole` (id)
)


CREATE INDEX `ix_APIKey_created_by_id` ON `APIKey` (created_by_id)
CREATE INDEX `ix_APIKey_modified_by_id` ON `APIKey` (modified_by_id)
CREATE INDEX `ix_APIKey_organization_id` ON `APIKey` (organization_id)
CREATE INDEX `ix_APIKey_sub_role_id` ON `APIKey` (sub_role_id)
ALTER TABLE `User` ADD FOREIGN KEY(organization_id) REFERENCES `Organization` (id)
ALTER TABLE `Organization` ADD FOREIGN KEY(created_by_id) REFERENCES `User` (id)
ALTER TABLE `SubRole` ADD FOREIGN KEY(modified_by_id) REFERENCES `User` (id)
ALTER TABLE `User` ADD FOREIGN KEY(sub_role_id) REFERENCES `SubRole` (id)
ALTER TABLE `Organization` ADD FOREIGN KEY(modified_by_id) REFERENCES `User` (id)
ALTER TABLE `SubRole` ADD FOREIGN KEY(created_by_id) REFERENCES `User` (id)
ALTER TABLE `User` ADD FOREIGN KEY(modified_by_id) REFERENCES `User` (id)
ALTER TABLE `User` ADD FOREIGN KEY(referred_by_id) REFERENCES `User` (id)
ALTER TABLE `User` ADD FOREIGN KEY(created_by_id) REFERENCES `User` (id)
ALTER TABLE `SubRole` ADD FOREIGN KEY(organization_id) REFERENCES `Organization` (id)
