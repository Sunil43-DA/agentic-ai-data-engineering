# 🤖 AI Data Engineering Agent

### Agentic Data Quality, Cleaning & Validation Pipeline

An AI-powered data engineering agent that combines **Python, Pandas, LangGraph, Groq LLM reasoning and SQLite** to automatically analyse, assess, clean, verify and load customer data.

The system uses an **LLM-driven decision layer** to determine what the pipeline should do next, while keeping the actual data engineering operations deterministic, reproducible and auditable.

---

## 🚀 What This Project Does

The agent accepts a customer CSV file and automatically takes it through an end-to-end data engineering workflow:

```text
CSV Input
    ↓
Schema Analysis
    ↓
Data Quality Assessment
    ↓
LLM Reasoning
    ↓
Dynamic Decision
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
SQL Validation ─┘
    ↓
   END


---

## PART 2 — Architecture + End-to-End

This is the section I particularly want you to have because it makes the GitHub README look much more professional.

Add this after Part 1:

```markdown
## 🏗️ System Architecture

The application follows a state-driven LangGraph architecture.

Each node performs a specific responsibility and updates the shared `AgentState`.

```text
                              ┌─────────────────────┐
                              │     CSV INPUT       │
                              │   customer.csv      │
                              └──────────┬──────────┘
                                         │
                                         ▼
                              ┌─────────────────────┐
                              │   SCHEMA ANALYSIS   │
                              │                     │
                              │ • Rows              │
                              │ • Columns           │
                              │ • Data Types        │
                              │ • Missing Values    │
                              │ • Duplicates        │
                              └──────────┬──────────┘
                                         │
                                  Schema Router
                                         │
                         ┌───────────────┴───────────────┐
                         │                               │
                    Input Error                     Valid Schema
                         │                               │
                         ▼                               ▼
                  ┌─────────────┐              ┌─────────────────┐
                  │    ERROR    │              │ QUALITY CHECK   │
                  │   HANDLER   │              │                 │
                  └──────┬──────┘              │ • Missing       │
                         │                     │ • Duplicates    │
                         ▼                     │ • Invalid Age   │
                        END                    │ • Invalid Email │
                                               └────────┬────────┘
                                                        │
                                                 Quality Router
                                                        │
                                                        ▼
                                             ┌────────────────────┐
                                             │   LLM REASONING    │
                                             │                    │
                                             │ Analyse quality    │
                                             │ Decide next step   │
                                             └─────────┬──────────┘
                                                       │
                                                LLM Decision
                                                       │
                                      ┌────────────────┴────────────────┐
                                      │                                 │
                                   FINISH                              CLEAN
                                      │                                 │
                                      ▼                                 ▼
                                     END                       ┌────────────────┐
                                                               │    CLEANING    │
                                                               │                │
                                                               │ • Duplicates   │
                                                               │ • Invalid Age  │
                                                               │ • Missing Age  │
                                                               │ • Missing Email│
                                                               └───────┬────────┘
                                                                       │
                                                                       ▼
                                                               ┌───────────────┐
                                                               │ VERIFICATION  │
                                                               │               │
                                                               │ Re-check data │
                                                               └───────┬───────┘
                                                                       │
                                                               Verification
                                                                   Router
                                                                       │
                                                       ┌───────────────┴──────────────┐
                                                       │                              │
                                                    PASSED                         FAILED
                                                       │                              │
                                                       ▼                              ▼
                                                ┌─────────────┐                ┌─────────────┐
                                                │   SUCCESS   │                │  RECOVERY   │
                                                └──────┬──────┘                └──────┬──────┘
                                                       │                              │
                                                       │                           Retry?
                                                       │                              │
                                                       │                         ┌────┴────┐
                                                       │                         │         │
                                                       │                       Retry      Stop
                                                       │                         │         │
                                                       │                         ▼         ▼
                                                       │                    CLEANING      END
                                                       │
                                                       ▼
                                                ┌─────────────────┐
                                                │     DATABASE    │
                                                │                 │
                                                │ SQLite          │
                                                │ customers table │
                                                └────────┬────────┘
                                                         │
                                                         ▼
                                                ┌─────────────────┐
                                                │  SQL VALIDATION │
                                                │                 │
                                                │ • Row count     │
                                                │ • Missing email │
                                                │ • Invalid ages  │
                                                │ • Duplicate IDs │
                                                └────────┬────────┘
                                                         │
                                                         ▼
                                                        END


---

### PART 3 — Technical Details + Setup + Testing

Then add this as the final major section:

```markdown
## 🧩 Project Structure

```text
ai-data-engineering-agent/
│
├── app/
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── langgraph_agent.py
│   │   ├── state.py
│   │   ├── schema_agent.py
│   │   ├── llm_test.py
│   │   └── tool_call_test.py
│   │
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── schema_tool.py
│   │   ├── quality_tool.py
│   │   ├── cleaning_tool.py
│   │   └── database_tool.py
│   │
│   ├── config.py
│   ├── logger.py
│   └── __init__.py
│
├── data/
│   └── raw/
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md

