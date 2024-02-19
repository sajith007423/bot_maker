# pip install pandas openpyxl
import os
import streamlit as st  # pip install streamlit
import streamlit_authenticator as stauth  # pip install streamlit-authenticator
import yaml
from yaml.loader import SafeLoader

st.set_page_config(page_title="bot_maker", page_icon=":bot:", layout="wide")

with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

#name,authentication_status,username = authenticator.login("Login", "main")
try:
    email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(preauthorization=False)
    if email_of_registered_user:
        st.success('User registered successfully')
        with open('./config.yaml', 'w') as file:
            yaml.dump(config, file, default_flow_style=False)
except Exception as e:
    st.error(e)