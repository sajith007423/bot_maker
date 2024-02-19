import streamlit as st
import os
import shutil
from bot_abstraction.codes import *
import sys
# Change console encoding to utf-8
sys.stdout.reconfigure(encoding='utf-8')
import yaml

def read_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data

def write_yaml(file_path, data):
    with open(file_path, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)

def add_bot(file_path, username, bot_name):
    # Read YAML file
    yaml_data = read_yaml(file_path)

    # Check if the username exists, if not, create an empty list
    if username not in yaml_data['bots']:
        yaml_data['bots'][username] = []

    # Add the bot to the specified username
    yaml_data['bots'][username].append(bot_name)

    # Write the updated data back to the YAML file
    write_yaml(file_path, yaml_data)


def create_directory(directory_path):
    try:
        os.makedirs(directory_path)
        print(f"Directory '{directory_path}' created successfully.")
    except OSError as error:
        print(f"Failed to create directory '{directory_path}': {error}")


def save_uploaded_files(uploaded_files, target_directory):
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    for uploaded_file in uploaded_files:
        file_path = os.path.join(target_directory, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"File saved to: {file_path}")



def move_file_to_directory(source_path, destination_directory):
    try:
        # Move the file to the destination directory
        shutil.move(source_path, destination_directory)
        print(f"File moved successfully from {source_path} to {destination_directory}.")
    except Exception as e:
        print(f"Error moving file: {e}")

if st.session_state["authentication_status"]:
    st.title("Create a new bot")
    name_of_bot=st.text_input("name of new bot")
    description_of_bot=st.text_input("description of new bot")
    
    embedding_selected= st.selectbox("Choose an embedding", ["sentence-transformers/all-MiniLM-L6-v2","sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"])
    llm_selected= st.selectbox("Choose a llm", ["mistralai/Mistral-7B-Instruct-v0.2","google/flan-t5-xxl","mistralai/Mixtral-8x7B-Instruct-v0.1"])
    bot_type = st.selectbox("Choose bot type", ["webpage","document"])
    if(bot_type=="document"):
        doc_type = st.selectbox("Choose file type", ["pdf","csv","json","md","txt"])
        documents= st.file_uploader("Upload your documents to chat", accept_multiple_files=True,type=doc_type)
        if st.button("create document bot"):
            print(name_of_bot)
            print(doc_type)
            
            directory_name = 'datas/'+name_of_bot
            # Specify the full path where you want to create the directory
            full_directory_path = os.path.join(os.getcwd(), directory_name)
            # Call the function to create the directory
            create_directory(full_directory_path)
            if documents is not None:
                # Save the uploaded file to the target directory
                save_uploaded_files(documents, directory_name)
            
            # Open a file in append mode
            with open(name_of_bot+".py", 'a',encoding='utf-8') as file:
                file.write('\n'+import_code)
                if(doc_type=="pdf"):
                    file.write('\n'+pdf_doc_code.replace("{{data_folder}}",name_of_bot))
                elif(doc_type=="csv"):
                    file.write('\n'+csv_doc_code.replace("{{data_folder}}",name_of_bot))
                elif(doc_type=="json"):
                    file.write('\n'+json_doc_code.replace("{{data_folder}}",name_of_bot))
                elif(doc_type=="txt"):
                    file.write('\n'+txt_doc_code.replace("{{data_folder}}",name_of_bot))
                else:
                    file.write('\n'+md_doc_code.replace("{{data_folder}}",name_of_bot))
                file.write('\n'+text_splitter)
                file.write('\n'+embeddings.replace("{{embedding}}",embedding_selected))
                file.write('\n'+vectorstore)
                file.write('\n'+llm.replace("{{llm_name}}",llm_selected))
                initial_code=streamlit_code_1.replace("{{bot_name}}",name_of_bot)
                initial_code=initial_code.replace("{{bot_description}}",description_of_bot)
                initial_code=initial_code.replace("{{bot_author}}",st.session_state["username"])
                file.write('\n'+initial_code)
                if(doc_type=="pdf"):
                    file.write('\n'+load_documents_pdf)
                elif(doc_type=="csv"):
                    file.write('\n'+load_documents_csv)
                elif(doc_type=="json"):
                    file.write('\n'+load_documents_json)
                elif(doc_type=="txt"):
                    file.write('\n'+load_documents_txt)
                else:
                    file.write('\n'+load_documents_md)
                file.write('\n'+streamlit_code_2)
                file.close()
            
            source_file_path = name_of_bot+".py"
            destination_directory = "allbots"
            # Move the file to the destination directory
            move_file_to_directory(source_file_path, destination_directory)
            add_bot('./config.yaml', st.session_state["username"], name_of_bot)
    else:
        weblink= st.text_input("provide a link", placeholder="paste a link here")
        if st.button("create weblink bot"):
            print(name_of_bot)
            print(weblink)
            
            # Open a file in append mode
            with open(name_of_bot+".py", 'a',encoding='utf-8') as file:
                file.write('\n'+import_code)
                file.write('\n'+webpage_code)
                file.write('\n'+text_splitter)
                file.write('\n'+embeddings.replace("{{embedding}}",embedding_selected))
                file.write('\n'+vectorstore)
                file.write('\n'+llm.replace("{{llm_name}}",llm_selected))
                initial_code=streamlit_code_1.replace("{{bot_name}}",name_of_bot)
                initial_code=initial_code.replace("{{bot_description}}",description_of_bot)
                initial_code=initial_code.replace("{{bot_author}}",st.session_state["username"])
                file.write('\n'+initial_code)
                file.write('\n'+load_webpage_code.replace("{{url}}",weblink))
                file.write('\n'+streamlit_code_2)
                file.close()
            
            source_file_path = name_of_bot+".py"
            destination_directory = "allbots"
            # Move the file to the destination directory
            move_file_to_directory(source_file_path, destination_directory)
            add_bot('./config.yaml', st.session_state["username"], name_of_bot)
                
        

    
    