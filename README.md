# Azure AIOps Anomaly Detection

AIOps platform for proactive anomaly detection in IT operations, starting with Azure. Automatically learns normal patterns from time-series metrics (e.g., CPU, memory) and detects deviations without manual thresholds.

## Features
- **Automated Learning**: Uses Azure Anomaly Detector API for ML-based detection.
- **Proactive Prevention**: Integrates with Azure Alerts for early remediation.
- **Multi-Cloud Ready**: Extensible to AWS/GCP via abstract data pipelines.
- **Infrastructure as Code**: Bicep templates in /infra.

## Quick Start
1. Provision Azure resources (see /docs/setup.md).
2. Run detection: `python src/detect_anomalies.py`
3. Set up alerts in Azure Monitor.

## Architecture
- Data: Azure Monitor + Log Analytics
- ML: Azure Anomaly Detector
- Orchestration: Azure Functions

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
