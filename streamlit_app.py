import streamlit as st
import torch
from transformers import RobertaTokenizer, RobertaModel

# Model laden
model_name = 'roberta-base'
tokenizer = RobertaTokenizer.from_pretrained(model_name)
model = RobertaModel.from_pretrained(model_name)

# Streamlit app
st.title("Job Matching App")

# Organisatie input
st.header("Organisatie informatie")
company_name = st.text_input("Wat is de naam van het bedrijf?")
core_values = st.text_area("Wat zijn de kernwaarden van het bedrijf?")
job_role = st.text_input("Wat is de openstaande functie/rol?")

# Kandidaat input
st.header("Kandidaten informatie")
num_candidates = st.number_input("Aantal kandidaten", min_value=1, value=1, step=1)

candidates = []
for i in range(num_candidates):
    st.subheader(f"Kandidaat {i+1}")
    candidate_name = st.text_input("Naam van de kandidaat")
    cv_file = st.file_uploader("Upload CV (PDF)", type="pdf")
    motivation_file = st.file_uploader("Upload motivatiebrief (PDF)", type="pdf")
    if candidate_name and cv_file and motivation_file:
        candidate = {
            "name": candidate_name,
            "cv": cv_file,
            "motivation": motivation_file
        }
        candidates.append(candidate)

# Kandidaten vergelijken
if st.button("Match kandidaten"):
    for candidate in candidates:
        st.subheader(f"Match voor kandidaat: {candidate['name']}")
        cv_text = candidate["cv"].read().decode()
        motivation_text = candidate["motivation"].read().decode()

        # Tokenizen van de tekst
        inputs = tokenizer.encode_plus(
            cv_text,
            motivation_text,
            add_special_tokens=True,
            max_length=512,
            truncation=True,
            padding="max_length",
            return_tensors="pt"
        )
        input_ids = inputs["input_ids"]
        attention_mask = inputs["attention_mask"]

        # Model inferentie
        with torch.no_grad():
            outputs = model(input_ids, attention_mask)
            embeddings = outputs.last_hidden_state[:, 0, :]

        # Doe iets met de embeddings, bijvoorbeeld bereken de cosine similarity met de organisatie embeddings
        # ... je code hier ...

        # Toon de resultaten
        st.write("Score: ...")  # Vul hier de score in op basis van de embeddings
