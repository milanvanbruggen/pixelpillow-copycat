import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="transformers")
import streamlit as st
import torch
from transformers import RobertaTokenizer, RobertaModel

# Model en tokenizer initialiseren
model_name = "roberta-base"
tokenizer = RobertaTokenizer.from_pretrained(model_name)
model = RobertaModel.from_pretrained(model_name)

# Functie om tekst te encoderen met het RoBERTa-model
def run_roberta(text):
    tokens = tokenizer.encode(text, add_special_tokens=True)
    tokens_tensor = torch.tensor([tokens])
    outputs = model(tokens_tensor)
    return outputs

# Streamlit app
st.title("Job Matching App")

# Organisatie input
st.header("Organisatie informatie")
company_type = st.text_input("Wat voor bedrijf is het?")
company_values = st.text_area("Wat zijn de kernwaarden van het bedrijf?")
job_role = st.text_input("Wat is de openstaande functie/rol?")

# Kandidaten input
st.header("Kandidaten")
num_candidates = st.number_input("Aantal kandidaten", min_value=1, step=1, value=1)

candidate_names = []
candidate_motivation_letters = []
candidate_cvs = []

for i in range(num_candidates):
    st.subheader(f"Kandidaat {i+1}")
    candidate_name = st.text_input("Naam van de kandidaat", key=f"candidate_name_{i}")
    candidate_names.append(candidate_name)

    candidate_motivation_letter = st.file_uploader("Motivatiebrief (PDF)", type="pdf", key=f"motivation_letter_{i}")
    candidate_motivation_letters.append(candidate_motivation_letter)

    candidate_cv = st.file_uploader("CV (PDF)", type="pdf", key=f"cv_{i}")
    candidate_cvs.append(candidate_cv)

# Verzendknop
if st.button("Verzend"):
    for i in range(num_candidates):
        st.subheader(f"Resultaten voor kandidaat {i+1}")
        candidate_text = ""
        if candidate_motivation_letters[i] is not None:
            candidate_text += candidate_motivation_letters[i].read().decode()
        if candidate_cvs[i] is not None:
            candidate_text += candidate_cvs[i].read().decode()

        encoded_output = run_roberta(candidate_text)
        # Voer verdere verwerking en scoreberekening uit voor de kandidaat

