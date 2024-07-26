import streamlit as st
from utils.llm.assistant import create_thread, delete_thread, create_messages_to_thread, run_assistant, get_chat_history

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
            thread = create_thread()
            st.session_state.thread_id = thread.id
            st.write(f"New thread created with ID: {st.session_state.thread_id}")
        if st.button("Clear"):
            if st.session_state.thread_id:
                delete_thread(st.session_state.thread_id)
                st.write(f"The thread with ID {st.session_state.thread_id} has been cleared!")
                st.session_state.thread_id = None
                st.session_state.assistant_id = None

    # 右側邊欄 - Copilot Version
    with st.expander("Copilot Version"):
        if st.button("輿情1.0.1"):
            st.session_state.assistant_id = "asst_Q0aogQUlR5PkLuBB6Hmh6mk5"
            st.write("Using Version 1.0.1")

    # 主功能區域
    if st.session_state.thread_id and st.session_state.assistant_id:
        prompt = st.text_input("User:")
        if st.button("Submit"):
            create_messages_to_thread(
                thread_id=st.session_state.thread_id,
                role="user",
                content=prompt
            )
            run = run_assistant(thread_id=st.session_state.thread_id, assistant_id=st.session_state.assistant_id)
            chat_history = get_chat_history(run=run, thread_id=st.session_state.thread_id)
            st.write(chat_history[-1])

        if st.button("Chat History Submit"):
            create_messages_to_thread(
                thread_id=st.session_state.thread_id,
                role="user",
                content=prompt
            )
            run = run_assistant(thread_id=st.session_state.thread_id, assistant_id=st.session_state.assistant_id)
            chat_history = get_chat_history(run=run, thread_id=st.session_state.thread_id)
            st.write(chat_history)

if __name__ == "__main__":
    main()
