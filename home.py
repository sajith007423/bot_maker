# pip install pandas openpyxl
import streamlit as st  # pip install streamlit
import streamlit_authenticator as stauth  # pip install streamlit-authenticator
import yaml
from yaml.loader import SafeLoader
from dotenv import  dotenv_values,set_key

def update_env_variable(env_file_path, key, new_value):
    # Load the current environment variables from the .env file
    env_vars = dotenv_values(env_file_path)
    # Update the specified variable
    set_key(env_file_path, key, new_value)

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

name,authentication_status,username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:
    st.title("Homepage")
    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome {name}")
    new_api=st.text_input("name of new bot:")
    if st.button("Apply New HF API"):
        env_file_path = '.env'
        variable_to_update = 'HUGGINGFACEHUB_API_TOKEN'
        new_value = new_api
        update_env_variable(env_file_path, variable_to_update, new_value)