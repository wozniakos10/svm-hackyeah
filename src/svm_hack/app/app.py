from collections import namedtuple

import streamlit as st
import json
from svm_hack.app.utils import st_dtypes
from svm_hack.app.llm import create_completion, create_completion_for_tool_call
from svm_hack.app.plotting import get_products_info, plot_strategy

UserInfo = namedtuple(
    "UserInfo",
    [
        "age",
        "time_horizon",
        "revenues",
        "expenses",
        "invest_percent",
        "reaction_to_loss",
    ],
)


def input_form() -> UserInfo:
    """Zebranie danych od użytkownika"""
    left_col, right_col = st.columns(2)
    with left_col:
        selected_age_bucket = st.selectbox("Ile masz lat?", st_dtypes.AgeBox.values())
    with right_col:
        selected_time = st.selectbox(
            "W jakim horyzoncie czasowym chcesz zainwestować?",
            st_dtypes.TimeHorizonBox.values(),
        )

    match selected_age_bucket:
        case st_dtypes.AgeBox.YOUNG:
            user_avg_age = 21
        case st_dtypes.AgeBox.MIDDLE_AGE:
            user_avg_age = 32
        case st_dtypes.AgeBox.OLDER:
            user_avg_age = 45
        case st_dtypes.AgeBox.SENIOR:
            user_avg_age = 70
        case _:
            raise ValueError("Incorrect age bucket selected")

    match selected_time:
        case st_dtypes.TimeHorizonBox.SHORT:
            investment_time = 5  # in years (could be changed to months)
        case st_dtypes.TimeHorizonBox.MEDIUM:
            investment_time = 10
        case st_dtypes.TimeHorizonBox.LONG:
            investment_time = 20
        case _:
            raise ValueError("Incorrect investment time horizon selected")

    with left_col:
        selected_revenues = st.number_input(
            "Jakie masz przychody? (miesięcznie)", min_value=0, step=100, value=5000
        )
    with right_col:
        selected_expenses = st.number_input(
            "Jakie masz wydatki? (miesięcznie)", min_value=0, step=100, value=2500
        )

    with left_col:
        selected_invest_percent = st.selectbox(
            "Jaki procent swoich miesięcznych dochodów możesz przeznaczyć na inwestycje, nie martwiąc się o bieżące wydatki?",
            st_dtypes.PercentMoneyBox.values(),
        )
    with right_col:
        selected_reaction_to_loss = st.selectbox(
            "Jak byś zareagował(a), gdyby Twoja inwestycja straciła 20% wartości w krótkim czasie?",
            st_dtypes.ReactionBox.values(),
        )

    return UserInfo(
        age=user_avg_age,
        time_horizon=investment_time,
        revenues=selected_revenues,
        expenses=selected_expenses,
        invest_percent=selected_invest_percent,
        reaction_to_loss=selected_reaction_to_loss,
    )


def main() -> None:
    st.set_page_config(
        page_title="InvestMate",
        page_icon="📈",
        layout="wide",
    )
    st.title("👨‍🦰 InvestMate")
    st.write("Moim zadaniem jest stanie się Twoim personalnym doradcą inwestycyjnym.")
    st.write(
        "Wypełnij formularz, a ja postaram się pomóc Ci ułożyć swój pierwszy plan inwestycyjny 😊"
    )

    st.header("📊 Powiedz mi coś o sobie!")
    user_info = input_form()

    # Button to run
    run_button = st.button(
        "Zaczynam inwestować...",
        help="Naciśnij, aby obliczyć sugerowany plan inwestycyjny",
    )
    print(run_button)

    budget = user_info.revenues - user_info.expenses
    if budget <= 0:
        raise ValueError("💀 ty sie skup na oszczedzaniu, a nie na inwestowaniu")
    else:
        suggested_investment = (1 - user_info.age / 100) * budget
        budget_perc = suggested_investment / budget * 100
        st.write(
            f"Sugerowany plan inwestycyjny to: {suggested_investment:.2f} zł miesięcznie ({budget_perc:.1f}% budżetu)"
        )
        selected_investment = st.slider(
            "Jaką część tej kwoty chcesz przeznaczyć na inwestycje?",
            value=suggested_investment,
            min_value=round(suggested_investment * 0.7, 0),
            max_value=round(suggested_investment * 1.5, 0),
            step=1.0,
        )
        print(selected_investment)

    # Show title and description.
    st.header("💬 Czy masz jeszcze jakieś pytania?")
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

        response = create_completion(user_info, st.session_state.messages)

        if response.tool_calls:
            st.chat_message("assistant").write(response.tool_calls)
            # PLOTOWANIE STRATEGII
            product_types = json.loads(response.tool_calls[0].function.arguments).get(
                "investing_strategies"
            )
            print("-" * 30)
            print(f"Product types: {product_types}")
            print("-" * 30)
            products_dict = get_products_info(product_types)
            plot_strategy(products_dict, selected_investment, user_info.time_horizon)

            tool_message = {  # append result message
                "role": "tool",
                "tool_call_id": response.tool_calls[0].id,
                "content": "dupa",
            }
            st.session_state.messages.append(tool_message)

            response = create_completion_for_tool_call(
                user_info, st.session_state.messages
            )
            st.session_state.messages.append(
                {"role": "assistant", "content": response.content}
            )
        else:
            st.chat_message("assistant").write(response.content)
            st.session_state.messages.append(
                {"role": "assistant", "content": response.content}
            )


if __name__ == "__main__":
    main()
