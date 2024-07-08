import streamlit as st
import data.data as dd
import pymysql
import time
import base64
# 现在有一个需求：想将数据在多个页面之间进行传递
# streamlit为多页面应用提供了一个会话session缓存器，缓存器可以存储页面变量，然后在其他页面当中获取变量进行使用
# 会话存储的变量数据只在当前浏览器中有效，如果把浏览器关闭之后重新打开，那么会话缓存的数据会自动清理
# session会话变量的基本用法
# 存储数据 st.session_state.xxx = 值
# 获取数据 res = st.session_state.xxx
# 获取缓存的用户id和用户账号
user_id = st.session_state.user_id # 用户id就是某一个用户的唯一标识
username = st.session_state.username
message = st.chat_input("请输入你的问题")

st.markdown(
"<center><h1>AI聊天助手 😃</h1></center>",
unsafe_allow_html=True # 允许HTML内容
)
# f"字符串{变量名}"

st.subheader(f"欢迎{username}用户使用")
st.text("既能写文案、读文档，又能脑洞大开、答疑解惑，还能倾听你的故事、感受你的心声。快来和我对话吧！")


# 渲染私人助手界面的时候，应该查询当前用户的历史聊天记录，用于进行界面的渲染
list = dd.query_message_by_user_id(user_id=user_id)
if list:
    #{"message_id":xx,"user_id":xx,message:xxx,role:xxx,message_time:xxx"}
    for msg in list:
        with st.chat_message(msg["role"]):
            st.write(msg["message"])
else:
    # 如果当前用户和AI助手没有任何的聊天记录，需要给他一个默认的助手欢迎语
    with st.chat_message("assistant"):
        st.write("我是你的AI聊天助手，可以回答你的任何问题，请问你有什么问题？")

if message:
    # 展示一个聊天信息 chat_message是一个聊天信息的展示组件，如果组件中增加信息，需要通过如下语法来完成
    with st.chat_message("user"):
        st.write(message)
    # AI回复一下
    with st.chat_message("assistant"):
        # write写出的数据是直接一下全部输出了 一般输出应该都是流式输出
        # write写出一个字符串即可，write_stream中不能放字符串 而应该是一个迭代器
        st.write("AI说:"+ message)

if message:
    st.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    with st.chat_message("user"):
        st.write(message)
    dd.add_message(user_id, message,role="user",message_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    st.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    with st.chat_message("assistant"):
        ai_response="AI说"+message
        st.write(ai_response)
    dd.add_message(user_id, ai_response, role="assistant", message_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

def main_bg(main_bg):
    main_bg_ext = "png"
    st.markdown(
        f"""
         <style>
         .stApp {{
             background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
             background-size: cover
         }}
         </style>
         """,
        unsafe_allow_html=True
    )
# 调用
main_bg('image/5.jpg')