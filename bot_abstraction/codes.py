
import_code='''
import streamlit as st
from streamlit_chat import message
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import PyPDFLoader, DirectoryLoader,CSVLoader,TextLoader,WebBaseLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import CTransformers
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.llms import HuggingFaceHub
'''
webpage_code='''
def load_webpage(url):
    loader = WebBaseLoader(url)
    data = loader.load()
    return data
'''

pdf_doc_code='''
def load_documents_pdf():
    loader = DirectoryLoader('datas/{{data_folder}}/', glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    return documents
'''

csv_doc_code='''
def load_documents_csv():
    loader = DirectoryLoader('datas/{{data_folder}}/', glob="*.csv", loader_cls=CSVLoader)
    documents = loader.load()
    return documents
'''

json_doc_code='''
def load_documents_json():
    loader = DirectoryLoader('datas/{{data_folder}}/', glob='*.json', loader_cls=TextLoader)
    documents = loader.load()
    return documents
'''

md_doc_code='''
def load_documents_md():
    loader = DirectoryLoader('datas/{{data_folder}}/', glob='*.md', loader_cls=TextLoader)
    documents = loader.load()
    return documents
'''

txt_doc_code='''
def load_documents_txt():
    loader = DirectoryLoader('datas/{{data_folder}}/', glob='*.txt', loader_cls=TextLoader)
    documents = loader.load()
    return documents
'''

text_splitter='''
def split_text_into_chunks(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    text_chunks = text_splitter.split_documents(documents)
    return text_chunks
'''

embeddings='''
def create_embeddings():
    embeddings = HuggingFaceEmbeddings(model_name="{{embedding}}", model_kwargs={'device':"cpu"})
    return embeddings
'''

vectorstore='''
def create_vector_store(text_chunks, embeddings):
    vector_store = FAISS.from_documents(text_chunks, embeddings)
    return vector_store
'''

llm='''
def create_llms_model():
    llm = HuggingFaceHub(repo_id="{{llm_name}}", model_kwargs={"temperature":0.5, "max_length":1000})
    return llm
'''

streamlit_code_1='''
if st.session_state["authentication_status"] and st.session_state["username"]=="{{bot_author}}":
    drawing_name = st.session_state["name"]
    st.subheader(f"created by {drawing_name}")
    st.title("{{bot_name}}")
    st.markdown('<style>h1{color: orange; text-align: center;}</style>', unsafe_allow_html=True)
    st.subheader('{{bot_description}}')
    st.markdown('<style>h3{color: red; text-align: center;}</style>', unsafe_allow_html=True)
'''

load_documents_pdf='''
    # loading of documents
    documents = load_documents_pdf()
'''

load_documents_csv='''
    # loading of documents
    documents = load_documents_csv()
'''

load_documents_json='''
    # loading of documents
    documents = load_documents_json()
'''

load_documents_md='''
    # loading of documents
    documents = load_documents_md()
'''
load_documents_txt='''
    # loading of documents
    documents = load_documents_txt()
'''

load_webpage_code='''
    documents = load_webpage("{{url}}")
'''


streamlit_code_2='''
    # Split text into chunks
    text_chunks = split_text_into_chunks(documents)

    # Create embeddings
    embeddings = create_embeddings()

    # Create vector store
    vector_store = create_vector_store(text_chunks, embeddings)

    # Create LLMS model
    llm = create_llms_model()

    # Initialize conversation history
    if 'history' not in st.session_state:
        st.session_state['history'] = []

    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["Hello! Ask me something"]

    if 'past' not in st.session_state:
        st.session_state['past'] = ["Hey! 👋"]

    # Create memory
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    # Create chain
    chain = ConversationalRetrievalChain.from_llm(llm=llm, chain_type='stuff',
                                                retriever=vector_store.as_retriever(search_kwargs={"k": 2}),
                                                memory=memory)

    # Define chat function
    def conversation_chat(query):
        result = chain({"question": query, "chat_history": st.session_state['history']})
        st.session_state['history'].append((query, result["answer"]))
        return result["answer"]

    # Display chat history
    reply_container = st.container()
    container = st.container()

    with container:
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_input("Question:", placeholder="Ask something", key='input')
            submit_button = st.form_submit_button(label='Send')

        if submit_button and user_input:
            output = conversation_chat(user_input)
            st.session_state['past'].append(user_input)
            st.session_state['generated'].append(output)

    if st.session_state['generated']:
        with reply_container:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="thumbs")
                message(st.session_state["generated"][i], key=str(i), avatar_style="fun-emoji")
else:
    st.subheader("This bot is owned by another user")
    st.markdown('<style>h3{color: green; text-align: center;}</style>', unsafe_allow_html=True)

'''
