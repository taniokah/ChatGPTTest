import streamlit as st
import openai
from openai import OpenAI

client = OpenAI(
    # Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
    api_key = st.secrets.OpenAIAPI.openai_api_key
)

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [{
            "role": "system", 
            "content": st.secrets.AppSettings.chatbot_setting
        }
    ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]
    messages[0] = {
        "role": "system", 
        "content": st.secrets.AppSettings.chatbot_setting + 
            "とくぽんAI塾では次のように説明されています。" + 
            target + #st.secrets.AppSettings.chatbot_setting2 + 
            "この内容はすべて正しいので、これを元に、できるだけ原文のまま、回答してください。"
    }

    user_message = {
        "role": "user", 
        "content": st.session_state["user_input"]
    }
    messages.append(user_message)
    
    completion = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = messages, 
        temperature=st.secrets.AppSettings.temperature
    )

    bot_message = {
        "role": completion.choices[0].message.role,
        "content": completion.choices[0].message.content, 
    }
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title(st.secrets.AppSettings.title)
st.write(st.secrets.AppSettings.body)
st.write(st.secrets.AppSettings.body2)

user_input = st.text_input(st.secrets.AppSettings.input, key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    #st.write(messages);

    for message in messages[1:]:#reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = ""
        if message["role"]=="assistant":
            speaker="🤖"
        if message["role"]=="user":
            speaker = "🙂"

        st.write(speaker + ": " + message["content"])


from bs4 import BeautifulSoup
import requests

url = "https://www.tokushima-u.ac.jp/ai/tokupon/qalist2021.html"

res = requests.get(url)
res.encoding = res.apparent_encoding
#soup = BeautifulSoup(res.text, 'html.parser')
soup = BeautifulSoup(res.content.decode("utf-8", "ignore"), "html.parser") #追加
#title_text = soup.find('title').get_text()
qs_ = soup.find_all(class_="q")
rs_ = soup.find_all(class_="r")
as_ = soup.find_all(class_="a")
#st.write(str(len(qs_)) + ' ' + str(len(rs_)) + ' ' + str(len(as_)))


from sudachipy import tokenizer
from sudachipy import dictionary

tokenizer_obj = dictionary.Dictionary().create()

mode = tokenizer.Tokenizer.SplitMode.B
#words = [m.surface() for m in tokenizer_obj.tokenize(title_text, mode)]
#st.write(words)

target = []
for i in range(len(qs_)) : 
    user_input = st.session_state["user_input"]
    inputs = [m.surface() for m in tokenizer_obj.tokenize(user_input, mode)]
    
    q = qs_[i].get_text() if i < len(qs_) else ""
    r = rs_[i].get_text() if i < len(rs_) else ""
    a = as_[i].get_text() if i < len(as_) else ""
    #st.write(q + '(' + r + ') ' + a)
    words = [m.surface() for m in tokenizer_obj.tokenize(q, mode)]
    #st.write(words)
    for input in inputs:
        if len(input) > 1: 
            if input in words:
                target.append("質問: " + q + "(" + r + ") 回答: " + a)
                break

target = ", ".join(target)
st.write("test " + target)


