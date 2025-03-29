import streamlit as st
from openai import OpenAI
from svm_hack.app.models import cfg
from svm_hack.app.models import product_database


class ProductAssistant:
    def __init__(self, api_key=cfg.OPENAI_API_KEY, product_db=product_database):
        """
        Inicjalizacja klienta OpenAI i bazy danych produktów.
        """
        self.client = OpenAI(api_key=api_key)
        self.product_db = product_db

    def get_openai_response(self, user_input: str) -> str:
        """
        Funkcja do komunikacji z OpenAI API, aby uzyskać odpowiedź na zapytanie użytkownika.
        """
        try:
            # Przygotowanie zapytania do OpenAI
            completion = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": f"Jesteś asystentem, który powinien wytłumaczyć użytkownikowi pojęcia związane z inwestowaniem."
                        f"Wiedzę o produktach bierz z tego jsona: {self.product_db.model_dump_json(indent=4)}\nNie"
                        f"możesz wymyślać informacji, korzystaj z bazy wiedzy którą ci podałem.",
                    },
                    {"role": "user", "content": user_input},
                ],
            )

            return completion.choices[0].message.content
        except Exception as e:
            return f"Error: {e}"

    def run_streamlit_interface(self):
        """
        Funkcja uruchamiająca interfejs Streamlit, gdzie użytkownik może zadawać pytania.
        """
        st.title("Asystent Inwestycyjny")

        user_input = st.text_input("Zadaj pytanie dotyczące inwestowania:")

        if user_input:
            response = self.get_openai_response(user_input)
            st.write("Odpowiedź Asystenta:")
            st.write(response)


# Przykład użycia:
if __name__ == "__main__":
    # Inicjalizacja klasy z odpowiednimi parametrami
    assistant = ProductAssistant(
        api_key=cfg.OPENAI_API_KEY, product_db=product_database
    )
