# P3REnemyPDFtoChatBot

Este proyecto convierte información de enemigos extraída desde un PDF del juego *Persona 3 Reload* en un chatbot interactivo. Combina procesamiento de lenguaje natural (NLP), modelos LLM y técnicas de recuperación semántica (RAG) para responder preguntas sobre enemigos del juego.

## Estructura del proyecto

```plaintext
p3renemypdftochatbot/
├── DataExtraction.py.py             # Extrae sombras desde el PDF
├── TranslatingSP.py                 # Traduce nombres de sombras a español
├── LLMOnly.py                       # Interacción con modelo LLM
├── NLPOnly.py                       # Chatbot con técnicas NLP (RapidFuzz)
├── LLMwRAG.py                       # Chatbot con RAG (embeddings + FAISS + LLM)
├── sombras_resultado.json           # Datos originales extraídos del PDF
├── sombras_traducidas.json          # Datos traducidos al español
├── traducciones.json                # Mapeo de nombres (inglés ↔ español)
├── requirements.txt                 # Lista de dependencias
└── README.md                        # Este archivo
```

## ¿Qué hace cada archivo?
*`DataExtraction.py`: Usa `pdfplumber` para leer datos del PDF original.

*`TranslatingSP.py`: Traduce los nombres de las sombras usando traducción automática.

*`NLPOnly.py`: Usa coincidencia aproximada para responder preguntas.

*`LLMOnly.py`: Responde preguntas usando un LLM.

*`LLMwRAG.py`: Usa embeddings con `FAISS` + LLM para respuestas más contextuales.

## Ejemplos de uso
*`¿Cuál es la debilidad de Jotun de sangre?`

*`¿Dónde está Orobas?`

*`Muéstrame las sombras de nivel 42`
## Instalación
```
pip install -r requirements.txt
```
## Tecnologías usadas
`pdfplumber`, `re`, `json`: para extracción y preprocesamiento

`RapidFuzz`: coincidencias textuales aproximadas

`sentence-transformers` + `faiss`: para recuperación semántica

`transformers`: para el modelo generativo LLM
