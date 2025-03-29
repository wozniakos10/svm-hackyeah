import numpy as np
import plotly.graph_objects as go
import streamlit as st
from openai import OpenAI
from svm_hack.app.utils import st_dtypes
from svm_hack.app.models import cfg
from svm_hack.app.llms import ProductAssistant


def main() -> None:
    # Inicjalizacja klasy ProductAssistant
    assistant = (
        ProductAssistant()
    )  # W przypadku bazy danych zmieniamy `product_db` na odpowiednią instancję

    # Create an OpenAI client.
    # Show title and description.
    st.title("💬 Chatbot")
    st.write("Zapytaj mnie o produkty inwestycyjne.")

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("What is up?"):
        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API through the assistant
        response = assistant.get_openai_response(prompt)

        # Display the assistant's response in the chat
        with st.chat_message("assistant"):
            st.markdown(response)

        # Store the assistant's response in the session state
        st.session_state.messages.append({"role": "assistant", "content": response})


main()
