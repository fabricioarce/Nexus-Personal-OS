"""
Analizador de Diario Personal
------------------------------
Script para analizar entradas de diario usando LM Studio y extraer información estructurada.

Uso:
    python diary_analyzer.py

Requisitos:
    - lmstudio
    - Python 3.7+
"""

import re
import json
import logging
from pathlib import Path
from typing import Dict, Optional, Any
import lmstudio as lms


# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DiaryAnalyzerError(Exception):
    """Excepción base para errores del analizador de diario"""
    pass


class FileReadError(DiaryAnalyzerError):
    """Error al leer archivos"""
    pass


class JSONParseError(DiaryAnalyzerError):
    """Error al parsear JSON"""
    pass


class ModelError(DiaryAnalyzerError):
    """Error relacionado con el modelo LLM"""
    pass


def leer_archivo_diario(ruta_archivo: str) -> str:
    """
    Lee el contenido de un archivo de diario.
    
    Args:
        ruta_archivo: Ruta al archivo markdown del diario
        
    Returns:
        Contenido del archivo como string
        
    Raises:
        FileReadError: Si el archivo no existe o no se puede leer
    """
    try:
        archivo = Path(ruta_archivo)
        if not archivo.exists():
            raise FileReadError(f"El archivo '{ruta_archivo}' no existe")
        
        if not archivo.is_file():
            raise FileReadError(f"'{ruta_archivo}' no es un archivo válido")
        
        contenido = archivo.read_text(encoding='utf-8')
        
        if not contenido.strip():
            logger.warning(f"El archivo '{ruta_archivo}' está vacío")
        
        return contenido
        
    except UnicodeDecodeError as e:
        raise FileReadError(f"Error de codificación al leer '{ruta_archivo}': {e}")
    except PermissionError:
        raise FileReadError(f"Sin permisos para leer '{ruta_archivo}'")
    except Exception as e:
        raise FileReadError(f"Error inesperado al leer el archivo: {e}")


def analizar_con_llm(contenido: str, modelo: str = "liquidai/lfm2-2.6b-exp@f16") -> str:
    """
    Analiza el contenido del diario usando LM Studio.
    
    Args:
        contenido: Texto del diario a analizar
        modelo: Identificador del modelo a usar
        
    Returns:
        Respuesta del modelo como string
        
    Raises:
        ModelError: Si hay problemas con el modelo o la conexión
    """
    prompt = f"""
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
    <<<{contenido}>>>"""
    
    try:
        with lms.Client() as client:
            model = client.llm.model(modelo)
            result = model.respond(prompt)
            
            if not result or not hasattr(result, 'content'):
                raise ModelError("El modelo no devolvió una respuesta válida")
            
            return result.content
            
    except ConnectionError as e:
        raise ModelError(f"No se pudo conectar con LM Studio: {e}")
    except Exception as e:
        raise ModelError(f"Error al procesar con el modelo: {e}")


def extraer_json_de_respuesta(texto: str) -> str:
    """
    Extrae el bloque JSON de la respuesta del modelo.
    
    Args:
        texto: Respuesta completa del modelo
        
    Returns:
        String JSON limpio
        
    Raises:
        JSONParseError: Si no se encuentra JSON válido
    """
    # Buscar bloque de código JSON (con o sin especificador de lenguaje)
    match = re.search(r'(?s)```(?:json)?\s*(.*?)\s*```', texto)
    
    if match:
        return match.group(1).strip()
    
    # Si no hay bloque de código, intentar encontrar objeto JSON directamente
    match = re.search(r'(?s)\{.*\}', texto)
    if match:
        return match.group(0).strip()
    
    raise JSONParseError("No se encontró un bloque JSON válido en la respuesta del modelo")


def parsear_analisis(json_texto: str) -> Dict[str, Any]:
    """
    Parsea el JSON y valida su estructura.
    
    Args:
        json_texto: String JSON a parsear
        
    Returns:
        Diccionario con los datos parseados
        
    Raises:
        JSONParseError: Si el JSON es inválido o no tiene la estructura esperada
    """
    try:
        datos = json.loads(json_texto)
    except json.JSONDecodeError as e:
        raise JSONParseError(f"JSON inválido: {e}")
    
    # Validar estructura básica
    campos_requeridos = {'summary', 'emotions', 'topics', 'people', 'intensity'}
    campos_faltantes = campos_requeridos - set(datos.keys())
    
    if campos_faltantes:
        logger.warning(f"Campos faltantes en el análisis: {campos_faltantes}")
    
    # Validar intensity
    if 'intensity' in datos and datos['intensity'] not in ['baja', 'media', 'alta', None]:
        logger.warning(f"Valor de intensity inválido: {datos['intensity']}")
    
    return datos


def cargar_historial_diario(ruta_json: str = "diario.json") -> list:
    """
    Carga el historial existente del diario.
    
    Args:
        ruta_json: Ruta al archivo JSON del historial
        
    Returns:
        Lista con las entradas previas
        
    Raises:
        JSONParseError: Si el archivo existe pero no es JSON válido
    """
    archivo = Path(ruta_json)
    
    if not archivo.exists():
        logger.info(f"Creando nuevo archivo de historial: {ruta_json}")
        return []
    
    try:
        contenido = archivo.read_text(encoding='utf-8')
        if not contenido.strip():
            logger.warning(f"El archivo {ruta_json} está vacío, iniciando lista nueva")
            return []
        
        datos = json.loads(contenido)
        
        if not isinstance(datos, list):
            raise JSONParseError(f"El archivo {ruta_json} no contiene una lista")
        
        return datos
        
    except json.JSONDecodeError as e:
        raise JSONParseError(f"Error al parsear {ruta_json}: {e}")
    except Exception as e:
        raise FileReadError(f"Error al leer {ruta_json}: {e}")


def guardar_analisis(analisis: Dict[str, Any], ruta_json: str = "diario.json") -> None:
    """
    Guarda el análisis en el archivo JSON del historial.
    
    Args:
        analisis: Diccionario con el análisis a guardar
        ruta_json: Ruta al archivo JSON del historial
        
    Raises:
        FileReadError: Si no se puede escribir el archivo
    """
    try:
        historial = cargar_historial_diario(ruta_json)
        historial.append(analisis)
        
        archivo = Path(ruta_json)
        archivo.write_text(
            json.dumps(historial, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )
        
        logger.info(f"Análisis guardado exitosamente en {ruta_json}")
        
    except PermissionError:
        raise FileReadError(f"Sin permisos para escribir en {ruta_json}")
    except Exception as e:
        raise FileReadError(f"Error al guardar el análisis: {e}")


def analizar_diario(
    ruta_entrada: str = "15-12-2025.md",
    ruta_salida: str = "diario.json",
    modelo: str = "liquidai/lfm2-2.6b-exp@f16"
) -> Optional[Dict[str, Any]]:
    """
    Función principal que orquesta el análisis completo del diario.
    
    Args:
        ruta_entrada: Ruta al archivo markdown del diario
        ruta_salida: Ruta al archivo JSON de salida
        modelo: Modelo de LM Studio a usar
        
    Returns:
        Diccionario con el análisis si fue exitoso, None si hubo error
    """
    try:
        logger.info(f"Iniciando análisis de '{ruta_entrada}'")
        
        # 1. Leer archivo
        contenido = leer_archivo_diario(ruta_entrada)
        logger.info(f"Archivo leído correctamente ({len(contenido)} caracteres)")
        
        # 2. Analizar con LLM
        logger.info("Enviando a LM Studio para análisis...")
        respuesta = analizar_con_llm(contenido, modelo)
        
        # 3. Extraer JSON
        json_texto = extraer_json_de_respuesta(respuesta)
        
        # 4. Parsear y validar
        analisis = parsear_analisis(json_texto)
        logger.info("Análisis completado exitosamente")
        
        # 5. Guardar
        guardar_analisis(analisis, ruta_salida)
        
        logger.info("¡Proceso completado con éxito!")
        return analisis
        
    except DiaryAnalyzerError as e:
        logger.error(f"Error en el análisis: {e}")
        return None
    except Exception as e:
        logger.error(f"Error inesperado: {e}", exc_info=True)
        return None


if __name__ == "__main__":
    # Configuración
    ARCHIVO_ENTRADA = "15-12-2025.md"
    ARCHIVO_SALIDA = "diario.json"
    MODELO_LLM = "liquidai/lfm2-2.6b-exp@f16"
    
    # Ejecutar análisis
    resultado = analizar_diario(
        ruta_entrada=ARCHIVO_ENTRADA,
        ruta_salida=ARCHIVO_SALIDA,
        modelo=MODELO_LLM
    )
    
    if resultado:
        print("\n✓ Análisis guardado correctamente")
        print(f"\nResumen: {resultado.get('summary', 'N/A')}")
    else:
        print("\n✗ El análisis no pudo completarse. Revisa los logs.")