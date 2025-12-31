# 📔 Analizador de Diario Personal

Herramienta automatizada para analizar entradas de diario personal usando modelos de lenguaje locales (LM Studio). Extrae información estructurada como emociones, temas, personas mencionadas y genera resúmenes neutrales.

## ✨ Características

- 🤖 **Análisis con IA Local**: Utiliza LM Studio para procesamiento privado
- 📊 **Extracción Estructurada**: Genera JSON con emociones, temas y resúmenes
- 🛡️ **Manejo Robusto de Errores**: Validación completa y mensajes claros
- 📝 **Logging Detallado**: Seguimiento completo del proceso
- 💾 **Historial Acumulativo**: Mantiene registro de todos los análisis
- 🔒 **Privacidad Total**: Todo el procesamiento es local

## 📋 Requisitos Previos

### Software Necesario

- **Python 3.7 o superior**
- **LM Studio** instalado y en ejecución
  - Descarga desde: [lmstudio.ai](https://lmstudio.ai)
  - Debe estar corriendo el servidor local

### Dependencias Python

```bash
pip install lmstudio
```

## 🚀 Instalación

### 1. Clonar o descargar el proyecto

```bash
git clone https://github.com/tu-usuario/diary-analyzer.git
cd diary-analyzer
```

### 2. Crear entorno virtual (recomendado)

```bash
# Crear entorno virtual
python3 -m venv .venv

# Activar entorno virtual
# En Linux/Mac:
source .venv/bin/activate

# En Windows:
.venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install lmstudio
```

### 4. Configurar LM Studio

1. Abre LM Studio
2. Descarga el modelo: `liquidai/lfm2-2.6b-exp@f16` (o el que prefieras)
3. Inicia el servidor local (generalmente en `http://localhost:1234`)

## 📖 Uso

### Uso Básico

1. Coloca tu archivo de diario (formato Markdown) en el directorio del proyecto
2. Ejecuta el script:

```bash
python diary_analyzer.py
```

Por defecto, buscará el archivo `15-12-2025.md` y guardará el resultado en `diario.json`.

### Personalizar Archivos

Edita las constantes en `diary_analyzer.py`:

```python
if __name__ == "__main__":
    ARCHIVO_ENTRADA = "mi-diario-personal.md"  # Tu archivo
    ARCHIVO_SALIDA = "analisis.json"           # Archivo de salida
    MODELO_LLM = "liquidai/lfm2-2.6b-exp@f16"  # Modelo a usar
```

### Uso como Módulo

```python
from diary_analyzer import analizar_diario

# Análisis simple
resultado = analizar_diario(
    ruta_entrada="2025-01-15.md",
    ruta_salida="resultados.json",
    modelo="liquidai/lfm2-2.6b-exp@f16"
)

if resultado:
    print(f"Resumen: {resultado['summary']}")
    print(f"Emociones: {resultado['emotions']}")
    print(f"Temas: {resultado['topics']}")
```

### Uso con Funciones Individuales

```python
from diary_analyzer import (
    leer_archivo_diario,
    analizar_con_llm,
    extraer_json_de_respuesta,
    parsear_analisis,
    guardar_analisis
)

# Leer archivo
contenido = leer_archivo_diario("mi-diario.md")

# Analizar con LLM
respuesta = analizar_con_llm(contenido)

# Procesar respuesta
json_texto = extraer_json_de_respuesta(respuesta)
analisis = parsear_analisis(json_texto)

# Guardar
guardar_analisis(analisis, "output.json")
```

## 📄 Formato de Entrada

El archivo de diario debe ser un archivo Markdown (`.md`) con texto libre. Ejemplo:

```markdown
# 15 de Diciembre, 2025

Hoy fue un día interesante. Me reuní con María para discutir el proyecto.
Me sentí un poco ansioso al principio, pero luego todo fluyó naturalmente.

Aprendí mucho sobre React y estoy emocionado por implementarlo.
También hablé con Juan sobre sus planes de viaje.
```

## 📊 Formato de Salida

El análisis se guarda en formato JSON con la siguiente estructura:

```json
{
  "summary": "Reunión productiva sobre proyecto con María. Aprendizaje de React y conversación con Juan sobre viajes.",
  "emotions": ["ansioso", "emocionado"],
  "topics": ["trabajo", "programación", "viajes"],
  "people": ["María", "Juan"],
  "intensity": "media"
}
```

### Campos del Análisis

- **summary**: Resumen neutral en máximo 3 líneas
- **emotions**: Lista de emociones detectadas (puede ser lista vacía)
- **topics**: Temas principales discutidos
- **people**: Personas mencionadas (null si no hay ninguna)
- **intensity**: Intensidad emocional ("baja", "media" o "alta")

## 🔧 Configuración

### Cambiar el Modelo

Puedes usar cualquier modelo compatible con LM Studio:

```python
MODELO_LLM = "mistral-7b-instruct"
# o
MODELO_LLM = "llama-2-7b-chat"
```

### Ajustar el Logging

Modifica el nivel de logging al inicio del script:

```python
logging.basicConfig(
    level=logging.DEBUG,  # Cambiar a DEBUG, INFO, WARNING o ERROR
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

## 🐛 Solución de Problemas

### Error: "No se pudo conectar con LM Studio"

**Solución**: 
- Verifica que LM Studio esté abierto
- Confirma que el servidor local esté activo
- Revisa que el puerto sea el correcto (por defecto 1234)

### Error: "El archivo no existe"

**Solución**:
- Verifica la ruta del archivo
- Asegúrate de que el archivo tenga extensión `.md`
- Comprueba los permisos de lectura

### Error: "No se encontró un bloque JSON válido"

**Solución**:
- El modelo podría no estar siguiendo las instrucciones
- Intenta con un modelo diferente
- Verifica que el prompt sea claro
- Revisa la respuesta en los logs para debugging

### Error: "JSON inválido"

**Solución**:
- El modelo generó JSON malformado
- Revisa el contenido del diario (caracteres especiales)
- Considera usar un modelo más capaz

### Archivo de salida corrupto

**Solución**:
```bash
# Hacer backup del archivo corrupto
cp diario.json diario.json.backup

# Crear uno nuevo limpio
echo "[]" > diario.json
```

## 📁 Estructura del Proyecto

```
diary-analyzer/
├── diary_analyzer.py      # Script principal
├── README.md              # Esta documentación
├── .venv/                 # Entorno virtual (opcional)
├── diario.json           # Historial de análisis (generado)
└── 15-12-2025.md         # Tu archivo de diario
```

## 🔒 Privacidad y Seguridad

- ✅ Todo el procesamiento es **100% local**
- ✅ No se envían datos a servicios externos
- ✅ Tus diarios permanecen en tu computadora
- ✅ Sin conexión a internet requerida (excepto instalación inicial)

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📝 Ejemplos de Uso

### Analizar múltiples archivos

```python
import glob
from diary_analyzer import analizar_diario

archivos = glob.glob("diarios/*.md")

for archivo in archivos:
    print(f"Analizando {archivo}...")
    analizar_diario(archivo, "todos-los-analisis.json")
```

### Filtrar por emoción

```python
import json
from pathlib import Path

# Cargar historial
data = json.loads(Path("diario.json").read_text())

# Filtrar días con ansiedad
dias_ansiosos = [
    entrada for entrada in data 
    if "ansiedad" in entrada.get("emotions", [])
]

print(f"Días con ansiedad: {len(dias_ansiosos)}")
```

### Exportar estadísticas

```python
import json
from collections import Counter

data = json.loads(Path("diario.json").read_text())

# Emociones más comunes
todas_emociones = []
for entrada in data:
    todas_emociones.extend(entrada.get("emotions", []))

contador = Counter(todas_emociones)
print("Emociones más frecuentes:")
for emocion, count in contador.most_common(5):
    print(f"  {emocion}: {count}")
```

## 🗺️ Roadmap

- [ ] Interfaz gráfica (GUI)
- [ ] Exportación a PDF/HTML
- [ ] Gráficos de emociones a lo largo del tiempo
- [ ] Búsqueda por fecha/emoción/persona
- [ ] Soporte para múltiples idiomas
- [ ] Tests unitarios completos
- [ ] Integración con Obsidian/Notion

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

## 👤 Autor

**Fabri**

- GitHub: [@tu-usuario](https://github.com/tu-usuario)

## 🙏 Agradecimientos

- [LM Studio](https://lmstudio.ai) por proporcionar una excelente plataforma local
- [Liquid AI](https://liquid.ai) por el modelo LFM
- La comunidad de código abierto

## 📞 Soporte

Si tienes problemas o preguntas:

1. Revisa la sección de [Solución de Problemas](#-solución-de-problemas)
2. Busca en [Issues](https://github.com/tu-usuario/diary-analyzer/issues)
3. Abre un nuevo issue con detalles específicos

---

**¿Te resultó útil este proyecto? ¡Dale una ⭐ en GitHub!**