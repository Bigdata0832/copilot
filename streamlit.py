import streamlit as st
from datetime import datetime
from src.logic import start_chat, clear_chat, select_assistant, send_message

def main():
    st.title("KEYPO Copilot")

    # 初始化狀態
    if 'thread_id' not in st.session_state:
        st.session_state.thread_id = None
    if 'assistant_id' not in st.session_state:
        st.session_state.assistant_id = None

    # 左側邊欄 - Thread Dashboard
    with st.sidebar:
        st.header("Thread Dashboard")
        if st.button("Create"):
            thread_id = start_chat()
            st.session_state.thread_id = thread_id
            st.write(f"New thread created with ID: {st.session_state.thread_id}")
        if st.button("Clear"):
            if st.session_state.thread_id:
                clear_chat(st.session_state.thread_id)
                st.write(f"The thread with ID {st.session_state.thread_id} has been cleared!")
                st.session_state.thread_id = None
                st.session_state.assistant_id = None

    # 右側邊欄 - Copilot Version
    with st.expander("Copilot Version"):
        col1, col2, _ = st.columns([1, 1, 7])
        with col1:
            if st.button("1.0.1"):
                st.session_state.assistant_id = select_assistant(name="KEYPO Copilot")
                st.write("Using Version 1.0.1")
        with col2:
            if st.button("1.0.2"):
                st.session_state.assistant_id = select_assistant(name="KEYPO Copilot2.0")
                st.write("Using Version 1.0.2")

    # 主功能區域
    if st.session_state.thread_id and st.session_state.assistant_id:
        prompt = st.text_input("User:")
        if st.button("Submit"):
            chat_history = send_message(
                user_message=prompt,
                assistant_id=st.session_state.assistant_id,
                thread_id=st.session_state.thread_id,
            )
            resp = chat_history[-1].replace("assistant: ","")
            st.write(f"KEYPO Copilot: {resp}")
            st.divider()
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.write(f"Response received at: {current_time}")
            st.write(chat_history)

if __name__ == "__main__":
    main()
