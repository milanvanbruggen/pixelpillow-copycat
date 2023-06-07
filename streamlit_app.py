import streamlit as st
from transformers import BertTokenizer, BertModel
import torch

# Laad het BERT-model en tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

def match_vacature_en_kandidaat(vacature, kandidaat):
    inputs = tokenizer.encode_plus(vacature, kandidaat, add_special_tokens=True, return_tensors='pt')

    with torch.no_grad():
        outputs = model(**inputs)

    vacature_embedding = outputs.last_hidden_state[0][0]
    kandidaat_embedding = outputs.last_hidden_state[0][1]

    similarity_score = torch.cosine_similarity(vacature_embedding, kandidaat_embedding, dim=0)
    return similarity_score.item()

def main():
    st.title('Matchingsapplicatie')

    # Bedrijfsinformatie
    st.header('Bedrijfsinformatie')
    bedrijf = st.text_input('Bedrijf')
    kernwaarden = st.text_input('Kernwaarden')
    gezochte_functie = st.text_input('Gezochte functie')

    # Kandidaten
    st.header('Kandidaten')
    num_kandidaten = st.number_input('Aantal kandidaten', min_value=1, max_value=10, value=1, step=1)

    for i in range(num_kandidaten):
        st.subheader(f'Kandidaat {i+1}')
        naam = st.text_input('Naam')
        motivatiebrief = st.text_area('Motivatiebrief')
        werkervaring = st.text_area('Werkervaring')

        if st.button('Match'):
            score = match_vacature_en_kandidaat(gezochte_functie, werkervaring)
            st.write(f'Matchingscore voor Kandidaat {i+1}: {score}')

if __name__ == '__main__':
    main()
