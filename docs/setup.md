# Azure Setup Guide

## Provision Resources
Use Azure CLI:
```
az group create --name aiops-rg --location eastus
az cognitiveservices account create --name anomalydetector01 --resource-group aiops-rg --kind AnomalyDetector --sku S0 --location eastus
```

## Data Ingestion
Enable Azure Monitor agents on your resources.
