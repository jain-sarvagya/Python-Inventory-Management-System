#!/bin/bash

# === CONFIGURATION ===
RESOURCE_GROUP="flask-rg-test"           # Resource group name
LOCATION="northeurope"                   # Azure region
SQL_SERVER_NAME="ims-sql-$RANDOM"        # Unique SQL server name
SQL_DB_NAME="imsdb"                      # Database name
ADMIN_USER="rootadmin"               # SQL Admin username
ADMIN_PASSWORD="P@#sword01"   # SQL Admin password (must meet complexity)

# === EXECUTION ===

echo "Creating SQL Server: $SQL_SERVER_NAME"
az sql server create \
  --name $SQL_SERVER_NAME \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --admin-user $ADMIN_USER \
  --admin-password $ADMIN_PASSWORD

echo "Allowing Azure services to access the SQL Server"
az sql server firewall-rule create \
  --resource-group $RESOURCE_GROUP \
  --server $SQL_SERVER_NAME \
  --name AllowAzureServices \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0

echo "Creating SQL Database: $SQL_DB_NAME"
az sql db create \
  --resource-group $RESOURCE_GROUP \
  --server $SQL_SERVER_NAME \
  --name $SQL_DB_NAME \
  --service-objective Basic

echo "✅ Done!"
echo "➡️  Server Name: $SQL_SERVER_NAME.database.windows.net"
echo "➡️  Database Name: $SQL_DB_NAME"
