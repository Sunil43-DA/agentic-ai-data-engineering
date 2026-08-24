from typing import TypedDict


class AgentState(TypedDict, total=False):

    # Original input dataset
    original_file: str

    # Schema analysis result
    schema_result: dict

    # Initial data-quality result
    quality_result: dict

    # LLM reasoning and decision
    llm_reasoning: str
    llm_decision: str
    llm_reason: str

    # Cleaning result
    cleaning_result: dict

    # Post-cleaning verification result
    verification_result: dict

    database_result: dict

    retry_count: int    


    # Pipeline status
    status: str

    error_message: str

    