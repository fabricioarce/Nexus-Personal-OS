# 🏗️ Arquitectura del Sistema

Este documento describe la arquitectura técnica de **Diario Reflexivo**, un sistema diseñado para analizar, indexar y conversar con entradas de diario personal.

## 🧩 Componentes Principales

El sistema está dividido en tres capas principales:

1.  **Pipeline de Procesamiento de Datos** (Python Scritps)
2.  **Backend API** (FastAPI)
3.  **Frontend** (Astro + React/Tailwind)
*(Componente Legacy: Streamlit App)*

### 1. Pipeline de Procesamiento de Datos (`backend/app/core/`)

Este es el núcleo del análisis offline. Se encarga de transformar los archivos de texto plano (Markdown) en una base de conocimiento vectorial.

*   **Entrada**: Archivos Markdown en `diarios/*.md`.
*   **`diary_analyzer.py`**:
    *   Lee los archivos y extrae metadatos (fecha).
    *   Utiliza un LLM Local (vía LM Studio) para analizar sentimientos, emociones y generar resúmenes.
    *   Divide el texto en *chunks* semánticos optimizados para recuperación.
    *   Guarda resultados en `data/diario.json` y `data/diario_chunks.json`.
*   **`embedding_generator.py`**:
    *   Toma los chunks procesados.
    *   Genera vectores (embeddings) usando modelos `sentence-transformers` (ej. `intfloat/multilingual-e5-small`).
    *   Crea un índice FAISS (`data/diario_index.faiss`) para búsqueda rápida.

### 2. Backend API (`backend/app/`)

Servidor que expone la lógica de negocio y los datos procesados al frontend.

*   **Tecnología**: FastAPI.
*   **Core Logic**:
    *   **`rag_chat_engine_api.py`**: Gestiona la lógica RAG (Retrieval Augmented Generation). Recupera chunks relevantes desde FAISS y consulta a la API de Groq para generar respuestas.
*   **Endpoints**:
    *   `/api/chat`: Endpoint para enviar mensajes y recibir respuestas del asistente.
    *   `/api/diary`: (Planificado) Para listar entradas y estadísticas.
    *   `/api/stats`: Estadísticas del diario.

### 3. Frontend (`frontend/`)

Interfaz de usuario moderna y responsiva.

*   **Tecnología**: Astro.
*   **Funcionalidad**:
    *   Interfaz de Chat (`DiaryChat.astro`).
    *   Comunicación con el Backend vía fetch REST API.
    *   Visualización de respuestas en markdown.

---

## 🔄 Flujo de Datos

### Flujo de Indexación (Offline)

```mermaid
graph LR
    MD[Archivos .md] --> Analyzer[diary_analyzer.py]
    Analyzer --> |LLM Local| Analysis[JSON Data]
    Analysis --> Chunks[Chunks Semánticos]
    Chunks --> Embedder[embedding_generator.py]
    Embedder --> FAISS[Índice FAISS (.faiss)]
    Embedder --> Metadata[Metadata (.json)]
```

### Flujo de Conversación (Online)

```mermaid
graph LR
    User[Usuario] --> |Mensaje| Frontend[Astro UI]
    Frontend --> |POST /api/chat| Backend[FastAPI]
    Backend --> |Query Vector| FAISS[Índice FAISS]
    FAISS --> |Contexto Relevante| Backend
    Backend --> |Prompt + Contexto| Groq[Groq API (Llama 3)]
    Groq --> |Respuesta| Backend
    Backend --> |JSON| Frontend
    Frontend --> |UI Update| User
```

## 📂 Estructura de Directorios Clave

```
/
├── backend/
│   ├── app/
│   │   ├── api/            # Rutas de FastAPI
│   │   ├── core/           # Lógica de negocio (Analyzer, RAG, Embeddings)
│   │   └── main.py         # Punto de entrada FastAPI
│   └── ...
├── frontend/               # Código fuente Astro
│   ├── src/
│   │   ├── components/
│   │   └── pages/
│   └── ...
├── scripts/                # Scripts de utilidad (run.sh)
├── data/                   # Almacenamiento de índices y JSONs (Ignorado en git)
├── diarios/                # Carpeta de entrada para tus archivos .md
└── docs/                   # Documentación del proyecto
```
