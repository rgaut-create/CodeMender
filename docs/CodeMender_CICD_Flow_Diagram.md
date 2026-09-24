# CodeMender CI/CD End-to-End Flow Diagrams

This document contains visual **flowcharts and sequence diagrams** illustrating the end-to-end integration of **Google CodeMender** within a **GitHub Actions CI/CD pipeline**.

---

## 1. End-to-End High-Level Architecture Flow

```mermaid
flowchart TD
    subgraph DEV ["1. Developer Workflow"]
        CODE["Developer Commits Vulnerable Code (app.py)"] --> PR["Create Pull Request / Commit Push"]
    end

    subgraph GHA ["2. GitHub Actions CI/CD Pipeline"]
        PR --> TRIGGER["Trigger Workflow (.github/workflows/codemender-cicd.yml)"]
        TRIGGER --> AUTH["Step 1: OIDC Auth via Workload Identity Federation (WIF)"]
        AUTH --> SCAN["Step 2: Run Vulnerability Discovery (cm find app.py)"]
        SCAN --> SARIF["Step 3: Export Findings to SARIF & Upload to GitHub Security"]
        SARIF --> VERIFY["Step 4: Execute Exploit Proof-of-Concept Verification (cm verify)"]
        VERIFY --> FIX["Step 5: Generate & Validate Patch (cm fix + pytest)"]
        FIX --> AUTOPR["Step 6: Submit Automated Remediation Pull Request"]
    end

    subgraph GCP ["3. Google Cloud Platform & CodeMender Service"]
        AUTH <-->|Keyless Token Exchange| WIF["GCP Workload Identity Pool"]
        SCAN <-->|Vulnerability Classifier API| CM_ENGINE["CodeMender Agent Service (Gemini 3.5 Flash)"]
        VERIFY <-->|Exploit Generation & Execution| CM_ENGINE
        FIX <-->|Patch Reasoning & Structured Thinking| CM_ENGINE
    end

    subgraph GH_UI ["4. GitHub Security & PR Interface"]
        SARIF -->|Display Vulnerability Alerts| GH_SEC["GitHub Security -> Code Scanning Alerts"]
        AUTOPR -->|Review & Merge Patch| GH_PR["GitHub Pull Requests -> 🛡️ [CodeMender] Auto-Fix PR"]
    end

    style DEV fill:#f9f9f9,stroke:#333,stroke-width:1px
    style GHA fill:#e1f5fe,stroke:#0288d1,stroke-width:2px
    style GCP fill:#e8f5e9,stroke:#388e3c,stroke-width:2px
    style GH_UI fill:#fff3e0,stroke:#f57c00,stroke-width:2px
```

---

## 2. Sequence Diagram: Authentication & Execution Loop

```mermaid
sequenceDiagram
    autonumber
    actor Dev as Developer
    participant GHA as GitHub Actions Runner
    participant WIF as GCP Workload Identity
    participant CM_CLI as CodeMender CLI (cm)
    participant CM_SVC as CodeMender Backend (Gemini)
    participant GH_SEC as GitHub Code Scanning

    Dev->>GHA: Push Commit / Create PR with app.py
    GHA->>WIF: Request OIDC token exchange (google-github-actions/auth)
    WIF-->>GHA: Return temporary GCP OAuth Token
    
    Note over GHA, CM_CLI: Initialize CodeMender Environment
    GHA->>CM_CLI: Run `cm find app.py`
    CM_CLI->>CM_SVC: Query vulnerability scanner API
    CM_SVC-->>CM_CLI: Return findings (SQLi, IDOR, RCE)
    
    GHA->>CM_CLI: Run `cm report --format sarif`
    CM_CLI-->>GHA: Output `codemender-findings.sarif`
    GHA->>GH_SEC: Upload SARIF report (codeql-action/upload-sarif)

    Note over GHA, CM_SVC: Autonomous Verification & Remediation
    GHA->>CM_CLI: Run `cm verify <FINDING_ID>`
    CM_CLI->>CM_SVC: Execute exploit proof-of-concept in sandbox
    CM_SVC-->>CM_CLI: Exploit confirmed (Zero False Positives)

    GHA->>CM_CLI: Run `cm fix <FINDING_ID>`
    CM_CLI->>CM_SVC: Generate patch & validate against `pytest`
    CM_SVC-->>CM_CLI: Verified diff applied to `app.py`

    GHA->>Dev: Create automated Fix PR with clean git diff
```

---

## 3. Pipeline Execution Stages & Decision Tree

```mermaid
flowchart LR
    A["Event Trigger (PR / Push / Manual)"] --> B{"WIF Auth Valid?"}
    B -- No --> C["Fail Workflow (Auth Error)"]
    B -- Yes --> D["Run CodeMender Scan (cm find)"]
    
    D --> E{"Vulnerabilities Found?"}
    E -- No --> F["Upload Clean SARIF & Pass Build"]
    E -- Yes --> G["Export SARIF to GitHub Security Tab"]
    
    G --> H{"Auto-Fix Enabled?"}
    H -- No --> I["Report Alerts & Complete Job"]
    H -- Yes --> J["Run cm verify (Exploit Validation)"]
    
    J --> K["Run cm fix (Patch Generation)"]
    K --> L["Execute Pytest Suite"]
    
    L -- Test Fails --> M["Backtrack & Retry Patch"]
    L -- Test Passes --> N["Open Automated Remediation Pull Request"]

    style A fill:#e3f2fd,stroke:#1565c0
    style N fill:#c8e6c9,stroke:#2e7d32
    style C fill:#ffcdd2,stroke:#c62828
```

---

## 4. Live Customer Demonstration Walkthrough

When presenting this diagram to a customer:

| Stage | What Happens | Customer Value Proposition |
| :--- | :--- | :--- |
| **1. Commit & Trigger** | Developer opens a PR containing vulnerable code (`app.py`). | Seamless shift-left scanning inside standard developer workflows. |
| **2. Keyless Auth (WIF)** | Runner exchanges GitHub OIDC token for short-lived GCP token. | Zero credential leaks: No static API keys stored in GitHub. |
| **3. Scanning & SARIF** | `cm find` scans code and uploads standard SARIF alerts to GitHub. | Fits into existing Security Operation dashboards (GitHub Security). |
| **4. Exploit Verification** | `cm verify` runs proof-of-concept exploits in an isolated sandbox. | **Zero False Positives**: Only confirmed vulnerabilities trigger fixes. |
| **5. Patch & PR Generation**| `cm fix` generates a diff and tests it against `pytest` before opening a PR. | **Autonomous Remediation**: Developers review and merge complete fixes. |
