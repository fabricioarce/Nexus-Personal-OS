# 📡 Referencia de API

Documentación de los endpoints disponibles en el Backend de FastAPI.

**Base URL**: `http://localhost:8000`

## 💬 Chat

### `POST /api/chat/message` (Ruta estimada)

Envía un mensaje al asistente RAG.

**Body (JSON)**:
```json
{
  "message": "¿Qué escribí sobre mi viaje a Japón?",
  "history": [] // Opcional: Historial de chat previo
}
```

**Respuesta (JSON)**:
```json
{
  "response": "En tu viaje a Japón mencionaste que...",
  "sources": [ ... ] // Chunks de contexto utilizados
}
```

## 📔 Diario

### `GET /api/diary`

Recupera una lista de las entradas de diario procesadas.

### `GET /api/diary/{id}`

Recupera los detalles de una entrada específica.

## 📊 Estadísticas

### `GET /api/stats`

Devuelve metadatos generales del diario.

**Respuesta Ejemplo**:
```json
{
  "total_entries": 45,
  "total_words": 15000,
  "top_emotions": ["alegría", "ansiedad"]
}
```

---

> **Nota para desarrolladores**: Puedes ver la documentación interactiva completa generada por FastAPI (Swagger UI) navegando a `http://localhost:8000/docs` cuando el servidor backend esté corriendo.
