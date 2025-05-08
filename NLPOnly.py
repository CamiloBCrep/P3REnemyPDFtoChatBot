import json
from rapidfuzz import fuzz

def buscar_sombra(nombre_buscado, sombras, umbral=60):
    print(f"\n🔍 Buscando coincidencias para: **{nombre_buscado}** (umbral: {umbral}%)\n")

    coincidencias = []
    for sombra in sombras:
        nombre_actual = sombra["name"]
        puntuacion = fuzz.ratio(nombre_buscado.lower(), nombre_actual.lower())
        if puntuacion >= umbral:
            coincidencias.append((nombre_actual, puntuacion, sombra))

    if coincidencias:
        coincidencias.sort(key=lambda x: x[1], reverse=True)
        for i, (nombre, score, sombra) in enumerate(coincidencias, 1):
            print(f"{i}. 🧿 {nombre}  →  Similitud: {score}%")
            print(f"   🔹 Nivel: {sombra['level']}  |  ❤️ HP: {sombra['hp']}  |  💧 SP: {sombra['sp']}")
            if "weaknesses" in sombra:
                print(f"   ⚡ Debilidades: {', '.join(sombra['weaknesses'])}")
            print(f"   📍 Ubicación: {sombra['location']}  |  🎁 Ítem: {sombra['drop_items']}\n")
    else:
        print("❌ No se encontraron coincidencias con suficiente similitud.")

def main():
    # Cargar las sombras traducidas desde el archivo JSON
    with open("sombras_traducidas.json", "r", encoding="utf-8") as f:
        sombras = json.load(f)

    while True:
        entrada = input("🔎 Ingresa el nombre de la sombra (o escribe 'salir'): ").strip()
        if entrada.lower() == "salir":
            print("👋 Hasta luego.")
            break
        buscar_sombra(entrada, sombras)

if __name__ == "__main__":
    main()

