# pip install pandas openpyxl
import os
import streamlit as st  # pip install streamlit
import streamlit_authenticator as stauth  # pip install streamlit-authenticator
import yaml
import shutil
from yaml.loader import SafeLoader

def read_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data

def extract_bots_list(yaml_data, username):
    # Check if the specified username exists in the "bots" section
    if 'bots' in yaml_data and username in yaml_data['bots']:
        return yaml_data['bots'][username]
    else:
        return []
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
st.title("BOT MAKER")
st.markdown('<style>h1{color: white; text-align: center;}</style>', unsafe_allow_html=True)
#name,authentication_status,username = authenticator.login("Login", "main")
name, authentication_status, username = authenticator.login(
    fields={"Form name": "Login", "Username": "Username", "Password": "Password", "Login": "Login"},
    location="main"
)

# yaml_path = 'config.yaml'

if authentication_status == False:
    st.error("Username/password is incorrect")
    # st.title("Signup")
    # new_username = st.text_input("Enter a username")
    # new_name = st.text_input("Enter a name")
    # new_email = st.text_input("Enter an email")
    # new_password = ['']
    # new_password[0] = st.text_input("Enter a password")
    # if st.button("create a new account"):
    #     print(stauth.Hasher(new_password).generate())
    #     add_username(yaml_path, new_username, new_email, new_name, stauth.Hasher(new_password).generate())

if authentication_status == None:
    st.warning("Please enter your username and password")
    # st.title("Signup")
    # new_username = st.text_input("Enter a username")
    # new_name = st.text_input("Enter a name")
    # new_email = st.text_input("Enter an email")
    # new_password = ['']
    # new_password[0] = st.text_input("Enter a password")
    # if st.button("create a new account"):
    #     print(stauth.Hasher(new_password).generate())
    #     add_username(yaml_path, new_username, new_email, new_name, stauth.Hasher(new_password).generate())

if authentication_status:
    st.subheader("Homepage")
    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome {name}")
    hf_api = st.text_input("Enter a Huggingface API:")
    if st.button("Put or change API"):
        os.environ["HUGGINGFACEHUB_API_TOKEN"] = hf_api
    if st.button("Dispense your bots"):
        def copy_files(source_folder, destination_folder, file_list):
            """
            Copies a list of files from one folder to another.

            Args:
                source_folder: The path to the source folder.
                destination_folder: The path to the destination folder.
                file_list: A list of filenames to copy.
            """
            for filename in file_list:
                source_path = os.path.join(source_folder, filename+".py")
                dest_path = os.path.join(destination_folder)

                try:
                    shutil.copy2(source_path, dest_path)  # Preserves file metadata
                    print(f"Copied {filename} from {source_path} to {dest_path}")
                except OSError as e:
                    print(f"Error copying {filename}: {e}")

        # Example usage
        source_folder = "allbots/"
        destination_folder = "pages/"
        file_path = './config.yaml'  # Replace with the actual path to your YAML file
        username = st.session_state["username"]
        # Read YAML file
        yaml_data = read_yaml(file_path)
        file_list = extract_bots_list(yaml_data,username)

        copy_files(source_folder, destination_folder, file_list)
    if st.button("retain your bots"):
        def delete_files(folder_path, file_list):
            """
            Deletes a list of files from a specified folder.

            Args:
                folder_path: The path to the folder containing the files.
                file_list: A list of filenames to delete.
            """
            for filename in file_list:
                full_path = os.path.join(folder_path,filename+".py")

                if os.path.isfile(full_path):  # Check if it's a file, not a folder
                    try:
                        os.remove(full_path)
                        print(f"Deleted {filename} from {folder_path}")
                    except OSError as e:
                        print(f"Error deleting {filename}: {e}")
                else:
                    print(f"Warning: '{filename}' is not a file, skipping deletion.")


        # Example usage
        folder_path = "./pages"
        file_path = './config.yaml'  # Replace with the actual path to your YAML file
        username = st.session_state["username"]
        # Read YAML file
        yaml_data = read_yaml(file_path)
        file_list = extract_bots_list(yaml_data,username)
        delete_files(folder_path, file_list)
        
        
    if st.button("Delete chat history"):
        st.session_state['history'] = []
        st.session_state['generated'] = ["Hello! Ask me something"]
        st.session_state['past'] = ["Hey! 👋"]
