# AI Code Quality & Risk Intelligence

### ML-powered Review Risk & Prioritization for AI-Assisted Software Development

> **With limited human review time, where should I look first?**

AI-assisted development is increasing the amount of code produced, while human review time remains limited.

**AI Code Quality & Risk Intelligence** is an end-to-end AI and software-engineering system designed to analyze source code, understand code and change characteristics, estimate review risk, localize areas requiring attention, and help developers prioritize limited human review effort.

The system is designed to **support human review, not replace it**.

---

## What This Project Does

The project evolves from source-code analysis into a developer intelligence system that connects:

**Code → Analysis → Risk Estimation → Localization → Change Intelligence → Review Prioritization → Evidence → Explanation**

It combines:

- Static code and structural analysis
- Machine learning-based risk estimation
- Explainable predictions
- AI-assisted code analysis
- Git history and code churn
- Change-aware analysis
- Review prioritization
- Review effort budgeting
- GitHub Pull Request intelligence
- CI/CD integration
- Evidence-grounded LLM explanations

The central question is:

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
