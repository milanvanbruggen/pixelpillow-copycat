import streamlit as st
import torch
from transformers import BertTokenizer, BertModel

# Load pre-trained model tokenizer (vocabulary)
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
# Load pre-trained model (weights)
model = BertModel.from_pretrained('bert-base-uncased')

# Set the model in evaluation mode to deactivate the DropOut modules
model.eval()

# Function to encode input
def encode_input(text):
    tokenized_text = tokenizer.tokenize(text)
    indexed_tokens = tokenizer.convert_tokens_to_ids(tokenized_text)
    tokens_tensor = torch.tensor([indexed_tokens])
    return tokens_tensor

# Function to run BERT model
def run_bert(tokens_tensor):
    with torch.no_grad():
        outputs = model(tokens_tensor)
        encoded_layers = outputs[0]
    return encoded_layers

# Streamlit app
st.title('Job Matching App')

st.header('Organisation Info')
company_type = st.text_input("What type of company is it?")
core_values = st.text_input("What are the core values of the company?")
role = st.text_input("What is the open position?")

st.header('Candidate Info')
motivation_letter = st.text_area("Please paste the motivation letter here:")
uploaded_cv = st.file_uploader("Please upload the CV:", type=['txt'])

if uploaded_cv is not None:
    cv_text = uploaded_cv.read().decode()
    st.text(cv_text)
else:
    cv_text = ""

company_info = company_type + " " + core_values + " " + role
candidate_info = motivation_letter + " " + cv_text

company_tokens = encode_input(company_info)
candidate_tokens = encode_input(candidate_info)

company_encoded = run_bert(company_tokens)
candidate_encoded = run_bert(candidate_tokens)

# TODO: Compare company_encoded and candidate_encoded to perform matching
