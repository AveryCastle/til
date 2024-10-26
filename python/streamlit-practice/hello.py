import streamlit as st

st.write("hello, world!")
x = st.text_input("favorite movies?")
st.write(f"your favorite movie is {x}")

is_clicked = st.button("click me")

st.write("## This is a H2 Title")