# P3REnemyPDFtoChatBot

Este proyecto convierte información de enemigos extraída desde un PDF del juego *Persona 3 Reload* en un chatbot interactivo. Combina procesamiento de lenguaje natural (NLP), modelos LLM y técnicas de recuperación semántica (RAG) para responder preguntas sobre enemigos del juego.

##Estructura del proyecto

```plaintext
p3renemypdftochatbot/
├── extractor.py             # Extrae sombras desde el PDF
├── traductor.py             # Traduce nombres de sombras a español
├── chatbot_llm.py           # Interacción con modelo LLM
├── chatbot_nlp.py           # Chatbot con técnicas NLP (RapidFuzz)
├── chatbot_rag.py           # Chatbot con RAG (embeddings + FAISS + LLM)
├── sombras.json             # Datos originales extraídos del PDF
├── sombras_traducidas.json  # Datos traducidos al español
├── nombres_traduccion.json  # Mapeo de nombres (inglés ↔ español)
├── requirements.txt         # Lista de dependencias
└── README.md                # Este archivo
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
