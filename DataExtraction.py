import pdfplumber
import json
import re

# Función para extraer texto del PDF
def extraer_texto_pdf(ruta_pdf):
    with pdfplumber.open(ruta_pdf) as pdf:
        texto = ""
        for pagina in pdf.pages:
            texto += pagina.extract_text() + "\n"
    return texto

# Función para procesar y extraer las sombras del texto
def extraer_sombras(texto_pdf):
    sombras = []
    
    # Dividir el texto por saltos de línea y palabras clave
    entradas = texto_pdf.split("\n")
    
    # Variables para almacenar la sombra actual
    sombra = {}
    
    for linea in entradas:
        # Extraer nombre y nivel (Ejemplo: Flowing Sand Lv.21)
        match_nombre = re.match(r"([A-Za-z\s]+)\sLv\.(\d+)", linea)
        if match_nombre:
            if sombra:  # Si hay una sombra ya iniciada, la agregamos antes de empezar una nueva
                sombras.append(sombra)
            sombra = {"name": match_nombre.group(1).strip(), "level": int(match_nombre.group(2))}
        
       # Extraer HP y SP (Ejemplo: ? HP, ? SP)
        match_hp_sp = re.search(r"([\d,]+|\?)\s*HP,\s*([\d,]+|\?)\s*SP", linea)
        if match_hp_sp:
            hp = match_hp_sp.group(1).strip().replace(",", "")
            sp = match_hp_sp.group(2).strip().replace(",", "")
            
            # Mantener "?" como valor cuando es desconocido
            if not es_valor_valido(hp):
                hp = "?"  # Si no es un valor válido, lo dejamos como "?"
            if not es_valor_valido(sp):
                sp = "?"  # Lo mismo para SP
            
            sombra["hp"] = hp
            sombra["sp"] = sp

        # Extraer debilidades (Ejemplo: Dark, Strike, Slash)
        # Buscamos múltiples palabras clave como debilidades separadas por comas
        match_debilidad = re.search(r"(Slash|Strike|Pierce|Fire|Ice|Wind|Elec|Light|Dark|Almi|None)(?:\s*,\s*(Slash|Strike|Pierce|Fire|Ice|Wind|Elec|Light|Dark|Almi|None))*", linea, re.IGNORECASE)
        if match_debilidad:
            # Añadimos todas las debilidades encontradas a una lista
            debilidades = [match_debilidad.group(i).strip() for i in range(1, match_debilidad.lastindex + 1)]
            sombra["weaknesses"] = debilidades

        
         # Extraer Location (si existe)
        match_location = re.search(r"Location\s*([^\n]+)", linea)
        if match_location:
            sombra["location"] = match_location.group(1).strip()  # Almacena el valor real de Location

        # Extraer Drop Items (si existe)
        match_drop_items = re.search(r"Drop Items\s*([^\n]+)", linea)
        if match_drop_items:
            sombra["drop_items"] = match_drop_items.group(1).strip()  # Almacena el valor real de Drop Items

    if sombra:  # Para agregar la última sombra
        sombras.append(sombra)
    
    return sombras

# Función para validar si un valor es un número o un "?"
def es_valor_valido(valor):
    # Si es un número válido o un "?", retornamos True
    return valor.isdigit() or valor == "?"

# Guardar resultados en JSON
def guardar_json(sombras, ruta_salida):
    with open(ruta_salida, 'w', encoding='utf-8') as f:
        json.dump(sombras, f, ensure_ascii=False, indent=4)

# Main
ruta_pdf = "Gatekeeper Min1.pdf"
texto_pdf = extraer_texto_pdf(ruta_pdf)
sombras = extraer_sombras(texto_pdf)

if sombras:
    guardar_json(sombras, "sombras_resultado.json")
    print(f"Se extrajeron {len(sombras)} sombras y se guardaron en 'sombras_resultado.json'.")
else:
    print("No se encontraron sombras para procesar.")

