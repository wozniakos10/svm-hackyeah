import numpy as np
import plotly.graph_objects as go
import streamlit as st

from svm_hack.app.utils import st_dtypes



def main() -> None:
    st.title("Asystent oszczędzania")

    st.header("Wprowadź input")
    selected_func_type = st.selectbox("Ile masz lat?", st_dtypes.AgeBox.values())
    selection_method = st.selectbox("W jakim horyzoncie czasowym chcesz zainwestować?", st_dtypes.HorizonttBox.values())


    # Button to run
    run_button = st.button("Run")


if __name__ == "__main__":
    main()