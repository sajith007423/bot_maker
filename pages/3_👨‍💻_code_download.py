import streamlit as st
import os
import shutil
from zipfile import ZipFile
import yaml

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




# You can continue with the rest of your Streamlit app...


def zip_folders_and_files(zip_filename, items_to_zip):
    with ZipFile(zip_filename, 'w') as zip_file:
        for item in items_to_zip:
            if os.path.isfile(item):
                # Add individual file to the zip archive
                zip_file.write(item, os.path.basename(item))
            elif os.path.isdir(item):
                # Add entire directory to the zip archive
                shutil.make_archive(item, 'zip', item)
                zip_file.write(item + '.zip', os.path.basename(item + '.zip'))


if st.session_state["authentication_status"]:
    file_path = './config.yaml'  # Replace with the actual path to your YAML file
    username = st.session_state["username"]
    # Read YAML file
    yaml_data = read_yaml(file_path)
    # Extract the list of bots for the specified username
    # Display the extracted list
    print(f"Bots list for {username}:")
    directory_path = 'allbots'
    bot_list = extract_bots_list(yaml_data, username)
    print('List of files:', bot_list)
    bot_selected= st.selectbox("Choose bot to upload", bot_list)
    # Example usage
    items_to_zip = ["datas/"+bot_selected,"allbots/"+bot_selected+".py"]
    print(items_to_zip)
    if st.button("compress to ZIP File"):
        # Create a temporary directory to store the ZIP file
        temp_dir = "temp_zips"
        os.makedirs(temp_dir, exist_ok=True)

        zip_filename = os.path.join(temp_dir, bot_selected+".zip")
        zip_folders_and_files(zip_filename, items_to_zip)

        with open(zip_filename, 'rb') as f:
            zip_content = f.read()

        # Display the download button
        st.download_button(
            label="Click to Download ZIP File",
            data=zip_content,
            key='download_button',
            file_name=bot_selected+".zip"
        )
    
    


    
    

