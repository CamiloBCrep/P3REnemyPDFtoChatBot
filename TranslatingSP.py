import json
import requests
import time

# Traduce una cadena de texto con Targomate
def traducir_texto(texto, target="es"):
    url = "https://api.mymemory.translated.net/get"
    params = {
        "q": texto,
        "langpair": "en|" + target
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()["responseData"]["translatedText"]
    else:
        return "Error: " + response.text

# Traduce todos los campos de texto del JSON
def traducir_json_completo(sombras):
    sombras_traducidas = []
    for sombra in sombras:
        sombra_traducida = {}
        for clave, valor in sombra.items():
            if isinstance(valor, str):
                sombra_traducida[clave] = traducir_texto(valor)
                time.sleep(0.5)  # para evitar bloqueo por demasiadas peticiones
            elif isinstance(valor, list):
                sombra_traducida[clave] = [traducir_texto(item) if isinstance(item, str) else item for item in valor]
                time.sleep(0.5)
            else:
                sombra_traducida[clave] = valor
        sombras_traducidas.append(sombra_traducida)
    return sombras_traducidas

# Carga y guarda los JSON
def main():
    with open("sombras_resultado.json", "r", encoding="utf-8") as f:
        sombras = json.load(f)

    print("🌐 Traduciendo sombras...")
    sombras_traducidas = traducir_json_completo(sombras)

    with open("sombras_traducidas_completo.json", "w", encoding="utf-8") as f:
        json.dump(sombras_traducidas, f, ensure_ascii=False, indent=4)

    print("✅ Traducción completa. Archivo guardado como 'sombras_traducidas_completo.json'.")

if __name__ == "__main__":
    main()


