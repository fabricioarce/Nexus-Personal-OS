# 🚀 Guía de Uso y Flujo de Trabajo

Aprende a ejecutar el sistema completo, desde añadir nuevas entradas hasta chatear con tu diario.

## 📝 1. Añadir Nuevas Entradas

1.  Crea archivos Markdown (`.md`) con tus entradas de diario.
2.  Guárdalos en la carpeta `diarios/` en la raíz del proyecto.
3.  **Formato Recomendado**: Usa el nombre del archivo como `DD-MM-YYYY.md` para facilitar la detección de fechas.

Ejemplo `diarios/15-01-2024.md`:
```markdown
# Reflexión del Lunes

Hoy aprendí mucho sobre estoicismo...
```

## 🧠 2. Procesar y Analizar (Pipeline Offline)

Cada vez que añadas entradas nuevas, debes ejecutar el pipeline para indexarlas.

Asegúrate de tener activa tu **venv** de Python y **LM Studio corriendo** (puerto 1234).

### Ejecución Automática (Recomendado)

Usa el script `run.sh` desde la raíz:

```bash
./run.sh
```
*Este script intentará ejecutar todo el proceso. Si solo quieres procesar datos, puedes interrumpirlo antes de lanzar la UI.*

### Ejecución Manual Paso a Paso

Si prefieres control total, ejecuta los módulos de Python:

1.  **Analizar Diarios** (Genera JSONs):
    ```bash
    python -m backend.app.core.diary_analyzer
    ```
2.  **Generar Embeddings e Índice** (Crea `.faiss`):
    ```bash
    python -m backend.app.core.query_engine --build-index
    ```

## 💻 3. Ejecutar la Aplicación (Modo Desarrollo)

Para usar el Chatbot con la interfaz moderna, necesitas correr dos servidores simultáneamente (en dos terminales distintas).

### Terminal 1: Backend (API)

```bash
# Desde la raíz del proyecto
source .venv/bin/activate
uvicorn backend.app.main:app --reload
```
*El servidor API estará disponible en `http://localhost:8000`.*

### Terminal 2: Frontend (UI)

```bash
# Desde la carpeta frontend/
cd frontend
pnpm dev
```
*La aplicación web estará disponible en `http://localhost:4321`.*

---

## 🐢 Modo Legacy (Streamlit)

Si necesitas probar algo rápido sin levantar el frontend de Astro:

```bash
streamlit run backend/app/app.py
```
