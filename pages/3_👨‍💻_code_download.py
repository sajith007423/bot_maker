import streamlit as st
import os
import shutil
from zipfile import ZipFile


# You can continue with the rest of your Streamlit app...

def list_files_starting_with_alphabet(directory_path):
    try:
        # List all files in the directory
        files = [f[:-len(os.path.splitext(f)[1])] for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f)) and f[0].isalpha()]

        # Print the list of files without extensions
        print(f'Files starting with alphabets (without extensions) in directory "{directory_path}":')
        for file in files:
            print(file)

        return files
    except OSError as e:
        print(f"Error: {e}")
        return []


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
    directory_path = 'pages'
    alphabet_files = list_files_starting_with_alphabet(directory_path)
    print('List of files:', alphabet_files)
    bot_selected= st.selectbox("Choose bot to upload", alphabet_files)
    # Example usage
    items_to_zip = ["datas/"+bot_selected,"pages/"+bot_selected+".py"]
    print(items_to_zip)
    if st.button("Download ZIP File"):
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
    
    


    
    

