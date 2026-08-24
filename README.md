# 🤖 AI Data Engineering Agent

### Agentic Data Quality, Cleaning, Validation & Database Pipeline

[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Agent%20Workflow-orange)](https://www.langchain.com/langgraph)
[![Groq](https://img.shields.io/badge/Groq-LLM-purple)](https://groq.com/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Engineering-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](#license)

An AI-powered data engineering agent that combines **Python, Pandas, LangGraph, Groq LLM reasoning and SQLite** to automatically analyse, assess, clean, verify and load customer data.

The project demonstrates how **agentic AI can be integrated into a practical data engineering workflow**, where the LLM is responsible for reasoning and decision-making while deterministic Python tools perform the actual data processing and validation.

---

# 📌 Table of Contents

- [Project Overview](#-project-overview)
- [Why This Project](#-why-this-project)
- [Project Objectives](#-project-objectives)
- [Key Features](#-key-features)
- [Architecture](#-architecture)
- [End-to-End Workflow](#-end-to-end-workflow)
- [Agent Nodes](#-agent-nodes)
- [LLM Decision-Making](#-llm-decision-making)
- [Data Quality Checks](#-data-quality-checks)
- [Data Cleaning](#-data-cleaning)
- [Verification](#-verification)
- [Recovery and Retry](#-recovery-and-retry)
- [Error Handling](#-error-handling)
- [Database Integration](#-database-integration)
- [SQL Validation](#-sql-validation)
- [Logging and Audit Trail](#-logging-and-audit-trail)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Configuration](#-configuration)
- [Installation](#-installation)
- [Running the Agent](#-running-the-agent)
- [Testing](#-testing)
- [Example Execution](#-example-execution)
- [Design Principles](#-design-principles)
- [Security](#-security)
- [Current Limitations](#-current-limitations)
- [Future Enhancements](#-future-enhancements)
- [Production Recommendations](#-production-recommendations)
- [Learning Outcomes](#-learning-outcomes)
- [Conclusion](#-conclusion)
- [Author](#-author)
- [Repository](#-repository)

---

# 🚀 Project Overview

Traditional data engineering pipelines are often designed as fixed sequences of operations:

```text
Extract
   ↓
Transform
   ↓
Validate
   ↓
Load
