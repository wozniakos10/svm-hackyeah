from openai import OpenAI
from svm_hack.app.schema import UserForm
from dotenv import load_dotenv

load_dotenv()

def tools_schema() -> str:
    update_plots_schema = {
        "type": "function",
        "function": {
            "name": "update_plots",
            "description": "Update the plots",
            "parameters": {
            "type": "object",
            "properties": {
                "investing_strategies": {
                    "type": "array",
                    "description": "List of investing strategies. Always 3 of them",
                    "items": {
                        "type": "string",
                        "enum": ["ike", "etf", "kryptowaluta", "nieruchomość", "depozyt", "akcja"]
                    }
                }
            },
            "required": ["investing_strategies"]
            }
        }
      }
    
    tools = [update_plots_schema]
    return tools

def create_system_prompt(user_form: UserForm) -> str:
    prompt = f"""
    You act as a financial advisor and help users create a strategy based on their goals and risk tolerance.
    You will be given a user's information and you will need to create a strategy for them.

    For the 
    
    User Name: {user_form.name}
    User Age: {user_form.age}
    Initial capital: {user_form.initial_capital}
    Desired strategy: {user_form.desired_strategy}
    Investing timeline: {user_form.investing_timeline}
    """
    return prompt

def create_completion(user_form: UserForm, messages: list[dict]):

    client = OpenAI()
    system_prompt = create_system_prompt(user_form)

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
        ] + messages,
        tools=tools_schema(),
        tool_choice="auto"
    )

    if completion.choices[0].message.tool_calls:
        return completion.choices[0].message
    else:
        return completion.choices[0].message


def create_completion_for_tool_call(user_form: UserForm, messages: list[dict]):

    client = OpenAI()
    system_prompt = create_system_prompt(user_form)

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
        ] + messages,
    )

    if completion.choices[0].message.tool_calls:
        return completion.choices[0].message
    else:
        return completion.choices[0].message