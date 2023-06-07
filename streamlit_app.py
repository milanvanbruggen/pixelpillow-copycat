from transformers import BertTokenizer, BertModel
import torch

# Laad het BERT-model en tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# Functie voor het matchen van vacature en kandidaat
def match_vacature_en_kandidaat(vacature, kandidaat):
    # Tokenize de vacature en kandidaat
    inputs = tokenizer.encode_plus(vacature, kandidaat, add_special_tokens=True, return_tensors='pt')

    # Genereer de embeddings
    with torch.no_grad():
        outputs = model(**inputs)

    # Haal de laatste verborgen toestand op
    vacature_embedding = outputs.last_hidden_state[0][0]  # Embedding voor de vacature
    kandidaat_embedding = outputs.last_hidden_state[0][1]  # Embedding voor de kandidaat

    # Bereken de cosinusgelijkenis tussen de embeddings
    similarity_score = torch.cosine_similarity(vacature_embedding, kandidaat_embedding, dim=0)

    return similarity_score.item()

# Voorbeeldgebruik
vacaturetekst = "Wij zoeken een ervaren softwareontwikkelaar met kennis van Python en ervaring met het bouwen van webtoepassingen."
kandidaattekst = "Ik ben een ervaren softwareontwikkelaar met sterke vaardigheden in Python en uitgebreide ervaring in het bouwen van webtoepassingen."

score = match_vacature_en_kandidaat(vacaturetekst, kandidaattekst)
print("Matchingscore:", score)
