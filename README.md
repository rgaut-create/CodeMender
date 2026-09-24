# 🛡️ CodeMender CI/CD Automated Security Remediation Demo

This repository demonstrates **CodeMender**—Google's autonomous AI security engineer—integrated directly into a GitHub Actions CI/CD pipeline using **Workload Identity Federation (WIF)** for keyless authentication to Google Cloud Vertex AI.

---

## 📚 Customer Presentation Decks & Guides

All customer presentation scripts, PowerPoint slides, PDFs, and architecture flowcharts are available in the [`docs/`](./docs) folder:

| Asset | Format | Direct Link | Description |
| :--- | :--- | :--- | :--- |
| **PowerPoint Slide Deck** | `.pptx` | [`docs/CodeMender_Architecture_and_Overview.pptx`](./docs/CodeMender_Architecture_and_Overview.pptx) | Editable PowerPoint presentation covering architecture & ROI |
| **Customer Presentation Script** | `.md` / `.pdf` | [`docs/CodeMender_Customer_Presentation_Guide.md`](./docs/CodeMender_Customer_Presentation_Guide.md) / [`PDF`](./docs/CodeMender_Customer_Presentation_Guide.pdf) | Step-by-step click-by-click script for presenting to customers |
| **Architecture Slide Deck** | `.md` / `.pdf` | [`docs/CodeMender_Architecture_Presentation.md`](./docs/CodeMender_Architecture_Presentation.md) / [`PDF`](./docs/CodeMender_Architecture_Presentation.pdf) | Technical architecture & keyless WIF security design slides |
| **CI/CD Flowchart** | `.md` | [`docs/CodeMender_CICD_Flow_Diagram.md`](./docs/CodeMender_CICD_Flow_Diagram.md) | Mermaid workflow diagram of CodeMender pipeline execution |

---

## 🚀 Live Demo Quick Links

1. **Vulnerable Application Code**: [`app.py`](./app.py)
2. **GitHub Security Alerts**: [Security $\rightarrow$ Code scanning](https://github.com/rgaut-create/CodeMender/security/code-scanning)
3. **CI/CD Pipeline Runs**: [Actions $\rightarrow$ Workflows](https://github.com/rgaut-create/CodeMender/actions)
4. **Automated Remediation PR**: [Pull Requests $\rightarrow$ PR #1](https://github.com/rgaut-create/CodeMender/pull/1)

---

## 🛠️ Application & Security Features

- **Vulnerable Endpoints in `app.py`**:
  - `/api/user/search`: SQL Injection (`CWE-89`)
  - `/api/documents/<id>`: Insecure Direct Object Reference / IDOR (`CWE-639`)
  - `/api/tools/ping`: Remote OS Command Execution (`CWE-78`)
- **Pytest Suite**: [`test_app.py`](./test_app.py) for regression testing pre- and post-patching.
- **Keyless Authentication**: Google Cloud Workload Identity Federation (WIF) OIDC token exchange.
- **SARIF 2.1.0 Export**: Direct upload into GitHub Code Scanning security hub.
