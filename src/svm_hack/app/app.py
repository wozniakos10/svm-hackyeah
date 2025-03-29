import numpy as np
import plotly.graph_objects as go
import streamlit as st
from openai import OpenAI
from svm_hack.app.utils import st_dtypes
from svm_hack.app.models import cfg



def main() -> None:
    st.title("Asystent oszczędzania")

    st.header("Wprowadź input")
    selected_age_bucket = st.selectbox("Ile masz lat?", st_dtypes.AgeBox.values())
    match selected_age_bucket:
        case st_dtypes.AgeBox.YOUNG:
            avg_age = 21
        case st_dtypes.AgeBox.MIDDLE_AGE:
            avg_age = 32
        case st_dtypes.AgeBox.OLDER:
            avg_age = 45
        case st_dtypes.AgeBox.SENIOR:
            avg_age = 70
        case _:
            raise ValueError('Incorrect age bucket selected')

    selection_time = st.selectbox("W jakim horyzoncie czasowym chcesz zainwestować?", st_dtypes.TimeHorizonBox.values())
    match selection_time:
        case st_dtypes.TimeHorizonBox.SHORT:
            investment_time = 2  # in years (could be changed to months)
        case st_dtypes.TimeHorizonBox.MEDIUM:
            investment_time = 5
        case st_dtypes.TimeHorizonBox.LONG:
            investment_time = 20
        case _:
            raise ValueError('Incorrect investment time horizon selected')

    selected_revenues = st.number_input("Jakie masz przychody? (miesięcznie)", min_value=0, step=100, value=5000)
    selected_expenses = st.number_input("Jakie masz wydatki? (miesięcznie)", min_value=0, step=100, value=2500)

    if selected_expenses > selected_revenues:
        st.write('ty sie skup na oszczedzaniu, a nie na inwestowaniu')
    else:
        suggested_investment = (1 - avg_age/100)  * (selected_revenues - selected_expenses)

        st.write(f'Sugerowany plan inwestycyjny to: {suggested_investment:.2f} zł miesięcznie')


    # Button to run
    run_button = st.button("Run")

    # Show title and description.
    st.title("💬 Chatbot")
    st.write(
        "This is a simple chatbot that uses OpenAI's GPT-3.5 model to generate responses. "
        "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
        "You can also learn how to build this app step by step by [following our tutorial](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)."
    )

    # Ask user for their OpenAI API key via `st.text_input`.
    # Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
    # via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management


    # Create an OpenAI client.
    client = OpenAI(api_key=cfg.OPENAI_API_KEY)

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

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()