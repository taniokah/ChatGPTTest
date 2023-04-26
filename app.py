import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", 
         "content": st.secrets.AppSettings.chatbot_setting + 
                    st.secrets.AppSettings.chatbot_setting2 + 
                    st.secrets.AppSettings.chatbot_setting3 + 
                    st.secrets.AppSettings.chatbot_setting4 + 
                    st.secrets.AppSettings.chatbot_setting5 + 
                    #st.secrets.AppSettings.chatbot_setting6 + 
                    st.secrets.AppSettings.chatbot_setting7 + 
                    #st.secrets.AppSettings.chatbot_setting8 + 
                    #st.secrets.AppSettings.chatbot_setting9 + 
                    #st.secrets.AppSettings.chatbot_setting10 + 
                    st.secrets.AppSettings.chatbot_setting11
        }
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages, 
        temperature=st.secrets.AppSettings.temperature
    )  

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title(st.secrets.AppSettings.title)
st.write(st.secrets.AppSettings.body)

user_input = st.text_input(st.secrets.AppSettings.input, key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
