import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity
from transformers import BertTokenizer, BertModel
import torch

# Load pre-trained model tokenizer (vocabulary)
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
# Load pre-trained model (weights)
model = BertModel.from_pretrained('bert-base-uncased')

# Set the model in evaluation mode to deactivate the DropOut modules
model.eval()

# Maximum sequence length
max_length = 512

# Function to encode input
def encode_input(text):
    tokenized_text = tokenizer.tokenize(text)
    tokenized_text = tokenized_text[:max_length]  # Truncate or pad to max_length
    indexed_tokens = tokenizer.convert_tokens_to_ids(tokenized_text)
    tokens_tensor = torch.tensor([indexed_tokens])
    return tokens_tensor

# Function to run BERT model
def run_bert(tokens_tensor):
    with torch.no_grad():
        outputs = model(tokens_tensor)
        pooled_output = outputs.pooler_output
    return pooled_output

# Function to calculate similarity score
def calculate_similarity(candidate_encoded, company_encoded):
    score = cosine_similarity(candidate_encoded.detach().numpy(), company_encoded.detach().numpy())
    return score

# Streamlit app
st.title('Job Matching App')

# Organisation input
st.header('Organisation Information')
org_description = st.text_area("What kind of company is it?")
org_values = st.text_area("What are the core values?")
org_role = st.text_area("What is the open position/role?")

# Candidates input
st.header('Candidates Information')
num_candidates = st.number_input('Number of candidates', min_value=1, value=1, step=1)

candidate_info = []
for i in range(num_candidates):
    with st.expander(f"Candidate {i+1}"):
        name = st.text_input(f"Candidate {i+1} Name")
        cv = st.file_uploader(f"Upload CV for candidate {i+1}", type=['txt', 'pdf'])
        motivation = st.file_uploader(f"Upload Motivation Letter for candidate {i+1}", type=['txt', 'pdf'])
        candidate_info.append({
            "name": name,
            "cv": cv,
            "motivation": motivation
        })

# Process candidate information
for candidate in candidate_info:
    st.subheader(f"Matching for {candidate['name']}")
    candidate_text = ""
    if candidate["cv"] is not None:
        candidate_text += candidate["cv"].read().decode(errors='ignore')
    candidate_text += " "
    if candidate["motivation"] is not None:
        candidate_text += candidate["motivation"].read().decode(errors='ignore')

    company_text = org_description + " " + org_values + " " + org_role

    candidate_tokens = encode_input(candidate_text)
    company_tokens = encode_input(company_text)

    candidate_tokens = candidate_tokens.to(torch.long)  # Convert to long tensor
    company_tokens = company_tokens.to(torch.long)  # Convert to long tensor

    candidate_encoded = run_bert(candidate_tokens)
    company_encoded = run_bert(company_tokens)

    similarity_score = calculate_similarity(candidate_encoded, company_encoded)
