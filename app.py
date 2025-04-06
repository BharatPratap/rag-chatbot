import streamlit as st
from app.rag_chain import qa_chain

st.set_page_config(page_title="RAG Chatbot", layout="wide")

st.title("RAG Chatbot")

# Input box
question = st.text_input("Ask a question based on your documents:")

# Handle input
if question:
    with st.spinner("Thinking..."):
        result = qa_chain.invoke({"query": question})
        st.markdown("### Answer")
        st.write(result["result"])

