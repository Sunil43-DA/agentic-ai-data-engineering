import json
from unittest import result

from openai import OpenAI

from app.logger import log_event

from langgraph.graph import StateGraph, START, END

from app.agents.state import AgentState


# ==================================================
# 1. Load Configuration
# ==================================================

from app.config import (
    GROQ_API_KEY,
    GROQ_BASE_URL,
    GROQ_MODEL,
    INPUT_FILE,
    CLEANED_FILE,
    MAX_RETRIES
)
from app.tools.database_tool import validate_customer_database


# ==================================================
# 2. Create Groq Client
# ==================================================

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url=GROQ_BASE_URL
)

# ==================================================
# 2. Schema Node
# ==================================================

def schema_node(state: AgentState):

    from app.tools.schema_tool import analyse_schema

    file_path = state["original_file"]

    try:

        result = analyse_schema(
            file_path
        )

        print("\n===== SCHEMA NODE =====")
        print(result)

        log_event(
            "schema",
            "Schema analysis completed"
        )

        # ------------------------------------------
        # Empty dataset check
        # ------------------------------------------

        if result.get("rows", 0) == 0:

            print(
                "ERROR: Dataset is empty."
            )

            log_event(
                "schema",
                "ERROR | Dataset is empty"
            )

            return {
                "schema_result": result,
                "status": "input_error",
                "error_message": (
                    "Dataset is empty. "
                    "The CSV contains no data rows."
                )
            }

        return {
            "schema_result": result,
            "status": "schema_complete"
        }

    except FileNotFoundError:

        error_message = (
            f"File not found: {file_path}"
        )

        print(
            f"ERROR: {error_message}"
        )

        log_event(
            "schema",
            f"ERROR | {error_message}"
        )

        return {
            "status": "input_error",
            "error_message": error_message
        }

    except Exception as error:

        error_message = str(error)

        print(
            f"ERROR during schema analysis: "
            f"{error_message}"
        )

        log_event(
            "schema",
            f"ERROR | {error_message}"
        )

        return {
            "status": "schema_error",
            "error_message": error_message
        }

# ==================================================
# Schema Error Router
# ==================================================

def route_after_schema(state: AgentState):

    status = state.get(
        "status",
        ""
    )

    print("\n===== SCHEMA ROUTER =====")
    print("Schema status:", status)

    if status in [
        "input_error",
        "schema_error"
    ]:

        print(
            "Schema failed. Routing to error handler."
        )

        return "error"

    print(
        "Schema successful. Routing to quality."
    )

    return "quality"

# ==================================================
# Error Handler Node
# ==================================================

def error_handler_node(state: AgentState):

    error_message = state.get(
        "error_message",
        "Unknown error"
    )

    print("\n===== ERROR HANDLER =====")
    print(
        "Pipeline stopped because of an error."
    )
    print(
        "Error:",
        error_message
    )

    return {
        "status": "failed"
    }

# ==================================================
# Quality Node
# ==================================================

def quality_node(state: AgentState):

    from app.tools.quality_tool import check_data_quality

    file_path = state.get(
        "original_file"
    )

    print("\n===== QUALITY NODE =====")

    if not file_path:

        print(
            "ERROR: No input file available for quality check."
        )

        return {
            "status": "quality_error",
            "error_message": (
                "No input file available for quality check."
            )
        }

    try:

        result = check_data_quality(
            file_path
        )

        print(result)

        log_event(
            "quality",
            "Data quality check completed"
        )

        return {
            "quality_result": result,
            "status": "quality_complete"
        }

    except Exception as error:

        print(
            f"ERROR during data-quality check: {error}"
        )

        return {
            "status": "quality_error",
            "error_message": str(error)
        }

# ==================================================
# Quality Error Router
# ==================================================

def route_after_quality_node(state: AgentState):

    status = state.get(
        "status",
        ""
    )

    print("\n===== QUALITY ERROR ROUTER =====")
    print("Quality status:", status)

    if status == "quality_error":

        print(
            "Quality check failed. "
            "Routing to error handler."
        )

        return "error"

    print(
        "Quality check successful. "
        "Routing to LLM reasoning."
    )

    return "llm_reasoning"

# ==================================================
# 5. LLM Reasoning / Decision Node
# ==================================================

def llm_reasoning_node(state: AgentState):

    quality = state.get(
        "quality_result",
        {}
    )

    prompt = f"""
You are a data engineering AI agent.

Review the following data-quality result:

{json.dumps(quality, indent=2)}

Decide what the pipeline should do next.

Return ONLY valid JSON in exactly this format:

{{
    "decision": "clean",
    "reason": "Explain why cleaning is required."
}}

Rules:

- Use "clean" if ANY data-quality problem exists.
- Use "finish" if there are NO data-quality problems.
- Do not modify the dataset.
- Do not return markdown.
- Do not return any text outside the JSON.
"""

    # --------------------------------------------------
    # Call the LLM safely
    # --------------------------------------------------

    try:

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    except Exception as error:

        print(
            f"\nERROR: LLM API call failed: {error}"
        )

        return {
            "status": "llm_error",
            "error_message": str(error)
        }

    # --------------------------------------------------
    # Read LLM response
    # --------------------------------------------------

    content = response.choices[0].message.content

    if not content:

        print(
            "\nERROR: LLM returned an empty response."
        )

        return {
            "status": "llm_error",
            "error_message": (
                "LLM returned an empty response."
            )
        }

    # --------------------------------------------------
    # Clean accidental markdown fences
    # --------------------------------------------------

    content = content.strip()

    if content.startswith("```"):

        content = content.replace(
            "```json",
            ""
        ).replace(
            "```",
            ""
        ).strip()

    # --------------------------------------------------
    # Parse JSON safely
    # --------------------------------------------------

    try:

        decision_data = json.loads(
            content
        )

    except json.JSONDecodeError as error:

        print(
            "\nERROR: LLM returned invalid JSON."
        )

        print(
            "LLM response:",
            content
        )

        return {
            "status": "llm_error",
            "error_message": (
                f"LLM did not return valid JSON: "
                f"{content}"
            )
        }

    # --------------------------------------------------
    # Extract decision and reason
    # --------------------------------------------------

    decision = decision_data.get(
    "decision"
    )

    if isinstance(decision, str):

        decision = decision.strip().lower()

    reason = decision_data.get(
        "reason"
    )

    # --------------------------------------------------
    # Validate decision
    # --------------------------------------------------

    if decision not in [
        "clean",
        "finish"
    ]:

        print(
            f"\nERROR: Invalid LLM decision: {decision}"
        )

        return {
            "status": "llm_error",
            "error_message": (
                f"Invalid LLM decision: {decision}"
            ),
            "llm_reasoning": content
        }

    # --------------------------------------------------
    # Validate reason
    # --------------------------------------------------

    if not reason:

        print(
            "\nERROR: LLM did not provide a reason."
        )

        return {
            "status": "llm_error",
            "error_message": (
                "LLM did not provide a reason."
            ),
            "llm_reasoning": content,
            "llm_decision": decision
        }

    # --------------------------------------------------
    # Successful LLM decision
    # --------------------------------------------------

    print(
        "\n===== LLM DECISION ====="
    )

    print(
        "Decision:",
        decision
    )

    print(
        "Reason:",
        reason
    )

    return {
        "llm_reasoning": content,
        "llm_decision": decision,
        "llm_reason": reason,
        "status": "llm_complete"
    }


# ==================================================
# 6. Cleaning Node
# ==================================================

def cleaning_node(state: AgentState):

    from app.tools.cleaning_tool import clean_customer_data

    result = clean_customer_data(
        state["original_file"],
        CLEANED_FILE
    )

    print("\n===== CLEANING NODE =====")
    print(result)

    log_event(
        "cleaning",
        "Data cleaning completed"
    )

    return {
        "cleaning_result": result
    }

# ==================================================
# 7. Verification Node
# ==================================================

def verification_node(state: AgentState):

    from app.tools.quality_tool import check_data_quality

    cleaned_file = CLEANED_FILE

    result = check_data_quality(
        cleaned_file
    )

    print("\n===== VERIFICATION NODE =====")
    print(result)

    log_event(
        "verification",
        "Data verification completed"
    )

    return {
        "verification_result": result
    }

# ==================================================
# Verification Router
# ==================================================

def route_after_verification(state: AgentState):

    verification = state.get(
        "verification_result",
        {}
    )

    has_remaining_issues = any(
        [
            bool(
                verification.get(
                    "missing_values"
                )
            ),

            verification.get(
                "duplicate_rows",
                0
            ) > 0,

            verification.get(
                "duplicate_customer_ids",
                0
            ) > 0,

            verification.get(
                "invalid_age_count",
                0
            ) > 0,

            verification.get(
                "invalid_email_count",
                0
            ) > 0
        ]
    )

    print("\n===== VERIFICATION ROUTER =====")

    if has_remaining_issues:

        print(
            "Remaining issues found."
        )

        return "recovery"

    print(
        "Verification passed. Dataset is clean."
    )

    return "success"

# ==================================================
# Success Node
# ==================================================

def success_node(state: AgentState):

    print("\n===== SUCCESS NODE =====")
    print(
        "Dataset successfully cleaned and verified."
    )

    log_event(
        "pipeline",
        "Pipeline completed successfully"
    )

    return {
        "status": "verified_clean"
    }

# ==================================================
# Database Node
# ==================================================

def database_node(state: AgentState):

    from app.tools.database_tool import (
        load_customers_to_database,
        validate_customer_database
    )

    cleaned_file = CLEANED_FILE

    # ==================================================
    # Load cleaned data into database
    # ==================================================

    result = load_customers_to_database(
        cleaned_file
    )

    print("\n===== DATABASE NODE =====")
    print(result)

    # ==================================================
    # Check database loading
    # ==================================================

    if result.get("status") != "success":

        print(
            "Database loading failed."
        )

        log_event(
            "database",
            "Database loading failed"
        )

        return {
            "database_result": result,
            "status": "database_error",
            "error_message": (
                "Failed to load cleaned data "
                "into database."
            )
        }

    # ==================================================
    # SQL Database Validation
    # ==================================================

    validation_result = (
        validate_customer_database()
    )

    print(
        "\n===== DATABASE SQL VALIDATION ====="
    )

    print(
        validation_result
    )

    log_event(
        "database",
        (
            "SQL validation = "
            f"{validation_result['status']}"
        )
    )

    # ==================================================
    # Check SQL Validation
    # ==================================================

    if validation_result["status"] != "valid":

        print(
            "SQL database validation failed."
        )

        log_event(
            "database",
            "SQL database validation failed"
        )

        return {
            "database_result": {
                "load_result": result,
                "validation_result": (
                    validation_result
                )
            },
            "status": "database_error",
            "error_message": (
                "SQL database validation failed."
            )
        }

    # ==================================================
    # Database Successfully Loaded and Validated
    # ==================================================

    log_event(
        "database",
        (
            f"Loaded {result['rows_loaded']} "
            "rows into customers table"
        )
    )

    return {
        "database_result": {
            "load_result": result,
            "validation_result": (
                validation_result
            )
        },
        "status": "database_loaded"
    }

# ==================================================
# Recovery Node
# ==================================================

def recovery_node(state: AgentState):

    verification = state.get(
        "verification_result",
        {}
    )

    retry_count = state.get(
        "retry_count",
        0
    )

    print("\n===== RECOVERY NODE =====")
    print("Current retry count:", retry_count)

    prompt = f"""
You are a data engineering recovery agent.

The cleaning pipeline has completed, but verification
still reports these issues:

{json.dumps(verification, indent=2)}

Current retry count: {retry_count}

Decide whether another cleaning attempt is appropriate.

Return ONLY valid JSON in this format:

{{

    "action": "retry",

    "reason": "Explain why another cleaning attempt is appropriate."

}}

Rules:

- Use "retry" if another cleaning attempt should be made.
- Use "stop" if the pipeline should stop and require human review.
- Never recommend more than 2 retries.
- Do not modify the dataset yourself.
"""

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError(
            "Recovery LLM returned an empty response."
        )

    content = content.strip()

    if content.startswith("```"):
        content = content.replace(
            "```json",
            ""
        ).replace(
            "```",
            ""
        ).strip()

    recovery_data = json.loads(content)

    action = recovery_data.get(
        "action"
    )

    reason = recovery_data.get(
        "reason"
    )

    print("\n===== RECOVERY LLM =====")
    print("Action:", action)
    print("Reason:", reason)

    log_event(
        "llm",
        f"Action = {action}"
    )

    return {
        "llm_reasoning": content,
        "status": "recovery_required"
    }
# ==================================================
#  Recovery Router
# ==================================================

def route_after_recovery(state: AgentState):

    retry_count = state.get(
        "retry_count",
        0
    )

    reasoning = state.get(
        "llm_reasoning",
        ""
    )

    print("\n===== RECOVERY ROUTER =====")
    print("Retry count:", retry_count)

    try:

        recovery_data = json.loads(
            reasoning
        )

        action = recovery_data.get(
            "action"
        )

    except (json.JSONDecodeError, TypeError):

        action = "stop"

    # Maximum 2 retries
    if (
        action == "retry"
        and retry_count < 2
    ):

        print(
            "Recovery decision: RETRY"
        )

        return "retry"

    print(
        "Recovery decision: STOP"
    )

    return "stop"
# ==================================================
# Retry Counter Node
# ==================================================

def increment_retry_node(state: AgentState):

    current_count = state.get(
        "retry_count",
        0
    )

    new_count = current_count + 1

    print("\n===== RETRY NODE =====")
    print("Retry number:", new_count)

    return {
        "retry_count": new_count,
        "status": "retrying"
    }


# ==================================================
# 8. Conditional Router
# ==================================================

def route_after_llm(state: AgentState):

    status = state.get(
        "status",
        ""
    )

    print("\n===== LLM ROUTER =====")
    print("LLM status:", status)

    # --------------------------------------------------
    # Handle LLM/API failure
    # --------------------------------------------------

    if status == "llm_error":

        print(
            "LLM processing failed."
        )

        print(
            "Routing to: error_handler"
        )

        return "error"

    # --------------------------------------------------
    # Handle successful LLM decision
    # --------------------------------------------------

    decision = state.get(
        "llm_decision"
    )

    print(
        "LLM Decision:",
        decision
    )

    if decision == "clean":

        print(
            "Routing to: cleaning"
        )

        return "cleaning"

    if decision == "finish":

        print(
            "Routing to: END"
        )

        return "end"

    # --------------------------------------------------
    # Unexpected or missing decision
    # --------------------------------------------------

    print(
        "Invalid or missing LLM decision."
    )

    return "error"


# ==================================================
# 9. Build LangGraph
# ==================================================

builder = StateGraph(
    AgentState
)


# ==================================================
# Register Nodes
# ==================================================

builder.add_node(
    "schema",
    schema_node
)

builder.add_node(
    "quality",
    quality_node
)

builder.add_node(
    "llm_reasoning",
    llm_reasoning_node
)

builder.add_node(
    "cleaning",
    cleaning_node
)

builder.add_node(
    "verification",
    verification_node
)

builder.add_node(
    "success",
    success_node
)

builder.add_node(
    "database",
    database_node
)

builder.add_node(
    "recovery",
    recovery_node
)

builder.add_node(
    "retry",
    increment_retry_node
)

builder.add_node(
    "error_handler",
    error_handler_node
)

# ==================================================
# 10. Connect Nodes
# ==================================================

# START → Schema
builder.add_edge(
    START,
    "schema"
)


# Schema → Quality
builder.add_conditional_edges(
    "schema",
    route_after_schema,
    {
        "quality": "quality",
        "error": "error_handler"
    }
)


# Quality → LLM
builder.add_conditional_edges(
    "quality",
    route_after_quality_node,
    {
        "llm_reasoning": "llm_reasoning",
        "error": "error_handler"
    }
)


# LLM → Conditional Router
# LLM → Error Check
builder.add_conditional_edges(
    "llm_reasoning",
    route_after_llm,
    {
        "cleaning": "cleaning",
        "end": END,
        "error": "error_handler"
    }
)


# Cleaning → Verification
builder.add_edge(
    "cleaning",
    "verification"
)


builder.add_conditional_edges(
    "verification",
    route_after_verification,
    {
        "success": "success",
        "recovery": "recovery"
    }
)

builder.add_edge(
    "success",
    "database"
)

builder.add_edge(
    "database",
    END
)

builder.add_conditional_edges(
    "recovery",
    route_after_recovery,
    {
        "retry": "retry",
        "stop": END
    }
)

builder.add_edge(
    "retry",
    "cleaning"
)

builder.add_edge(
    "error_handler",
    END
)

# ==================================================
# 11. Compile Graph
# ==================================================

graph = builder.compile()


# ==================================================
# 12. Run Agent
# ==================================================

if __name__ == "__main__":

    initial_state: AgentState = {
    "original_file": INPUT_FILE,
    "retry_count": 0,
    "status": "starting"
}

    print("\n========================================")
    print("      AI DATA ENGINEERING AGENT")
    print("========================================")

    final_state = graph.invoke(
        initial_state
    )

    # Update final status based on verification
    verification = final_state.get(
        "verification_result",
        {}
    )

    if verification:

        has_remaining_issues = any(
            [
                bool(
                    verification.get(
                        "missing_values"
                    )
                ),

                verification.get(
                    "duplicate_rows",
                    0
                ) > 0,

                verification.get(
                    "duplicate_customer_ids",
                    0
                ) > 0,

                verification.get(
                    "invalid_age_count",
                    0
                ) > 0,

                verification.get(
                    "invalid_email_count",
                    0
                ) > 0
            ]
        )

        if has_remaining_issues:

            final_state["status"] = (
                "verification_failed"
            )

        else:

            final_state["status"] = (
                "verified_clean"
            )

    elif final_state.get(
        "llm_decision"
    ) == "finish":

        final_state["status"] = (
            "already_clean"
        )

    else:

        final_state["status"] = (
            "completed"
        )


    print("\n===== FINAL STATE =====")

    print(
        json.dumps(
            final_state,
            indent=2,
            default=str
        )
    )