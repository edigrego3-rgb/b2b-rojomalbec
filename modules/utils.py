import urllib.parse
import math
import os
import re

def redondear_precio(valor):
    """Redondea hacia arriba a los 100 pesos más cercanos"""
    if valor <= 0:
        return 0
    return math.ceil(valor / 100.0) * 100

import unicodedata

def normalizar_texto(texto):
    """Quita tildes, guiones, convierte a minúsculas y elimina espacios extras."""
    if not texto:
        return ""
    t = unicodedata.normalize('NFD', str(texto))
    t = ''.join(c for c in t if unicodedata.category(c) != 'Mn')
    t = t.lower().replace("-", " ").replace(":", " ")
    return re.sub(r'\s+', ' ', t).strip()

def extraer_descripcion(nombre_blend, filepath="Descripciones_RojoMalbec.md"):
    """
    Busca el nombre del blend en el archivo markdown y extrae su descripción
    limpiando todos los caracteres de formato (Markdown).
    """
    if not os.path.exists(filepath):
        return "Descripción no disponible en este momento."
        
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            contenido = f.read()
            
        nombre_norm = normalizar_texto(nombre_blend)
        nombre_clean = nombre_norm.replace("blend ", "").replace("vital ", "").strip()
        
        secciones = re.split(r'^##\s+', contenido, flags=re.MULTILINE)
        
        for sec in secciones[1:]:
            lineas = sec.split('\n')
            if not lineas:
                continue
            titulo_norm = normalizar_texto(lineas[0])
            
            # Coincidencia flexible por título
            if (nombre_norm in titulo_norm or 
                nombre_clean in titulo_norm or 
                (len(nombre_clean) > 3 and titulo_norm in nombre_clean)):
                
                descripcion_limpia = []
                ingredientes_texto = ""
                
                for linea in lineas[1:]:
                    linea_str = linea.strip()
                    if not linea_str or linea_str.startswith('---') or linea_str.startswith('>') or linea_str.startswith('#') or linea_str.startswith('='):
                        continue
                    
                    linea_limpia = linea_str.replace('**', '')
                    
                    if linea_limpia.startswith('Ingredientes:'):
                        ingredientes_texto = linea_limpia
                    elif any(linea_limpia.startswith(kw) for kw in ['Técnica', 'Maridaje', 'Uso', 'Perfil', 'Sugerencias', 'Tip']):
                        descripcion_limpia.append(f"• {linea_limpia}")
                    else:
                        if not ingredientes_texto and not linea_limpia.startswith('•'):
                            descripcion_limpia.append(linea_limpia)
                
                texto_final = " ".join([l for l in descripcion_limpia if not l.startswith('•')])
                texto_final += "\n\n"
                if ingredientes_texto:
                    texto_final += f"🌿 {ingredientes_texto}\n"
                for extra in [l for l in descripcion_limpia if l.startswith('•')]:
                    texto_final += f"{extra}\n"
                    
                resultado = texto_final.strip()
                if resultado:
                    return resultado
    except Exception as e:
        print(f"Error extrayendo: {e}")
        pass
        
    return "Una creación premium de Rojo Malbec."

def generar_mensaje_whatsapp(carrito, total_pedido, telefono, datos_cliente):
    """
    Genera el link de WhatsApp con el pedido formateado.
    """
    nombre_local = datos_cliente.get("nombre", "Cliente B2B")
    cuit = datos_cliente.get("cuit", "")
    direccion = datos_cliente.get("direccion", "")
    
    texto = f"🌟 *NUEVO PEDIDO ROJO MALBEC* 🌟\n"
    texto += f"🏠 Local: {nombre_local}\n"
    if cuit: texto += f"📋 CUIT: {cuit}\n"
    if direccion: texto += f"📍 Envío: {direccion}\n"
    texto += "\n*DETALLE DEL PEDIDO:*\n"
    
    for item in carrito:
        texto += f"▪️ {item['cantidad']}x {item['nombre']} ($ {item['subtotal']:,})\n"
        
    texto += f"\n💰 *TOTAL A ABONAR:* $ {total_pedido:,}\n"
    texto += "\n_Aguardamos confirmación y datos de transferencia. ¡Gracias!_"
    
    texto_codificado = urllib.parse.quote(texto)
    # Asegurar formato internacional del teléfono (remover + si existe)
    tel_limpio = telefono.replace("+", "").replace(" ", "")
    
    return f"https://wa.me/{tel_limpio}?text={texto_codificado}"
