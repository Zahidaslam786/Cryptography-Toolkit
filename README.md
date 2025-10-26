Classical Cryptography Toolkit

This is a web application built with Python and Streamlit that provides a graphical user interface (GUI) for encrypting and decrypting text using various classical ciphers.

Features

Monoalphabetic Ciphers: Caesar, Affine

Polyalphabetic Ciphers: Vigenere, Playfair, Hill

Transposition Ciphers: Rail Fence, Row Transposition

Mechanical Ciphers: An Enigma-like Rotor Machine simulation

The application provides a clean interface for selecting ciphers, entering keys, and processing text, along with explanations and visualizations for each algorithm.

How to Run

Prerequisites: Make sure you have Python installed on your system.

Set up a Virtual Environment (Recommended):

## --> Create the environment
python -m venv venv

# Activate it
## --> On Windows:
.\venv\Scripts\activate

# On macOS/Linux:
<!-- source venv/bin/activate -->


## --> Install Dependencies:
From the project's root directory (Cryptography_Toolkit_App/), run the following command to install the required libraries:

pip install -r requirements.txt


# --> Run the Streamlit App:
Once the dependencies are installed, run the main application file:

streamlit run app.py


Open your web browser and navigate to the local URL provided in the terminal (usually http://localhost:8501).

#### For once:
python -m venv venv

./venv/Scripts/python.exe -m pip install -r requirements.txt

./venv/Scripts/python.exe -c "import streamlit as st; print(st.__version__)"

./venv/Scripts/python.exe -m streamlit run app.py


### For AES Algorithm Install new libraray

./venv/Scripts/python.exe -m pip install pycryptodome   