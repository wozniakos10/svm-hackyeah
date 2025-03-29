import numpy as np
import plotly.graph_objects as go
import streamlit as st


def main() -> None:
    st.title("Asystent oszczędzania")

    st.header("Wprowadź input")
    selected_func_type = st.selectbox("Target Function", ca.FunctionBox.values())
    selection_method = st.selectbox("Selection Method", ca.SelectionBox.values())


    # Button to run
    run_button = st.button("Run")


if __name__ == "__main__":
    main()