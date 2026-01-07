# 🧠 Diario Reflexivo con IA

> Sistema completo de análisis semántico de diario personal con RAG (Retrieval Augmented Generation), búsqueda vectorial y chatbot conversacional.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Astro](https://img.shields.io/badge/astro-5.0-orange.svg)](https://astro.build)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Tabla de Contenidos

- [Descripción General](#-descripción-general)
- [Características](#-características)
- [Documentación](#-documentación)
- [Inicio Rápido](#-inicio-rápido)
- [Tecnologías](#-tecnologías)

---

## 🎯 Descripción General

**Diario Reflexivo con IA** es un sistema integral que transforma tus entradas de diario personal en una base de conocimiento semántica consultable. Utiliza modelos de lenguaje locales (LM Studio) para el análisis inicial offline, embeddings multilingües para búsqueda semántica, y **Groq API** para conversaciones contextualizadas en tiempo real.

### ¿Qué hace este sistema?

1.  **Analiza** tus entradas de diario (emociones, temas).
2.  **Indexa** semánticamente tus memorias en una base de datos vectorial local.
3.  **Conversa** contigo a través de una interfaz moderna, respondiendo preguntas sobre tu pasado, patrones emocionales y reflexiones.

---

## ✨ Características

*   **100% Privacidad en Procesamiento**: El análisis de tus textos se hace localmente con LM Studio.
*   **Chatbot RAG Rápido**: Respuestas instantáneas usando Groq (Llama 3 / Mixtral) con contexto de tus diarios.
*   **Interfaz Moderna**: Frontend construido con Astro y React para una experiencia fluida.
*   **API Robusta**: Backend en FastAPI modular y extensible.
*   **Búsqueda Semántica**: Encuentra recuerdos por significado, no solo palabras clave.

---

## 📚 Documentación

Hemos organizado la documentación en guías detalladas:

*   **[🛠️ Guía de Instalación (SETUP.md)](docs/SETUP.md)**: Requisitos y pasos para configurar Backend y Frontend.
*   **[🚀 Guía de Uso (USAGE.md)](docs/USAGE.md)**: Cómo añadir diarios, ejecutar el pipeline y usar la App.
*   **[🏗️ Arquitectura (ARCHITECTURE.md)](docs/ARCHITECTURE.md)**: Diagramas y explicación técnica de los componentes.
*   **[📡 Referencia API (API_REFERENCE.md)](docs/API_REFERENCE.md)**: Documentación de los endpoints del Backend.

---

## ⚡ Inicio Rápido

Si ya tienes los requisitos (Python, Node.js, LM Studio):

1.  **Instalar dependencias**:
    ```bash
    # Backend
    python -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt
    
    # Frontend
    cd frontend && pnpm install
    ```

2.  **Configurar `.env`**:
    Añade tu `GROQ_API_KEY` en `backend/app/.env`.

3.  **Ejecutar Servidores**:
    
    *Backend* (Terminal 1):
    ```bash
    uvicorn backend.app.main:app --reload
    ```
    
    *Frontend* (Terminal 2):
    ```bash
    cd frontend && pnpm dev
    ```

Visita `http://localhost:4321` para usar la aplicación.

---

## 🛠️ Tecnologías

### Backend
*   **FastAPI**: Server API.
*   **LangChain / RAG**: Lógica de chat.
*   **FAISS**: Base de datos vectorial.
*   **Sentence Transformers**: Embeddings locales.

### Frontend
*   **Astro**: Framework web.
*   **React**: Componentes de UI.
*   **TailwindCSS**: Estilos.