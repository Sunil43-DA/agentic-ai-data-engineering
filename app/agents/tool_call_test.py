import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from app.tools.schema_tool import analyse_schema
from app.tools.quality_tool import check_data_quality
from app.tools.cleaning_tool import clean_customer_data
from app.agents.state import AgentState


# --------------------------------------------------
# 1. Load environment variables
# --------------------------------------------------

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)


# --------------------------------------------------
# 2. Define tools available to the LLM
# --------------------------------------------------

tools = [
    {
        "type": "function",
        "function": {
            "name": "analyse_schema",
            "description": (
                "Analyse the structure of a CSV dataset and return "
                "rows, columns, data types, missing values and duplicates."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the CSV file."
                    }
                },
                "required": ["file_path"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "check_data_quality",
            "description": (
                "Check a CSV dataset for data-quality issues including "
                "missing values, duplicate rows, duplicate customer IDs, "
                "invalid ages and invalid email formats."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the CSV file."
                    }
                },
                "required": ["file_path"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "clean_customer_data",
            "description": (
                "Clean the customer CSV by removing exact duplicate rows, "
                "handling missing age values, normalising email values, "
                "and saving the cleaned dataset."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "input_path": {
                        "type": "string",
                        "description": "Path to the input CSV file."
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Path where the cleaned CSV should be saved."
                    }
                },
                "required": [
                    "input_path",
                    "output_path"
                ]
            }
        }
    }
]


# --------------------------------------------------
# 3. Tool registry
# --------------------------------------------------

tool_registry = {
    "analyse_schema": analyse_schema,
    "check_data_quality": check_data_quality,
    "clean_customer_data": clean_customer_data,
}

state: AgentState = {
    "original_file": "data/raw/customer.csv",
    "status": "starting"
}


# --------------------------------------------------
# 4. User request
# --------------------------------------------------

user_message = (
    "Analyse data/raw/customer.csv completely. "
    "First analyse the schema, then check data quality. "
    "If quality problems are found, clean the dataset and "
    "save it to data/clean/customer_cleaned.csv. "
    "After cleaning, run the data-quality check again on "
    "the cleaned file to verify that the problems were resolved. "
    "Only report the dataset as successfully cleaned if the "
    "verification shows no remaining quality issues."
)


# --------------------------------------------------
# 5. Conversation state
# --------------------------------------------------

messages = [
    {
        "role": "user",
        "content": user_message
    }
]


# --------------------------------------------------
# 6. Agent loop
# --------------------------------------------------

max_iterations = 5

for iteration in range(max_iterations):

    print(f"\n===== AGENT ITERATION {iteration + 1} =====")

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    message = response.choices[0].message

    # Add the assistant's response to conversation history
    messages.append(message)

    # --------------------------------------------------
    # If the LLM does not request a tool, finish
    # --------------------------------------------------

    if not message.tool_calls:

        print("\n===== FINAL AI ANALYSIS =====")
        print(message.content)

        break


    # --------------------------------------------------
    # Execute requested tools
    # --------------------------------------------------

    for tool_call in message.tool_calls:

        tool_name = tool_call.function.name

        tool_arguments = json.loads(
            tool_call.function.arguments
        )

        print("\n===== TOOL REQUESTED BY LLM =====")
        print("Tool:", tool_name)
        print("Arguments:", tool_arguments)


        # Find the Python function
        tool_function = tool_registry.get(tool_name)

        if tool_function is None:

            raise ValueError(
                f"Unknown tool requested: {tool_name}"
            )


        # Execute the selected tool
        tool_result = tool_function(
            **tool_arguments

        )
            # --------------------------------------------------
    # Execute requested tools
    # --------------------------------------------------

    for tool_call in message.tool_calls:

        tool_name = tool_call.function.name

        tool_arguments = json.loads(
            tool_call.function.arguments
        )

        print("\n===== TOOL REQUESTED BY LLM =====")
        print("Tool:", tool_name)
        print("Arguments:", tool_arguments)


        # Find the Python function
        tool_function = tool_registry.get(tool_name)

        if tool_function is None:
            raise ValueError(
                f"Unknown tool requested: {tool_name}"
            )


        # Execute the selected tool
        tool_result = tool_function(
            **tool_arguments
        )


        # --------------------------------------------------
        # Store result in Agent State
        # --------------------------------------------------

        if tool_name == "analyse_schema":

            state["schema_result"] = tool_result

        elif tool_name == "check_data_quality":

            if tool_arguments["file_path"] == state["original_file"]:

                state["quality_result"] = tool_result

            else:

                state["verification_result"] = tool_result

        elif tool_name == "clean_customer_data":

            state["cleaning_result"] = tool_result



        print("\n===== TOOL RESULT =====")
        print(tool_result)


        # --------------------------------------------------
        # Send tool result back to the LLM
        # --------------------------------------------------

        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(tool_result)
            }
        )

else:

    print(
        "\nAgent stopped because the maximum number "
        "of iterations was reached."
    )