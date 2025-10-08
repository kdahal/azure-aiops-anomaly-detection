param location string = resourceGroup().location
param anomalyDetectorName string = 'anomalydetector-${uniqueString(resourceGroup().id)}'

// Resource Group (if needed; assume aiops-rg exists)
// var rgName = 'aiops-rg'

// Anomaly Detector Resource
resource anomalyDetector 'Microsoft.CognitiveServices/accounts@2023-05-01' = {
  name: anomalyDetectorName
  location: location
  sku: {
    name: 'S0'
  }
  kind: 'AnomalyDetector'
  properties: {
    customSubDomainName: anomalyDetectorName
  }
}

// Log Analytics Workspace for Data Storage
resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2020-08-01' = {
  name: 'aiops-logs-${uniqueString(resourceGroup().id)}'
  location: location
  properties: {
    sku: 'PerGB2018'
    retentionInDays: 30
    workspaceCapping: {
      dailyQuotaGb: -1
    }
  }
}

// Output for API Endpoint and Key
output anomalyDetectorEndpoint string = anomalyDetector.properties.endpoint
output logAnalyticsId string = logAnalytics.id
