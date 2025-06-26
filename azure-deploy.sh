#!/bin/bash

# Config
APP_NAME="ims-app-$RANDOM"
RESOURCE_GROUP="rg"
PLAN_NAME="app-flask-ims"
LOCATION="centralus"

echo "Logging in to Azure..."
az login

echo "Creating Resource Group..."
az group create --name $RESOURCE_GROUP --location $LOCATION

echo "Creating App Service Plan..."
az appservice plan create --name $PLAN_NAME --resource-group $RESOURCE_GROUP --sku F1 --is-linux

echo "Creating Web App ($APP_NAME)..."
az webapp create \
  --resource-group $RESOURCE_GROUP \
  --plan $PLAN_NAME \
  --name $APP_NAME \
  --runtime "PYTHON|3.11" \
  --deployment-local-git

echo "Fetching deployment Git URL..."
GIT_URL=$(az webapp deployment source config-local-git --name $APP_NAME --resource-group $RESOURCE_GROUP --query url --output tsv)

echo "Deployment Git URL: $GIT_URL"

echo "Setting up Git for deployment..."
git init
git remote add azure $GIT_URL
git add .
git commit -m "Initial commit for Azure deployment"

echo "Pushing to Azure remote..."
git push azure master

echo "Opening app in browser..."
az webapp browse --name $APP_NAME --resource-group $RESOURCE_GROUP
