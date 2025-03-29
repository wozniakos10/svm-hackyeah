from openai import OpenAI
from dotenv import load_dotenv
import json
from svm_hack.app.schema import UserInfo

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
                    "description": "Lista strategii inwestycyjnych. Zawsze musisz wybrać 3 strategie",
                    "items": {
                        "type": "string",
                        "enum": ["obligacja", "ike", "etf", "kryptowaluta", "nieruchomość", "depozyt", "akcja"]
                    }
                }
            },
            "required": ["investing_strategies"]
            }
        }
      }
    
    tools = [update_plots_schema]
    return tools

def create_system_prompt(user_info: UserInfo) -> str:
    prompt = f"""
    Działasz jako doradca finansowy i pomagasz użytkownikom tworzyć strategie w oparciu o ich cele i tolerancję ryzyka.
    Otrzymasz informacje o użytkowniku i będziesz musiał stworzyć dla niego strategię.

    Twoja pierwsza wiadomość musi być pojedynczym wywołaniem narzędzia, aby wyświetlić użytkownikowi sugerowaną strategię na podstawie jego informacji.
    Wybierz 3 strategie dla użytkownika. W rezultacie zobaczy wykresy dla każdej strategii.

    Używaj wywołań narzędzi tylko wtedy, gdy użytkownik prosi o nową strategię. W przeciwnym razie odpowiadaj normalnymi wiadomościami.
    
    Odpowiedz w języku polskim.
    
    Wiek użytkownika: {user_info.age}
    Horyzont czasowy: {user_info.time_horizon}
    Przychody: {user_info.revenues}
    Wydatki: {user_info.expenses}
    Procent dochodów miesięcznych przeznaczonych na inwestycje: {user_info.invest_percent}
    Reakcja na straty: {user_info.reaction_to_loss}
    """
    return prompt

def create_system_prompt_for_tool_call(user_info: UserInfo) -> str:
    prompt = f"""
    Działasz jako doradca finansowy i pomagasz użytkownikom tworzyć strategie w oparciu o ich cele i tolerancję ryzyka.
    Otrzymasz informacje o użytkowniku i będziesz musiał stworzyć dla niego strategię.
    Na podstawie poprzednich wiadomości zdecyduj, która strategia najlepiej pasuje do użytkownika.
    Twoja odpowiedź powinna bazować na wynikach z wykresów.
    Odpowiedz w języku polskim.
    
    Wiek użytkownika: {user_info.age}
    Horyzont czasowy: {user_info.time_horizon}
    Przychody: {user_info.revenues}
    Wydatki: {user_info.expenses}
    Procent dochodów miesięcznych przeznaczonych na inwestycje: {user_info.invest_percent}
    Reakcja na straty: {user_info.reaction_to_loss}


    """
    return prompt

def create_completion(user_info: UserInfo, messages: list[dict]):

    client = OpenAI()
    system_prompt = create_system_prompt(user_info)

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


def create_completion_for_tool_call(user_info: UserInfo, messages: list[dict]):

    client = OpenAI()
    system_prompt = create_system_prompt_for_tool_call(user_info)

    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
        ] + messages,
        stream=True
    )

    return stream