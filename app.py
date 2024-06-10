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

    user_message = {
        "role": "user", 
        "content": "とくぽんAI塾では次のように説明されています。"+ 
            st.secrets.AppSettings.chatbot_setting2 + 
            "とくぽんAI塾について、" + st.session_state["user_input"]
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

    st.write(messages);

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = ""
        if message["role"]=="assistant":
            speaker="🤖"
        if message["user"]=="assistant":
            speaker = "🙂"

        st.write(speaker + ": " + message["content"])


from bs4 import BeautifulSoup
import requests

url = "https://www.tokushima-u.ac.jp/ai/tokupon/qalist2021.html"

res = requests.get(url)
res.encoding = res.apparent_encoding
#soup = BeautifulSoup(res.text, 'html.parser')
soup = BeautifulSoup(res.content.decode("utf-8", "ignore"), "html.parser") #追加
title_text = soup.find('title').get_text()


from sudachipy import tokenizer
from sudachipy import dictionary

tokenizer_obj = dictionary.Dictionary().create()

mode = tokenizer.Tokenizer.SplitMode.B
words = [m.surface() for m in tokenizer_obj.tokenize(title_text, mode)]
#st.write(words)

import requests

url='https://sudachi.s3-ap-northeast-1.amazonaws.com/chive/chive-1.3-mc90_gensim.tar.gz'
filename='chive-1.3-mc90_gensim.tar.gz'

urlData = requests.get(url).content

with open(filename ,mode='wb') as f: # wb でバイト型を書き込める
  f.write(urlData)
st.write("loaded " + filename)

import tarfile

# tar.gzファイルを開く
with tarfile.open(filename, 'r:gz') as tar:
    tar.extractall()
st.write("extracted " + filename)

#import requests
#
#url='https://github.com/taniokah/ChatGPTTest/raw/main/chive-1.3-mc90.kv'
#filename='chive-1.3-mc90.kv'
#urlData = requests.get(url).content
#with open(filename ,mode='wb') as f: # wb でバイト型を書き込める
#  f.write(urlData)
#st.write("loaded " + filename)

import gensim

vectors = gensim.models.KeyedVectors.load("./chive-1.3-mc90_gensim/chive-1.3-mc90.kv")
#vectors = gensim.models.KeyedVectors.load("chive-1.3-mc90.kv")

for word in words: 
    st.write(word + ", " + vectors[word])
