# AI Data Engineering Agent

## Overview

This project is an AI-powered data engineering agent designed to automatically analyse, validate, clean, verify and store customer data.

The system combines traditional data engineering techniques with Large Language Model (LLM) reasoning and LangGraph-based workflow orchestration.

The agent can identify data-quality problems, decide whether cleaning is required, execute cleaning operations, verify the cleaned dataset, recover from failures, retry processing when necessary, maintain an audit log and load the validated data into a SQLite database.

---

## Project Objectives

The main objectives of the project are:

- Analyse the structure of incoming CSV data.
- Detect common data-quality problems.
- Use an LLM to determine the appropriate next processing step.
- Automatically clean poor-quality data.
- Verify the cleaned dataset.
- Handle input and processing errors.
- Support retry and recovery logic.
- Maintain an audit trail.
- Store validated data in a database.
- Perform SQL-based validation after database loading.

---

## Architecture

The overall workflow is:

CSV Input
↓
Schema Analysis
↓
Data Quality Assessment
↓
LLM Reasoning
↓
Conditional Routing
↓
Data Cleaning
↓
Verification
↓
Recovery / Retry if Required
↓
Success
↓
SQLite Database
↓
SQL Validation
↓
End

---

## Technologies Used

### Programming

- Python
- Pandas
- SQLite

### AI / Agent Framework

- LangGraph
- Groq API
- OpenAI-compatible Python client

### Data Engineering

- CSV processing
- Data-quality validation
- Data cleaning
- SQL validation
- Database loading

### Configuration and Reliability

- python-dotenv
- Python logging
- Retry and recovery handling
- Error handling

---

## Project Structure

```text
ai-data-engineering-agent/
│
├── app/
│   ├── agents/
│   │   ├── langgraph_agent.py
│   │   └── state.py
│   │
│   ├── tools/
│   │   ├── schema_tool.py
│   │   ├── quality_tool.py
│   │   ├── cleaning_tool.py
│   │   └── database_tool.py
│   │
│   ├── config.py
│   ├── logger.py
│   └── ...
│
├── data/
│   ├── raw/
│   ├── clean/
│   └── database/
│
├── logs/
│   └── agent.log
│
├── .env
├── .gitignore
└── README.md