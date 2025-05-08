import json
from rapidfuzz import process
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# 📂 Cargar datos desde el archivo JSON
with open("sombras_traducidas.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Crear lista de nombres para búsqueda fuzzy
names = [entry["name"] for entry in data]

# ⚙️ Cargar TinyLlama
tokenizer = AutoTokenizer.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0")
model = AutoModelForCausalLM.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0", device_map="auto")
llama_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer)

# 🔍 Función para buscar enemigos y generar respuesta
def search_enemy(user_input):
    match, score, idx = process.extractOne(user_input, names)
    
    if score > 70:  # Umbral de similitud
        enemy = data[idx]
        prompt = (
    f"Enemigo: {enemy['name']}\n"
    f"Nivel: {enemy['level']}\n"
    f"HP: {enemy['hp']}\n"
    f"SP: {enemy['sp']}\n"
    f"Debilidades: {', '.join(enemy['weaknesses'])}\n"
    f"Ubicación: {enemy['location']}\n"
    f"Objetos que deja: {enemy['drop_items']}\n"
    f"=== Fin del enemigo ===\n"
    f"Describe este enemigo como si fueras un experto en videojuegos:"
)
        result = llama_pipeline(prompt, max_new_tokens=100, do_sample=False)[0]["generated_text"]
 
        return result
    else:
        return "No encontré un enemigo con un nombre similar. ¿Puedes revisar si escribiste bien?"

# ▶️ Ejecutar
if __name__ == "__main__":
    while True:
        user_query = input("Nombre del enemigo ('salir' para terminar): ")
        if user_query.lower() == "salir":
            break
        print(search_enemy(user_query))

