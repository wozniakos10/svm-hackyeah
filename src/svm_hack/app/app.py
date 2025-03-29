import numpy as np
import plotly.graph_objects as go
import streamlit as st
import json
from svm_hack.app.utils import st_dtypes
from svm_hack.app.models import cfg
from svm_hack.app.llm import create_completion, create_completion_for_tool_call
from svm_hack.app.schema import UserForm
from svm_hack.app.plotting import get_products_info, plot_strategy

st.set_page_config(layout="wide")
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
            raise ValueError("Incorrect age bucket selected")

    selection_time = st.selectbox(
        "W jakim horyzoncie czasowym chcesz zainwestować?",
        st_dtypes.TimeHorizonBox.values(),
    )
    match selection_time:
        case st_dtypes.TimeHorizonBox.SHORT:
            investment_time = 2  # in years (could be changed to months)
        case st_dtypes.TimeHorizonBox.MEDIUM:
            investment_time = 5
        case st_dtypes.TimeHorizonBox.LONG:
            investment_time = 20
        case _:
            raise ValueError("Incorrect investment time horizon selected")

    selected_revenues = st.number_input(
        "Jakie masz przychody? (miesięcznie)", min_value=0, step=100, value=5000
    )
    selected_expenses = st.number_input(
        "Jakie masz wydatki? (miesięcznie)", min_value=0, step=100, value=2500
    )

    if selected_expenses > selected_revenues:
        st.write("ty sie skup na oszczedzaniu, a nie na inwestowaniu")
    else:
        suggested_investment = (1 - avg_age / 100) * (
            selected_revenues - selected_expenses
        )

        st.write(f'Sugerowany plan inwestycyjny to: {suggested_investment:.2f} zł miesięcznie')

    user_form = UserForm(
        name="Mateusz",
        age=selected_age_bucket,
        initial_capital=str(1000),
        desired_strategy="Zarabianie na kryptowalutach",
        investing_timeline=selection_time
    )

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


        # Stream the response to the chat using `st.write_stream`, then store it in
        # # session state.
        # with st.chat_message("assistant"):
        #     response = st.write_stream(create_completion(user_form, st.session_state.messages))

        response = create_completion(user_form, st.session_state.messages)



        if response.tool_calls:
            st.chat_message("assistant").write(response.tool_calls)
            # PLOTOWANIE STRATEGII
            product_types = json.loads(response.tool_calls[0].function.arguments).get("investing_strategies")
            print("-"*30)
            print(f"Product types: {product_types}")
            print("-" * 30)
            products_dict = get_products_info(product_types)
            MONTHLY_RATE = 500
            YEARS = 5
            plot_strategy(products_dict, MONTHLY_RATE, YEARS)



            tool_message = {                               # append result message
                "role": "tool",
                "tool_call_id": response.tool_calls[0].id,
                "content": "dupa"
            }
            st.session_state.messages.append(tool_message)

            response = create_completion_for_tool_call(user_form, st.session_state.messages)
            st.session_state.messages.append({"role": "assistant", "content": response.content})
        else:
            st.chat_message("assistant").write(response.content)
            st.session_state.messages.append({"role": "assistant", "content": response.content})


if __name__ == "__main__":
    main()
