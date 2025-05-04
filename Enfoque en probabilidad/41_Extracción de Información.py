# 📚 Importamos spaCy, una librería popular para Procesamiento de Lenguaje Natural
import spacy

# 🚀 Cargamos un modelo preentrenado en español
nlp = spacy.load('es_core_news_sm')  # Si quieres inglés, usa 'en_core_web_sm'

# 📄 Texto del cual queremos extraer información
texto = "Juan Pérez trabaja en Google y vive en Madrid. María fue a Barcelona en 2023."

# 🧠 Procesamos el texto
doc = nlp(texto)

# 🕵️‍♂️ Extraemos las entidades nombradas
print("🔎 Entidades encontradas:")
for ent in doc.ents:
    print(f"Texto: {ent.text}, Tipo: {ent.label_}")
