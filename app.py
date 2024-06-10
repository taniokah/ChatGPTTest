import streamlit as st
import openai
from openai import OpenAI

client = OpenAI(
    # Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
    api_key = st.secrets.OpenAIAPI.openai_api_key
)

import datetime

dt = datetime.datetime.today()  # ローカルな現在の日付と時刻を取得

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [{
            "role": "system", 
            "content": st.secrets.AppSettings.chatbot_setting + 
                " 今日は" + str(dt) + "です。" + 
                " あなたはいま、徳島大学常三島キャンパスにいます。" + 
                " とくぽんは、徳島大学に住み着いているマスコットキャラクターです。" +
                " systemに与えられた情報以外の情報を用いて会話してはいけません。"
        }
    ]
    #st.write(st.session_state["messages"])

# チャットボットとやりとりする関数
def communicate():
    user_input = st.session_state["user_input"]
    inputs = [m.surface()  if m.part_of_speech()[0] in morph else ""  for m in tokenizer_obj.tokenize(user_input, mode)]
    #if len(inputs) > 0:
        #st.write(inputs)

    target = []
    for i in range(len(ms_)):
        m = ms_[i]
        for input in inputs:
            if len(input) > 1:
                if input in m:
                    #st.write("key " + input)
                    q = qs_[i].get_text() if i < len(qs_) else ""
                    r = rs_[i].get_text() if i < len(rs_) else ""
                    a = as_[i].get_text() if i < len(as_) else ""
                    target.append("質問: " + q + "(" + r + ") 回答: " + a)
    target = ", ".join(target)
    #if len(target) > 0: 
        #st.write(target)
    
    messages = st.session_state["messages"]
    user_message = {
        "role": "user", 
        "content": st.session_state["user_input"]
    }
    user_message_ = {}
    if len(target) > 0: 
        #messages[0] = {
        #    "role": "system", 
        #    "content": st.secrets.AppSettings.chatbot_setting + 
        #        "とくぽんAI塾では次のように説明されています。" + 
        #        target + #st.secrets.AppSettings.chatbot_setting2 + 
        #        "この内容はすべて正しいので、これを元に、できるだけ原文のまま、回答してください。" + 
        #        " systemに与えられた情報以外の情報を用いて会話してはいけません。"
        #}
        user_message_ = {
            "role": user_message["role"], 
            "content": "「" + user_message["content"] + "」の内容について、" + 
                "「" + target + "」の内容を元に、回答できる場合は、できるだけ原文のまま、私に回答をしてください。" + 
                "与えられた情報以外を用いて会話してはいけません。"
        }
    else:
        #messages[0] = {
        #    "role": "system", 
        #    "content": st.secrets.AppSettings.chatbot_setting + 
        #        " 今日は" + str(dt) + "です。" + 
        #        " あなたはいま、徳島大学常三島キャンパスにいます。" + 
        #        " とくぽんは、徳島大学に住み着いているマスコットキャラクターです。" +
        #        " systemに与えられた情報以外の情報を用いて会話してはいけません。"
        #}
        user_message_ = {
            "role": "user", 
            "content": "「" + st.session_state["user_input"] +  "」の内容が、挨拶の場合は、素直に回答してください。" +
                "自己紹介や名前の確認は積極的にしましょう。" + 
                "とくぽんAI塾に関連する話題の場合は、返答文の形で1文30字以内で回答してください。" + 
                 #"とくぽんAI塾への質問ならば、返答文の形で1文30字以内で回答してください。" + 
                "それ以外の場合は、「どういう意味かな？」と回答してください。"
        }
    
    _messages = st.session_state["messages"]
    _messages.append(user_message_)
    
    if len(messages) > 5:
        _messages = [_messages[0]] + _messages[len(messages)-5:]
    
    completion = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = _messages, 
        temperature=st.secrets.AppSettings.temperature
    )
    #st.write(_messages)
    messages[len(messages)-1] = user_message
    
    st.session_state["messages"] = messages

    bot_message = {
        "role": completion.choices[0].message.role,
        "content": completion.choices[0].message.content, 
    }
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去
    #st.write(messages)


# ユーザーインターフェイスの構築
st.title(st.secrets.AppSettings.title)
st.write(st.secrets.AppSettings.body)
st.write(st.secrets.AppSettings.body2)
st.write(st.secrets.AppSettings.body3)

user_input = st.text_input(st.secrets.AppSettings.input, key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    #st.write(messages);

    for message in messages[1:]:#reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = ""
        if message["role"]=="assistant":
            speaker="🤖"
        elif message["role"]=="user":
            speaker = "🙂"
        else:
            continue
        st.write(speaker + ": " + message["content"])

    #if len(messages) > 5:
    #    st.session_state["messages"] = [messages[0]] + messages[3:]

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

morph = ('名詞')
ms_ = []

for i in range(len(qs_)) : 
    m = []
    q = qs_[i].get_text() if i < len(qs_) else ""
    r = rs_[i].get_text() if i < len(rs_) else ""
    a = as_[i].get_text() if i < len(as_) else ""
    #st.write(q + '(' + r + ') ' + a)
    words_q = [m.surface() if m.part_of_speech()[0] in morph else ""  for m in tokenizer_obj.tokenize(q, mode)]
    words_r = [m.surface() if m.part_of_speech()[0] in morph else ""  for m in tokenizer_obj.tokenize(r, mode)]
    words_a = [m.surface() if m.part_of_speech()[0] in morph else ""  for m in tokenizer_obj.tokenize(a, mode)]
    m = words_q + words_r + words_a
    ms_.append(m)
#st.write(ms_)

#st.write(messages)
