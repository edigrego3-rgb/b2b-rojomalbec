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
            
        # Limpiar el nombre de la BD para que coincida mejor con el Markdown
        nombre_buscar = nombre_blend.lower().replace("blend ", "").replace("vital ", "").strip()
        
        # Regex estricta: busca un encabezado ## que contenga el nombre en ESA misma línea,
        # y captura hasta el próximo ## o el final del archivo.
        patron = re.compile(rf"^##\s+[^\n]*?{re.escape(nombre_buscar)}[^\n]*\n(.*?)(?=^## |\Z)", re.MULTILINE | re.IGNORECASE | re.DOTALL)
        match = patron.search(contenido)
        
        # Si falla, intentamos con el nombre original completo
        if not match:
            patron_alt = re.compile(rf"^##\s+[^\n]*?{re.escape(nombre_blend)}[^\n]*\n(.*?)(?=^## |\Z)", re.MULTILINE | re.IGNORECASE | re.DOTALL)
            match = patron_alt.search(contenido)
            
        if match:
            bloque = match.group(1)
            lineas = bloque.split('\n')
            
            descripcion_limpia = []
            ingredientes_texto = ""
            
            for linea in lineas:
                linea = linea.strip()
                if not linea or linea.startswith('---') or linea.startswith('>') or linea.startswith('#') or linea.startswith('='):
                    continue
                
                # Limpiar negritas
                linea_limpia = linea.replace('**', '')
                
                if linea_limpia.startswith('Ingredientes:'):
                    ingredientes_texto = linea_limpia
                elif linea_limpia.startswith('Técnica') or linea_limpia.startswith('Maridaje') or linea_limpia.startswith('Uso') or linea_limpia.startswith('Perfil'):
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
                
            resultado = texto_final.strip()
            return resultado if resultado else "Una creación premium de Rojo Malbec."
    except Exception as e:
        print(f"Error extraendo: {e}")
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
