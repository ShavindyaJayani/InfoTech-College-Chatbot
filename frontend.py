import streamlit as st
import requests
import json


st.set_page_config(
    page_title="InfoTech College Chatbot",
    page_icon="🎓",
    layout="wide"
)


st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1E3A8A;
        text-align: center;
    }
    .chat-container {
        background-color: #F0F2F6;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        max-height: 400px;
        overflow-y: auto;
    }
    .user-message {
        background-color: #1E3A8A;
        color: white;
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
        text-align: right;
    }
    .bot-message {
        background-color: #E5E7EB;
        color: black;
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
        text-align: left;
    }
    .stButton button {
        width: 100%;
        background-color: #1E3A8A;
        color: white;
    }
</style>
""", unsafe_allow_html=True)


st.markdown('<h1 class="main-header">InfoTech College Chatbot</h1>', unsafe_allow_html=True)
st.markdown("""
Welcome to the InfoTech College Chatbot! I can help you with information about:
- Programs and courses
- Admission requirements
- Tuition and fees
- Program duration
- Contact information

Ask me anything about InfoTech College!
""")


if "messages" not in st.session_state:
    st.session_state.messages = []



chat_container = st.container()
with chat_container:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="user-message"><b>You:</b> {message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-message"><b>Chatbot:</b> {message["content"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)



user_input = st.text_input("Type your message here:", key="input", placeholder="Ask about programs, admission, fees...")


if st.button("Send") and user_input:
    
    st.session_state.messages.append({"role": "user", "content": user_input})
    
   
    try:
        response = requests.post(
            "http://localhost:8000/chat",
            json={"message": user_input}
        )
        
        if response.status_code == 200:
            data = response.json()
            bot_response = data["response"]
            sources = data["sources"]
            
            
            full_response = f"{bot_response}\n\nSources: {', '.join(sources)}"
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        else:
            error_msg = "Sorry, I'm having trouble connecting to the knowledge base. Please try again later."
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
            
    except requests.exceptions.RequestException:
        error_msg = "Unable to connect to the chatbot service. Please make sure the backend is running."
        st.session_state.messages.append({"role": "assistant", "content": error_msg})
    
    
    st.rerun()


with st.sidebar:
    st.image("https://via.placeholder.com/150x150.png?text=College+Logo", width=150)
    st.title("InfoTech College")
    st.markdown("""
    **Contact Information:**
    - Email: info@infotechcollege.com
    - Phone: (555) 123-4567
    - Address: 123 Tech Avenue, Innovation City
    """)
    
    st.markdown("---")
    st.markdown("""
    **Quick Questions:**
    - What programs are offered?
    - How much is tuition?
    - What are admission requirements?
    - How long are the programs?
    """)
    
    
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.rerun()


st.markdown("---")
st.markdown("© 2025 InfoTech College Chatbot | Built with FastAPI and Streamlit")