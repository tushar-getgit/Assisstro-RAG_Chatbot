import requests
import gradio as gr
import streamlit as st

API_KEY = st.secrets["api_keys"]["API_KEY"]
API_URL = st.secrets["api_keys"]["API_URL"]

his = []
def perplexity_chatbot(query,history):
    messages = [{"role": "user", "content": "Act like a Astrologer who is expert in Numerology and astrology.\
    Reply in consise and minimum words and do not repeat that you are Astrologer or Numerology. Be very professional."+query}]
    his.append( messages[0])
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "sonar",  #sonar-pro
        "messages":his ,
        # "max_tokens": 150,
        # "temperature": 0.2
    }
    response = requests.post(API_URL, json=data, headers=headers)
    if response.status_code == 200:
        assistant_reply = response.json()["choices"][0]["message"]["content"]
        his.append({"role": "assistant", "content": assistant_reply})
        return assistant_reply
    else:
        return f"Error: {response.status_code} - {response.text}"

if "messages" not in st.session_state:
    st.session_state.messages = []
    
st.title("*** ASSISSTRO - AI ***")
st.markdown("""I am a AI assistant for all your astrology needs. You can find out :
            - How will your day be?
            - How is this year going to be for you?
            - Is your Zodic sign compatible with your name ?
            - Discover your compatibility with your partner using just your names or dates of birth.
            and much more....""")
# Display the existing chat messages via `st.chat_message`.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("What is your query?"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    bot_reply = perplexity_chatbot(user_input, st.session_state.messages)
    with st.chat_message("assistant"):
        response = st.write(bot_reply)
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})



