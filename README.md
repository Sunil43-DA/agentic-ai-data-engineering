# 🤖 AI Data Engineering Agent

### Agentic Data Quality, Cleaning & Validation Pipeline

<p align="center">

<img src="https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white">
<img src="https://img.shields.io/badge/LangGraph-Agentic%20Workflow-orange">
<img src="https://img.shields.io/badge/Groq-LLM-purple">
<img src="https://img.shields.io/badge/Pandas-Data%20Engineering-150458?logo=pandas&logoColor=white">
<img src="https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite&logoColor=white">
<img src="https://img.shields.io/badge/AI-Data%20Engineering-success">

</p>

---

## 🚀 Overview

> **An agentic data engineering pipeline that uses LLM reasoning to make workflow decisions while deterministic Python tools perform data processing, validation and database operations.**

The **AI Data Engineering Agent** is an AI-powered data engineering workflow that automatically analyses, validates, cleans, verifies and stores customer data.

The project combines traditional data engineering techniques with **Large Language Model (LLM) reasoning** and **LangGraph workflow orchestration**.

The system is designed around a simple principle:

> **Use AI for reasoning and deterministic engineering tools for execution.**

The LLM analyses the results of data-quality checks and decides what the pipeline should do next. Python-based tools then perform the actual data processing, cleaning, verification and database operations.

---

# 🎯 What Does This Project Do?

The agent takes a customer CSV file and processes it through an end-to-end workflow:

```text
CSV Input
    ↓
Schema Analysis
    ↓
Data Quality Assessment
    ↓
LLM Reasoning
    ↓
Decision
    ├── Finish
    │
    └── Clean
          ↓
       Cleaning
          ↓
      Verification
          ↓
    ┌─────┴─────┐
    │           │
  Passed      Failed
    │           │
    ↓           ↓
 Success     Recovery
    │           │
    ↓         Retry
 Database      │
    ↓           │
SQL Validation ┘
    ↓
   END
```
---

# ✨ Key Features

| Feature | Description |
|---|---|
| 🔍 Schema Analysis | Analyses dataset structure, columns, data types and missing values |
| 🧪 Data Quality Assessment | Detects missing values, duplicates and invalid records |
| 🧠 LLM Reasoning | Uses an LLM to determine the appropriate next processing step |
| 🔀 Conditional Routing | Uses LangGraph to route the workflow based on processing results |
| 🧹 Automated Cleaning | Cleans detected data-quality issues using deterministic Python logic |
| ✅ Data Verification | Re-validates the dataset after cleaning |
| ♻️ Recovery & Retry | Provides controlled recovery when verification fails |
| 🚨 Error Handling | Handles missing, empty and malformed input files |
| 📝 Audit Logging | Records important pipeline events and processing stages |
| 🗄️ SQLite Database | Stores validated customer records |
| 🔎 SQL Validation | Performs an additional validation after database loading |
| 🔐 Secure Configuration | Keeps API credentials outside the source code |

---

# 🧠 Why Use an LLM?

The LLM is **not responsible for directly modifying the data**.

Instead, the architecture separates **reasoning** from **execution**.

```text
                ┌───────────────────┐
                │       LLM         │
                │                   │
                │ Analyse Results   │
                │ Reason            │
                │ Make Decision     │
                └─────────┬─────────┘
                          │
                    Decision Only
                          │
                          ▼
                ┌───────────────────┐
                │    LangGraph      │
                │      Router       │
                └─────────┬─────────┘
                          │
                          ▼
              ┌────────────────────────┐
              │ Deterministic Python   │
              │ Data Engineering Tools │
              │                        │
              │ Schema                 │
              │ Quality                │
              │ Cleaning               │
              │ Verification           │
              │ Database               │
              └────────────────────────┘
