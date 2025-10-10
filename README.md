# Azure AIOps Anomaly Detection ![Python](https://img.shields.io/badge/python-3.9%2B-blue) ![CI](https://github.com/kdahal/azure-aiops-anomaly-detection/workflows/CI%20Pipeline/badge.svg)

AIOps platform for proactive anomaly detection in IT operations, starting with Azure. Automatically learns normal patterns from time-series metrics (e.g., CPU, memory) and detects deviations without manual thresholds.

![Demo GIF](anomaly_demo.gif)  
*Interactive demo loop: Data gen → Live Azure detection → Plot with anomalies → Alert (multi-cloud toggles).*

## Features
- **Automated Learning**: Uses Azure Anomaly Detector API for ML-based detection.
- **Proactive Prevention**: Integrates with Azure Alerts for early remediation.
- **Multi-Cloud Ready**: Extensible to AWS/GCP via abstract data pipelines (stubs in notebook).
- **Infrastructure as Code**: Bicep templates in `/infra` for one-click deployment.

## Quick Start
1. **Provision Resources**: Follow `/docs/setup.md` for Azure CLI or deploy Bicep (`az deployment group create --resource-group aiops-rg --template-file infra/main.bicep`).
2. **Run Detection**: `python src/detect_anomalies.py` (set `ANOMALY_DETECTOR_ENDPOINT`/`_KEY` env vars for real API).
3. **Visualize**: `python src/visualize_anomalies.py` (plots actual vs. expected, saves PNG).

### Interactive Demo
Launch the Jupyter notebook for step-by-step simulation (Azure/AWS/GCP stubs, live API toggle, alerting):
- Clone: `git clone https://github.com/kdahal/azure-aiops-anomaly-detection.git`
- Install: `pip install -r requirements.txt`
- Run: `cd examples && jupyter notebook anomaly_demo.ipynb`
- Tune `anomaly_prob` and re-execute cells for "live" tweaks.

[View Notebook on GitHub](examples/anomaly_demo.ipynb)

## Architecture
```
[Azure Resources (VMs/Apps)] --> [Azure Monitor (Metrics Ingestion)] --> [Log Analytics (Storage)]
|
v
[Anomaly Detector API (ML Processing)] <--> [Azure Functions (Orchestration)]
|
v
[Alert Rules] --> [Action Groups (Email/Slack/Remediation)]
```

Multi-Cloud Comparison (from Notebook):
| Cloud | Baseline | Anomaly Rate | Sample Alert |
|-------|----------|--------------|--------------|
| **Azure** | 75% | 10% | "2 deviations in 50 mins—scale VM!" |
| **AWS** | 70% | 12% | "7 bursts in 50 mins—check EC2!" |
| **GCP** | 72% | 11% | "6 surges in 50 mins—monitor instance!" |

## See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.