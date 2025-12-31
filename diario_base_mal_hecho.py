# Create and run venv
# fabri@fedora:~/Documents/Diario$ python3 -m venv .venv
# fabri@fedora:~/Documents/Diario$ source .venv/bin/activate
# Desactivar: deactivate

import re
import lmstudio as lms
from pathlib import Path
import json


try: 
    with open('15-12-2025.md', 'r', encoding='utf-8') as file:
        contenido_md = file.read()
except FileNotFoundError:
    print("El archivo no fue encontrado.")

with lms.Client() as client:
    model = client.llm.model("liquidai/lfm2-2.6b-exp@f16")
    result = model.respond(f"""
    INSTRUCCIONES:
    Tu tarea es analizar texto de diario personal y extraer información estructurada.
    No hagas juicios, no des consejos, no interpretes más allá del texto.
    No inventes información que no esté explícita o claramente inferida.

    Si algo no está presente, devuélvelo como null.

    SALIDA:
    Devuelve exclusivamente un objeto JSON válido con las siguientes claves:

        summary: resumen neutral en máximo 3 líneas
        emotions: lista de emociones explícitas o claramente inferidas
        topics: lista de temas principales
        people: lista de personas mencionadas (o null)
        intensity: "baja", "media" o "alta"

    TEXTO DEL DIARIO:
    <<<{contenido_md}>>>""")
    # print(result)

#print(type(result))

texto = result.content

match = re.search(
    r'(?s)```(?:json)?\s*(.*?)\s*```',
    texto
)

if not match:
    raise ValueError("El modelo no devolvió un bloque JSON")

json_limpio = match.group(1)

ruta = Path("diario.json")

data = json.loads(ruta.read_text(encoding="utf-8"))
obj = json.loads(json_limpio)
data.append(obj)

ruta.write_text(
    json.dumps(data, indent=2, ensure_ascii=False),
    encoding="utf-8"
)


print("listo")