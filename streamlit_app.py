import torch
from sklearn.metrics.pairwise import cosine_similarity
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

def calculate_score(encoded1, encoded2):
    # Calculate cosine similarity
    score = cosine_similarity(encoded1.detach().numpy(), encoded2.detach().numpy())
    return score

def calculate_experience_score(candidate_encoded, job_encoded):
    # Placeholder function - replace with your own logic
    return calculate_score(candidate_encoded, job_encoded)

def calculate_role_score(candidate_encoded, job_encoded):
    # Placeholder function - replace with your own logic
    return calculate_score(candidate_encoded, job_encoded)

def calculate_culture_score(candidate_encoded, job_encoded):
    # Placeholder function - replace with your own logic
    return calculate_score(candidate_encoded, job_encoded)

# Streamlit app
st.title('Job Matching App')

st.header('Organisation Info')
company_type = st.text_input("What type of company is it?")
core_values = st.text_input("What are the core values of the company?")
role = st.text_input("What is the open position?")

st.header('Candidate Info')
candidate_name = st.text_input("Candidate's name:")
uploaded_letter = st.file_uploader("Please upload the motivation letter:", type=['txt'])
uploaded_cv = st.file_uploader("Please upload the CV:", type=['txt'])

if uploaded_letter is not None:
    letter_text = uploaded_letter.read().decode()
else:
    letter_text = ""

if uploaded_cv is not None:
    cv_text = uploaded_cv.read().decode()
else:
    cv_text = ""

company_info = company_type + " " + core_values + " " + role
candidate_info = letter_text + " " + cv_text

company_tokens = encode_input(company_info)
candidate_tokens = encode_input(candidate_info)

company_encoded = run_bert(company_tokens)
candidate_encoded = run_bert(candidate_tokens)

experience_score = calculate_experience_score(candidate_encoded, company_encoded)
role_score = calculate_role_score(candidate_encoded, company_encoded)
culture_score = calculate_culture_score(candidate_encoded, company_encoded)

# Display scores
st.header('Match Scores for ' + candidate_name)
st.write('Experience Score: ', experience_score)
st.write('Role Score: ', role_score)
st.write('Culture Score: ', culture_score)
