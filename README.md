# CodeMender End-to-End Vulnerable Python Demo App

This repository provides an **end-to-end, runnable demo app** for showcasing **Google CodeMender** integration in GitHub Actions CI/CD pipelines.

---

## 📁 Repository Structure

```
├── app.py                      # Flask REST API containing 3 vulnerabilities (SQLi, IDOR, RCE)
├── test_app.py                 # Pytest suite verifying functional behavior
├── requirements.txt            # Python dependencies (flask, pytest)
├── push_to_github.sh           # Helper script to initialize git and push to your GitHub repo
├── .codemender/
│   └── config.yaml             # CodeMender CLI non-interactive CI/CD settings
└── .github/
    └── workflows/
        └── codemender-cicd.yml # Production-ready GitHub Actions workflow
```

---

## 🔒 Vulnerabilities Included in `app.py`

1. **SQL Injection (SQLi)**: `/api/user/search?username=' OR 1=1 --`
   * Vulnerable string concatenation query.
   * **CodeMender Fix**: Replaces string formatting with parameterized SQLite placeholders `(username,)`.

2. **Insecure Direct Object Reference (IDOR)**: `/api/documents/<doc_id>`
   * Missing ownership check (`owner_id == current_user_id`).
   * **CodeMender Fix**: Adds ownership validation check against `X-User-ID` header.

3. **Command Injection (RCE)**: `/api/tools/ping` (POST `{"host": "127.0.0.1; cat /etc/passwd"}`)
   * Direct `os.system` invocation.
   * **CodeMender Fix**: Uses `subprocess.run` with list arguments (`shell=False`) or input sanitization.

---

## 🚀 Quick Start: Pushing to Your GitHub Repository

1. Open your terminal and navigate to this folder:
   ```bash
   cd /usr/local/google/home/rgaut/.gemini/jetski/brain/ef1223b3-fe9e-4d7c-ab14-a41210d6b62a/demo-codemender-python-app
   ```

2. Run the push helper script with your GitHub repository URL:
   ```bash
   ./push_to_github.sh https://github.com/<YOUR_GITHUB_ORG_OR_USER>/<YOUR_REPO_NAME>.git
   ```

3. Ensure GitHub Secrets are set under **Settings -> Secrets and variables -> Actions**:
   * `WIF_PROVIDER`: Your GCP Workload Identity Provider ID.
   * `WIF_SERVICE_ACCOUNT`: Your GCP Service Account email.
   * `GCP_PROJECT_ID`: Your GCP Project ID.

---

## 🎬 How to Perform the Live Customer Demo

1. **Trigger Scan**: Open a Pull Request or push a commit to `main`.
2. **Watch Pipeline**: Observe the GitHub Actions workflow running:
   - `cm find` detects all 3 vulnerabilities in `app.py`.
   - `cm report --format sarif` posts alerts directly into **GitHub Security -> Code Scanning**.
3. **Automated Remediation**: CodeMender runs `cm verify` (exploit validation) and `cm fix` (patch generation).
4. **Fix Pull Request**: CodeMender automatically creates a new PR titled `🛡️ [CodeMender] Automated Vulnerability Remediation` containing clean, verified patches for `app.py`.
