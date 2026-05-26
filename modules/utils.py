import urllib.parse
import math
import os
import re

def redondear_precio(valor):
    """Redondea hacia arriba a los 100 pesos más cercanos"""
    if valor <= 0:
        return 0
    return math.ceil(valor / 100.0) * 100

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
            
        patron = re.compile(rf"##\s+.*?{re.escape(nombre_blend)}.*?$.*?(?=\n## |\Z)", re.MULTILINE | re.IGNORECASE | re.DOTALL)
        match = patron.search(contenido)
        
        if match:
            bloque = match.group(0)
            lineas = bloque.split('\n')
            
            descripcion_limpia = []
            ingredientes_texto = ""
            
            for linea in lineas[1:]: # saltar el título
                linea = linea.strip()
                if not linea or linea.startswith('---') or linea.startswith('>') or linea.startswith('#'):
                    continue
                
                # Limpiar negritas
                linea_limpia = linea.replace('**', '')
                
                if linea_limpia.startswith('Ingredientes:'):
                    ingredientes_texto = linea_limpia
                elif linea_limpia.startswith('Técnica') or linea_limpia.startswith('Maridaje') or linea_limpia.startswith('Uso'):
                    descripcion_limpia.append(f"• {linea_limpia}")
                else:
                    if not ingredientes_texto and not linea_limpia.startswith('•'):
                        descripcion_limpia.append(linea_limpia)
            
            # Unir todo de forma prolija
            texto_final = " ".join([l for l in descripcion_limpia if not l.startswith('•')])
            texto_final += "\n\n"
            if ingredientes_texto:
                texto_final += f"🌿 {ingredientes_texto}\n"
            for extra in [l for l in descripcion_limpia if l.startswith('•')]:
                texto_final += f"{extra}\n"
                
            return texto_final.strip() if texto_final.strip() else "Una creación premium de Rojo Malbec."
    except Exception:
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
