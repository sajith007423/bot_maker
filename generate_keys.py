import pickle
from pathlib import Path

import streamlit_authenticator as stauth

names = ["Sajith kuttipuravan", "Jyothish Inklampurath"]
usernames = ["sajith", "jyothish"]
passwords = ["sajith@123", "jyothish@123"]

hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)