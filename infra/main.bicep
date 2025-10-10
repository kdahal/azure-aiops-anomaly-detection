param location string = resourceGroup().location
param anomalyDetectorName string = 'anomalydetector-${uniqueString(resourceGroup().id)}'
param logAnalyticsName string = 'aiops-logs-${uniqueString(resourceGroup().id)}'

@description('Anomaly Detector SKU (S0 for production)')
@allowed(['F0', 'S0'])
param anomalySku string = 'S0'

@description('Log Analytics SKU')
@allowed(['CapacityReservation', 'Free', 'LACluster', 'PerGB2018', 'PerNode', 'Premium', 'Standalone', 'Standard'])
param logSku string = 'PerGB2018'

@description('Retention in days for logs')
@minValue(30)
@maxValue(730)
param retentionDays int = 30

// Anomaly Detector Resource (ML Engine)
resource anomalyDetector 'Microsoft.CognitiveServices/accounts@2023-05-01' = {
  name: anomalyDetectorName
  location: location
  sku: {
    name: anomalySku
  }
  kind: 'AnomalyDetector'
  properties: {
    customSubDomainName: anomalyDetectorName
  }
}

// Log Analytics Workspace (Data Storage)
resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2020-08-01' = {
  name: logAnalyticsName
  location: location
  properties: {
    sku: {  // Fixed: Object format for WorkspaceSku (no BCP036)
      name: logSku
    }
    retentionInDays: retentionDays
    workspaceCapping: {
      dailyQuotaGb: -1  // Unlimited
    }
  }
}

// Output for Integration (use in scripts/env vars)
output anomalyDetectorEndpoint string = anomalyDetector.properties.endpoint
// output anomalyDetectorKey string = anomalyDetector.listKeys().key1  // Commented: Avoid secret output
output logAnalyticsId string = logAnalytics.id
output logAnalyticsWorkspaceName string = logAnalyticsName
