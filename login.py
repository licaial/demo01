import streamlit as st
import data.data as dd
import time
import base64
# 设置页面的标签页的名字和icon
st.markdown(
"<center><h1>AI聊天助手登录页面🙂</h1></center>",
unsafe_allow_html=True # 允许HTML内容
)


# 设置页面的组件的，两个输入框+一个登录按钮+一个去注册按钮
username = st.text_input("请输入用户名",)
password = st.text_input("请输入密码",type="password")
loginFlag = st.button("登录")

# 注册按钮
registerFlag = st.button("没有账号？点击注册")
accountFlag = st.button("忘记密码")

# 登录函数
def login(username,password):
    # 先检验数据是否为空，根据用户名和密码去校验数据是否存在
    if  username and password:
        # 校验的时候只需要根据用户名查询即可，如果用户名存在，根据获取回来的密码和传入的密码做比对 登录成功显示登录成功，延迟两秒到首页（AI助手聊天页面）
        # select * from sys_user where username=?
        result = dd.query_user_by_username(username)
        if result is None:
            st.error("用户不存在，请前往注册",width=100)
        else:
            if result["password"] == password:
                st.success("登录成功！")
                progress_bar = st.empty()
                for i in range(5):
                    progress_bar.progress(i / 5, '登录中')
                    time.sleep(0.05)

                with st.spinner('加载中...'):
                    time.sleep(2)
                # 登录成功 跳转页面之前 需要把当前用户的用户id和账号缓存起来，去首页使用
                st.session_state.user_id = result["user_id"]
                st.session_state.username = result["username"]
                st.switch_page("pages/chatbot.py")
            else:
                st.error("用户存在，密码不正确！")
    else:
        st.error("请填写账号和密码！")

if loginFlag:
    login(username,password)

# 注册按钮点击之后应该跳转到注册页面
if registerFlag:
    # streamlit中有一个函数叫做swtich_page("py页面文件的路径") py文件必须位于项目的pages目录下
    st.switch_page("pages/register.py")

if accountFlag:
    st.switch_page("pages/account.py")

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
main_bg('image/sss.png')