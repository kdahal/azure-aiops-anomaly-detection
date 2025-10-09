# Azure AIOps Anomaly Detection ![Python](https://img.shields.io/badge/python-3.9%2B-blue) ![CI](https://github.com/kdahal/azure-aiops-anomaly-detection/workflows/CI/badge.svg)

AIOps platform for proactive anomaly detection in IT operations, starting with Azure. Automatically learns normal patterns from time-series metrics (e.g., CPU, memory) and detects deviations without manual thresholds.

![Demo GIF](anomaly_demo.gif)
*Interactive demo of anomaly detection: Synthetic data → Detection → Alert → Plot (Azure/AWS comparison).*

## Features
- **Automated Learning**: Uses Azure Anomaly Detector API for ML-based detection.
- **Proactive Prevention**: Integrates with Azure Alerts for early remediation.
- **Multi-Cloud Ready**: Extensible to AWS/GCP via abstract data pipelines.
- **Infrastructure as Code**: Bicep templates in `/infra`.

## Quick Start
1. Provision Azure resources (see `/docs/setup.md`).
2. Run detection: `python src/detect_anomalies.py` (set env vars for API).
3. Set up alerts in Azure Monitor.

### Interactive Demo
Launch the Jupyter notebook for step-by-step simulation (Azure stub, AWS mock, alerting):
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
| **Azure** | 75% | 10% | "9 deviations in 50 mins—scale VM!" |
| **AWS** | 70% | 12% | "6 bursts in 50 mins—check EC2!" |

## See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.