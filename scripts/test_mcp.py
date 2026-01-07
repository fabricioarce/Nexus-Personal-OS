import sys
import os

# Añadir el directorio raíz al path para poder importar backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.core.rag_chat_engine_api import DiarioRAGChat

def test_mcp():
    print("🚀 Iniciando prueba de Memoria a Corto Plazo (MCP)...")
    chat = DiarioRAGChat()
    
    # Primera interacción
    print("\n💬 Pregunta 1: 'Hola, mi nombre es Fabricio.'")
    resp1 = chat.preguntar("Hola, mi nombre es Fabricio.")
    print(f"🤖 IA: {resp1[:50]}...")
    
    # Segunda interacción (Verificar si recuerda el nombre)
    print("\n💬 Pregunta 2: '¿Cómo me llamo?'")
    resp2 = chat.preguntar("¿Cómo me llamo?")
    print(f"🤖 IA: {resp2}")
    
    if "Fabricio" in resp2:
        print("\n✅ ÉXITO: La IA recordó el nombre. MCP funcionando correctamente.")
    else:
        print("\n❌ ERROR: La IA no recordó el nombre.")

if __name__ == "__main__":
    test_mcp()
