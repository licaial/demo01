import streamlit as st
import re
import data.data as dd
import time
import base64

st.markdown(
"<center><h1>AI聊天助手找回密码🙂</h1></center>",
unsafe_allow_html=True # 允许HTML内容
)

# 设置页面的标题


# 设置注册页面的组件
username = st.text_input("请输入手机号")
password = st.text_input("请输入密码",type="password")
repass = st.text_input("请再次输入密码",type="password")
# 登录按钮
accountFlag = st.button("已完成修改？点击登录")

def account(username,password,repass):
    # 1、校验三个信息是否填写
    if username and password and repass:
        #2、校验用户名的长度是否为11位 并且是否为手机号 正则表达式
        if re.match('^(13|15|17|18|19)[0-9]{9}$', username):
            #3、查看两次密码是否一致 并且密码长度必须大于等于8位
            if password == repass and len(password) >=8:
                # 4、查询数据库是否有重复信息
                if dd.query_user_by_username(username):
                    dd.change_password(username,password)
                    st.success("修改成功")
                    progress_bar = st.empty()
                    for i in range(5):
                        progress_bar.progress(i / 5, '修改中')
                        time.sleep(0.05)

                    with st.spinner('加载中...'):
                        time.sleep(2)
                    st.switch_page("login.py")
                else:
                    st.error("用户已注册，请勿重复注册！")
            else:
                st.error("两次密码不一致或者密码长度字段不足8位")
        else:
            st.error("手机号格式不正确")

    else:
        st.error("请务必填写相关注册信息")


if accountFlag:
    # 如果要跳转到系统的首页，前面不能加pages
    account(username,password,repass)



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
