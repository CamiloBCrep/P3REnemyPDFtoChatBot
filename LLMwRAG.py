import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from rapidfuzz import process

# Cargar datos
with open("sombras_traducidas.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Preparar textos
def format_enemy(enemy):
    return (
        f"Nombre: {enemy['name']}\n"
        f"Nivel: {enemy['level']}\n"
        f"HP: {enemy['hp']}\n"
        f"SP: {enemy['sp']}\n"
        f"Debilidades: {', '.join(enemy['weaknesses'])}\n"
        f"Ubicación: {enemy.get('location', 'Desconocido')}\n"  # Usar 'Desconocido' si no existe
        f"Objetos: {enemy.get('drop_items', 'Desconocido')}\n"  # Usar 'Desconocido' si no existe
    )

texts = [format_enemy(e) for e in data]
enemy_names = [e["name"] for e in data]

# Embeddings
model_embed = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model_embed.encode(texts, show_progress_bar=True)
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

# TinyLlama pipeline
model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)
qa_model = pipeline("text-generation", model=model, tokenizer=tokenizer)

# Función para corregir nombre con un umbral más bajo
def corregir_nombre(nombre_input, nombres_enemigos, umbral=60):
    match = process.extractOne(nombre_input, nombres_enemigos, score_cutoff=umbral)
    print(f"Corregido: {nombre_input} -> {match}")  # Depuración para ver el nombre corregido
    return match[0] if match else None

# Función para responder
def responder(pregunta, top_k=1):
    print(f"Pregunta recibida: {pregunta}")  # Depuración de la entrada

    # Buscar enemigo mencionado
    nombre_candidato = corregir_nombre(pregunta, enemy_names)
    if not nombre_candidato:
        return "No encontré un enemigo con un nombre similar. ¿Puedes revisar si escribiste bien o intenta con otro nombre?"
    
    print(f"Enemigo corregido: {nombre_candidato}")  # Depuración del enemigo corregido

    # Embedding y búsqueda
    emb_pregunta = model_embed.encode([pregunta])
    distancias, indices = index.search(np.array(emb_pregunta), top_k)

    if top_k > 1:
        mejor_indice = np.argmin(distancias)
    else:
        mejor_indice = 0

    contexto = texts[indices[0][mejor_indice]]

    # Prompt especial para TinyLlama
    prompt = (
        f"<|system|>\nEres un experto en videojuegos. Usa solo el contexto entregado.\n"
        f"<|user|>\nContexto:\n{contexto}\n\nPregunta: {pregunta}\n"
        f"<|assistant|>"
    )

    # Respuesta del modelo
    salida = qa_model(prompt, max_new_tokens=120, do_sample=False, temperature=0.7)[0]["generated_text"]
    
    # Asegurarnos de que la respuesta se extrae correctamente
    if "<|assistant|>" in salida:
        respuesta = salida.split("<|assistant|>")[-1].strip()
    else:
        respuesta = salida.strip()

    return respuesta


# CLI
if __name__ == "__main__":
    print("Bot RAG activado con TinyLlama. Pregunta por enemigos ('salir' para terminar)")
    while True:
        q = input("Tu pregunta: ")
        if q.lower() == "salir":
            break
        print(responder(q))
#aún no funciona**