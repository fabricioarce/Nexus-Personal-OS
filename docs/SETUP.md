# 🛠️ Guía de Instalación y Configuración

Configura tu entorno de desarrollo para ejecutar **Diario Reflexivo**.

## 📋 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

1.  **Python 3.10+**: Para el backend y scripts de análisis.
2.  **Node.js 18+** y **pnpm** (o npm): Para el frontend.
3.  **LM Studio** (Opcional pero recomendado para análisis local): Para procesar los diarios con privacidad total.
4.  **Cuenta de Groq** (Requerido para el Chat): Obtén una API Key en [console.groq.com](https://console.groq.com).

## 🔧 Configuración del Backend

### 1. Entorno Virtual

Navega a la raíz del proyecto y crea un entorno virtual:

```bash
# Crear entorno
python -m venv .venv

# Activar entorno
# En Linux/Mac:
source .venv/bin/activate
# En Windows:
.venv\Scripts\activate
```

### 2. Instalar Dependencias

Instala las librerías necesarias:

```bash
pip install -r requirements.txt
```

> **Nota**: Si no existe `requirements.txt`, las dependencias principales son: `fastapi`, `uvicorn`, `streamlit`, `sentence-transformers`, `faiss-cpu`, `requests`, `python-dotenv`.

### 3. Variables de Entorno

Crea un archivo `.env` en la carpeta `backend/app/` (o en la raíz del backend según configuración):

```env
GROQ_API_KEY=gsk_tu_api_key_aqui...
```

*   `GROQ_API_KEY`: *Requerido*. Tu llave para generar respuestas de chat.

---

## 🎨 Configuración del Frontend

El frontend está construido con **Astro**.

### 1. Instalar Dependencias

Navega a la carpeta `frontend`:

```bash
cd frontend
pnpm install
# O si usas npm:
npm install
```

### 2. Configuración de Entorno (Frontend)

Crea un archivo `.env` en `frontend/` si necesitas configurar la URL de la API:

```env
PUBLIC_API_URL=http://localhost:8000
```

---

## ⚙️ Configuración de LM Studio (Para Análisis)

Si vas a procesar nuevas entradas de diario:

1.  Abre **LM Studio**.
2.  Carga un modelo ligero pero capaz (ej. `Llama 3 8B` o `Mistral 7B`).
3.  Ve a la pestaña de **Local Server**.
4.  Inicia el servidor en el puerto `1234` (default).
5.  Asegúrate de que `CORS` esté habilitado si es necesario (generalmente no afecta llamadas locales de python).

¡Listo! Ya tienes todo configurado. Pasa a la guía de [Uso](USAGE.md) para ejecutar el proyecto.
