import streamlit as st
import requests
import pyperclip
import time
import os

def copy_to_clipboard():
        pyperclip.copy(st.session_state.result)
        success=st.success("Result copied to clipboard!")
        time.sleep(3)
        success.empty()
def save_answers():
    filename = f"QA_Pairs.txt"
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(f"Question: {st.session_state.query}\n")
        file.write(f"Answer: {st.session_state.result}\n\n\n")

def makeUI():
    st.set_page_config(page_title="NCC-AI")
    parent_folder_path = './source_documents'
    folder_names = [f for f in os.listdir(parent_folder_path) if os.path.isdir(os.path.join(parent_folder_path, f)) and not f.startswith('.')]
    st.header("NCC-AI👨‍💻")
    st.sidebar.title("Documents Available")
    for folder_name in folder_names:
        st.sidebar.write("- "+folder_name)
    st.sidebar.markdown('[Extract Report](https://36a2ce3eb7b0e6d-dot-us-central1.notebooks.googleusercontent.com/lab/tree/NCC_AI/QA_Pairs.txt) ⬇️')
    
    if "messages" not in st.session_state.keys(): # Initialize the chat message history
        st.session_state.messages = [
        {"role": "assistant", "content": "Welcome to Nokia Converged Charging", "time_taken": 0, "ref_docs":None}]
    if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
        st.session_state.messages.append({"role": "user", "content": prompt, "time_taken":0, "ref_docs": None})

    for message in st.session_state.messages: # Display the prior chat messages
        with st.chat_message(message["role"]):
            st.write(message["content"])
            if(message["time_taken"]!=0):
                st.write(f"({message['time_taken']} s)")
            if(message["ref_docs"]!=None):
                with st.expander("Reference Documents "):
                    for docs in message["ref_docs"]:
                        st.write(docs)
            
    # If last message is not from assistant, generate a new response
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Generating..."):
                # response = chat_engine.chat(prompt)
                response = requests.post("http://127.0.0.1:5001/ask", json={"question": prompt})
                if response.status_code==200:
                    st.write(response.json()["answer"])
                    st.write(f"({response.json()['time_taken']} s)")
                    with st.expander("Reference Documents "):
                        for docs in response.json()["ref_docs"]:
                            st.write(docs)
                    message = {"role": "assistant", "content": response.json()["answer"], "time_taken": response.json()['time_taken'],"ref_docs": response.json()["ref_docs"]}
                    st.session_state.messages.append(message) # Add response to message history
                else:
                    st.write("Error:", response.json()["error"])


if __name__ == "__main__":
    makeUI()
