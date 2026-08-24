---

# 📁 Project Structure

The project follows a modular structure that separates workflow orchestration, data engineering tools, configuration and input data.

```text
ai-data-engineering/
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
│       └── customer.csv
│
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
