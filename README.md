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
