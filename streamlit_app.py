import streamlit as st
from transformers import RobertaTokenizer, RobertaModel

# Model laden
model = RobertaModel.from_pretrained("roberta-base")
tokenizer = RobertaTokenizer.from_pretrained("roberta-base")

# Streamlit app configureren
st.set_page_config(page_title="Job Matching App")

# Functie om de berekeningen uit te voeren
def run_roberta(tokens):
    inputs = tokenizer.encode_plus(tokens, add_special_tokens=True, truncation=True, padding=True, return_tensors="pt")
    outputs = model(**inputs)
    return outputs

# UI-componenten weergeven
st.title("Job Matching App")

company_name = st.text_input("Naam van de organisatie")
company_core_values = st.text_input("Kernwaarden van de organisatie")
job_role = st.text_input("Openstaande functie/rol")

candidates = []

# Kandidaat toevoegen aan de lijst
def add_candidate(name, motivation_letter, cv):
    candidates.append({"name": name, "motivation_letter": motivation_letter, "cv": cv})

# Motivatiebrief en CV uploaden voor elke kandidaat
candidate_name = st.text_input("Naam van de kandidaat")
motivation_letter = st.file_uploader("Motivatiebrief uploaden", type="pdf")
cv = st.file_uploader("CV uploaden", type="pdf")

if st.button("Kandidaat toevoegen"):
    if candidate_name and motivation_letter and cv:
        add_candidate(candidate_name, motivation_letter, cv)
        st.success("Kandidaat succesvol toegevoegd!")

# Verzend knop
if st.button("Verzend"):
    if company_name and company_core_values and job_role and candidates:
        st.subheader("Organisatie informatie:")
        st.write("Naam van de organisatie:", company_name)
        st.write("Kernwaarden van de organisatie:", company_core_values)
        st.write("Openstaande functie/rol:", job_role)
        st.subheader("Kandidaten:")
        for candidate in candidates:
            st.write("Naam:", candidate["name"])
            st.write("Motivatiebrief:", candidate["motivation_letter"].name)
            st.write("CV:", candidate["cv"].name)
            st.write("Score:")
            candidate_tokens = candidate["motivation_letter"].read().decode() + " " + candidate["cv"].read().decode()
            outputs = run_roberta(candidate_tokens)
            st.write(outputs)  # Weergeef de scores voor elke kandidaat
    else:
        st.warning("Vul alle velden in en voeg minstens één kandidaat toe.")

