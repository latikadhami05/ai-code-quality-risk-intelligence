# AI Code Quality & Risk Intelligence

### ML-powered Review Risk & Prioritization for AI-Assisted Software Development

> **With limited human review time, where should I look first?**

AI-assisted development is increasing the amount of code produced, but human review time remains limited. This project explores how machine learning, code analysis, repository history, and change intelligence can be combined to identify **where human review attention is most valuable**.

The system analyzes code and code changes, estimates review risk, localizes high-risk areas, and prioritizes what developers should inspect first.

It is designed to **support human review, not replace it**.

---

## What This Project Does

The system evolves from basic source-code analysis into an end-to-end developer intelligence system:

**Code → Analysis → Risk Estimation → Localization → Change Intelligence → Review Prioritization → Evidence → Explanation**

It combines:

* Static code and structural metrics
* Machine learning-based risk estimation
* Explainable predictions
* AI-assisted code analysis
* Git history and code churn
* Change-aware analysis
* Review prioritization
* Review effort budgeting
* GitHub Pull Request integration
* CI/CD integration
* Evidence-grounded LLM explanations

The final system focuses on one central question:

> **Given the code and changes in front of me, what deserves the most human review attention, and why?**

---

## System Architecture

```text
                 Developer / GitHub
                        │
                        ▼
                Repository / PR
                        │
                        ▼
                 Code Ingestion
                        │
                        ▼
              Code Representation
              (AST / Static Analysis)
                        │
                        ▼
                 Feature Engine
                        │
                        ▼
                  ML Risk Engine
                        │
                        ▼
                Risk Localization
                        │
                        ▼
          Change + Historical Intelligence
                        │
                        ▼
             Review Prioritization
                        │
                        ▼
          Review Effort / Risk Budgeting
                        │
                        ▼
                 Evidence Layer
                        │
                        ▼
          Grounded LLM Explanation
                        │
                        ▼
             Developer Dashboard
                        │
                 ┌──────┴──────┐
                 ▼             ▼
             GitHub PR       CI/CD
```

---

# Project Evolution

The project is developed through **12 progressive versions**, with each version solving a deeper part of the same problem.

### V1 — Code Risk Estimator

Extracts measurable characteristics from source code and uses machine learning to estimate code risk.

### V2 — ML Improvement

Improves the modeling pipeline through model comparison, evaluation, validation, imbalance handling, and error analysis.

### V3 — Explainable Risk

Explains which measurable characteristics contribute to a risk prediction instead of presenting a black-box score.

### V4 — AI-Code Intelligence

Studies measurable differences between AI-assisted/generated code and comparable code without attempting to determine authorship.

### V5 — Multi-Dimensional Risk

Expands risk beyond a single score into multiple meaningful dimensions related to code quality and review attention.

### V6 — Code-Level Localization

Moves from repository/file-level analysis to identifying specific files, classes, and functions requiring attention.

### V7 — Change & Historical Intelligence

Uses Git history, code churn, change frequency, and repository evolution as additional signals.

### V8 — Change-Aware Review Prioritization

Focuses analysis on changed code and determines which changed areas deserve attention first.

### V9 — Review Effort & Risk Budgeting

Introduces limited review-time allocation so developers can prioritize high-value review areas under realistic time constraints.

### V10 — GitHub Pull Request Intelligence

Connects the system to real Pull Requests and analyzes changed code within an actual developer workflow.

### V11 — CI/CD Intelligence

Integrates the analysis into automated development pipelines using GitHub Actions and CI/CD workflows.

### V12 — Evidence-Grounded AI Developer Assistant

Adds an LLM explanation layer that converts structured analysis and model evidence into developer-readable reasoning.

The LLM does **not** become the source of truth.
The underlying code analysis, metrics, model outputs, history, and structured evidence remain the foundation.

---

# Core Technical Areas

### Code Intelligence

* Python AST / parsing
* Static code analysis
* Code metrics
* Feature engineering
* Change analysis

### Machine Learning

* Classification / risk estimation
* Model comparison
* Feature analysis
* Explainability
* Error analysis
* Evaluation and validation

### Software Engineering

* Git
* GitHub
* Repository analysis
* Pull Request workflows
* APIs
* Testing
* Modular architecture

### Developer Infrastructure

* GitHub Actions
* CI/CD
* Automated analysis
* Reports and artifacts
* Docker / deployment where required

### AI Layer

* Structured evidence generation
* Evidence-grounded LLM explanations
* Hallucination/unsupported-claim testing
* Developer-facing explanations

---

# Technology Stack

```text
Languages
├── Python
└── YAML / Configuration

Data & ML
├── NumPy
├── Pandas
├── Scikit-learn
└── Explainability tools

Code Intelligence
├── Python AST / Parsing
└── Static Analysis

Development
├── Git
├── GitHub
├── APIs
└── Testing

Automation
├── GitHub Actions
└── CI/CD

Application Layer
├── FastAPI
├── Dashboard / UI
└── Docker

AI
└── LLM APIs
```

Technologies are introduced only when they solve an architectural or engineering requirement.

---

# Key Research Questions

The project investigates questions such as:

* Which software characteristics are useful for estimating review risk?
* Does repository history improve risk estimation?
* Does change-aware analysis provide better review prioritization than analyzing entire repositories?
* Can risk signals help allocate limited review effort?
* Which features contribute most to predictions?
* What are the system's major failure modes and limitations?
* Can structured evidence produce reliable, grounded LLM explanations?

The project focuses on **measurable experiments and empirical evaluation**, rather than claiming that the system can prove the presence of defects.

---

# Evaluation

Evaluation evolves with the system and includes:

* Classification performance
* Precision, recall and F1
* Confusion matrices
* Cross-validation where appropriate
* Feature importance
* Error analysis
* Model comparison
* Risk localization quality
* Review prioritization effectiveness
* Risk coverage under limited review budgets
* Groundedness of AI-generated explanations

---

# Important Design Principle

> **A risk prediction does not prove that a defect exists.**

The system identifies code and changes that may deserve greater human attention based on measurable signals.

Human developers remain responsible for understanding, validating, and acting on the results.

---

# Role of the LLM

The LLM is intentionally placed **after the analytical pipeline**.

```text
Code
  ↓
Static Analysis
  ↓
Features
  ↓
ML Risk
  ↓
History / Changes
  ↓
Prioritization
  ↓
Structured Evidence
  ↓
LLM Explanation
```

This prevents the language model from becoming the primary source of technical truth.

Its role is to explain existing evidence in a useful developer-oriented format.

---

# Final Goal

The long-term goal is to build a developer intelligence system that helps answer:

> **What should I review first, and why?**

Instead of simply detecting problems, the project aims to connect:

**code quality + machine learning + software history + code changes + review constraints + developer workflows + grounded AI**

into one practical system.

---

## Project Direction

This project is intentionally designed to grow from a small ML experiment into a substantial software-engineering and AI system.

The emphasis is on:

**Learn → Understand → Build → Test → Debug → Experiment → Document → Improve**

AI tools may assist development, but generated code and explanations must be understood, tested, and validated.

---

## Author

**Latika Dhami**

B.Tech Computer Science
VMSB Uttarakhand Technical University

