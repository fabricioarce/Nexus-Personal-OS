# Estrategia App Móvil (Capacitor + Cloud API)

Esta estrategia te permite tener una **App Móvil Real** (instalada en tu teléfono) que funciona conectada a tu API en la nube, cumpliendo tus requisitos:
1.  **Gratis**: Hosting gratuito para DB/API. Sin costos de hosting frontend.
2.  **PC Apagada**: La app funciona independientemente de tu PC de desarrollo.
3.  **Sin Hosting Frontend**: La interfaz (UI) vive dentro del teléfono.

## Arquitectura "Híbrida Local"

```mermaid
graph TD
    Phone[Tu Teléfono] -->|1. Abre App| App[App Instalada (Capacitor)]
    App -->|2. Carga UI (Rápido)| UI[HTML/JS/CSS Local]
    UI -->|3. Pide Datos| CloudAPI[Cloud API (Render/Railway)]
    CloudAPI -->|4. Consulta| CloudDB[(Base de Datos PostgreSQL)]
    
    subgraph "En tu Teléfono (Offline UI)"
    App
    UI
    end
    
    subgraph "En la Nube (Siempre Activo)"
    CloudAPI
    CloudDB
    end
```

### ¿Por qué Capacitor?
Capacitor toma tu build de Astro (`dist/`) y lo empaqueta dentro de una "cáscara" nativa de Android/iOS.
*   **No necesitas hosting web**: Tu frontend no se sirve desde una URL, se sirve desde el almacenamiento interno del teléfono.
*   **Velocidad**: La carga es instantánea porque los archivos ya están ahí.

## Pasos de Implementación

### 1. Preparar Astro para ser "Estático"
Asegúrate de que tu `astro.config.mjs` esté configurado para generar un sitio estático (o SPA), ya que Capacitor no puede ejecutar un servidor Node.js (SSR) en el teléfono.

```javascript
// astro.config.mjs
import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  output: 'static', // Importante: Estático
  integrations: [tailwind()],
});
```

### 2. Instalar Capacitor (En carpeta `frontend`)
```bash
cd frontend
npm install @capacitor/core @capacitor/cli @capacitor/android
npx cap init NexusApp io.nexus.app
```

### 3. Configurar API Remota
Antes de construir la app, debes apuntar el frontend a tu API en la nube (la que creaste con la guía de Deployment).
Edita `frontend/.env.production`:
```bash
PUBLIC_API_URL=https://tu-api-en-railway.app
```

### 4. Construir y Sincronizar
```bash
# 1. Construir el frontend (genera carpeta dist/)
npm run build

# 2. Copiar los archivos a la plataforma nativa
npx cap add android
npx cap sync
```

### 5. Instalar en el Teléfono
1.  Ejecuta `npx cap open android`.
2.  Esto abrirá **Android Studio**.
3.  Conecta tu teléfono por USB (asegúrate de tener "Depuración USB" activa).
4.  Dale al botón de "Play" (Run) en Android Studio.
5.  **¡Listo!** La app se instalará en tu teléfono.

## Acerca de los Datos Locales
Mencionaste: *"que la parte de datos se pudiera guardar en el telefono"*.

En este modelo (API en Nube), los datos principales "viven" en la nube (PostgreSQL). Esto es lo mejor porque:
1.  Si pierdes el teléfono, no pierdes tus datos.
2.  Puedes acceder desde la PC o el teléfono y ver lo mismo.

**Si quieres funcionalidad Offline (sin internet):**
Podemos implementar una caché local en el frontend (usando `localStorage` o `IndexedDB` en el navegador/app).
1.  La app guarda los diarios nuevos **localmente** si no hay internet.
2.  Cuando detecta internet, los envía a la API.
Esto se llama "Sync" y es un poco más avanzado, pero es totalmente posible con esta arquitectura.
