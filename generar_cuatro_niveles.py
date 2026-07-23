import os
import re
import shutil
import pandas as pd
from barcode import Code128
from barcode.writer import ImageWriter
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import mm
from reportlab.pdfgen import canvas

PRODUCTOS_DATA = [
    ("Sal al Malbec", "🧂 Sales", "RM-SAL-MALBEC"),
    ("Sal British", "🧂 Sales", "RM-SAL-BRITISH"),
    ("Sal de Hierbas Ahumadas", "🧂 Sales", "RM-SAL-AHUMADA"),
    ("Sal de Limon y Chile (Suave)", "🧂 Sales", "RM-SAL-LIMCHIL"),
    ("Sal de Rosas y Romero", "🧂 Sales", "RM-SAL-ROSAS"),
    ("Sal del Desierto", "🧂 Sales", "RM-SAL-DESIERTO"),
    ("Sal Negra Tipo Hawaiana", "🧂 Sales", "RM-SAL-HAWAI"),
    ("Sal Esvanetian", "🧂 Sales", "RM-SAL-ESVANET"),
    ("Sal Vikinga Ahumada", "🧂 Sales", "RM-SAL-VIKINGA"),
    ("DRY HOT HONEY", "🌿 Blends", "RM-BLE-DRYHONEY"),
    ("Advieh Persa", "🌿 Blends", "RM-BLE-ADVIEH"),
    ("AJO A LAS HIERBAS GOURMET", "🌿 Blends", "RM-BLE-AJOHIERB"),
    ("BAHARAT", "🌿 Blends", "RM-BLE-BAHARAT"),
    ("BBQ", "🌿 Blends", "RM-BLE-BBQ"),
    ("Criolla Deshidratada", "🌿 Blends", "RM-BLE-CRIOLLA"),
    ("Curry Colombo", "🌿 Blends", "RM-BLE-CURRY"),
    ("Crocante de Panko, Sesamo Y Limon", "🌿 Blends", "RM-BLE-PANKO"),
    ("KHMELI SUNELI", "🌿 Blends", "RM-BLE-KHMELI"),
    ("Muddica Atturrata", "🌿 Blends", "RM-BLE-MUDDICA"),
    ("Nanami Tōgarashi", "🌿 Blends", "RM-BLE-NANAMI"),
    ("Panch Phoron", "🌿 Blends", "RM-BLE-PANCH"),
    ("Pesto Siciliano con Pistacho", "🌿 Blends", "RM-BLE-PESTO"),
    ("Vadouvan", "🌿 Blends", "RM-BLE-VADOUVAN"),
    ("Tandoori Masala", "🌿 Blends", "RM-BLE-TANDOORI"),
    ("ZA'ATAR", "🌿 Blends", "RM-BLE-ZAATAR"),
    ("Blend Burger", "🌿 Blends", "RM-BLE-BURGER"),
    ("Sloopy Joe", "🌿 Blends", "RM-BLE-SLOPPYJOE"),
    ("Dip Ranch", "🌿 Blends", "RM-BLE-RANCH"),
    ("Blend Bosque y Brasas (Montreal Steak)", "🌿 Blends", "RM-BLE-BOSQUE"),
    ("Blend Kebab & Dip", "🌿 Blends", "RM-BLE-KEBAB"),
    ("Jerk Jamaica", "🌿 Blends", "RM-BLE-JERK"),
    ("España Profunda", "🌿 Blends", "RM-BLE-ESPANA"),
    ("Mole Mexicano", "🌿 Blends", "RM-BLE-MOLE"),
    ("Quatre Epice", "🌿 Blends", "RM-BLE-QUATRE"),
    ("Glühwein", "🌿 Blends", "RM-BLE-GLUHWEIN"),
    ("Te Pu-Erh Rojo Malbec", "🍵 Tés", "RM-TEA-PUERH"),
    ("TE VERDE DEL ZOCO", "🍵 Tés", "RM-TEA-ZOCO"),
    ("Te Karak", "🍵 Tés", "RM-TEA-KARAK"),
    ("Rooibos : Ambar Africano", "🍵 Tés", "RM-TEA-ROOIBOS"),
    ("Vital Caldo", "💚 Vital", "RM-VIT-CALDO"),
    ("Vital Italia", "💚 Vital", "RM-VIT-ITALIA"),
    ("Vital India", "💚 Vital", "RM-VIT-INDIA"),
    ("Vital Parrilera", "💚 Vital", "RM-VIT-PARRILLA"),
    ("Vital Criollo", "💚 Vital", "RM-VIT-CRIOLLO"),
    ("Vital Citrus", "💚 Vital", "RM-VIT-CITRUS"),
    ("VITAL TIPO QUESO · Perfil Parmesano Reserva", "💚 Vital", "RM-VIT-QUESO"),
    ("Pimienta Negra de Autor", "🌶️ Pimientas", "RM-PIM-NEGRA"),
    ("Pimienta Roja y Pimienta Larga", "🌶️ Pimientas", "RM-PIM-ROJA"),
    ("Pimienta Verde de Autor", "🌶️ Pimientas", "RM-PIM-VERDE"),
    ("Mocktail : Floral Hibiscus", "🍹 Mocktails", "RM-MOC-HIBISCUS"),
    ("Mocktail: Dorado Especiado", "🍹 Mocktails", "RM-MOC-DORADO"),
    ("Mocktail: Aperitivo Botanico", "🍹 Mocktails", "RM-MOC-BOTANICO"),
]

DESKTOP_MAIN = r"C:\Users\Eduardo\Desktop\Codigos_Barra_RojoMalbec"
DESKTOP_PNG_DIR = os.path.join(DESKTOP_MAIN, "Imagenes_PNG_Para_Labelife")
DESKTOP_INDIV_DIR = os.path.join(DESKTOP_MAIN, "Etiquetas_Individuales")

# Limpiar subcarpetas previas para que no haya duplicados
for folder in [DESKTOP_PNG_DIR, DESKTOP_INDIV_DIR]:
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(folder, exist_ok=True)

# 1. GENERAR IMÁGENES PNG (4 NIVELES)
WIDTH_PX = 600
HEIGHT_PX = 300

try:
    font_brand = ImageFont.truetype("arial.ttf", 16)
    font_product = ImageFont.truetype("arialbd.ttf", 24)
    font_code = ImageFont.truetype("arial.ttf", 18)
except Exception:
    font_brand = ImageFont.load_default()
    font_product = ImageFont.load_default()
    font_code = ImageFont.load_default()

print("Generando PNGs de 4 Niveles...")
for nombre, cat, code in PRODUCTOS_DATA:
    fn_clean = re.sub(r'[^a-zA-Z0-9_]', '_', nombre).replace("__", "_").strip("_")
    
    # Barcode puro sin texto
    bc_temp = os.path.join(DESKTOP_PNG_DIR, f"temp_{code}")
    c128 = Code128(code, writer=ImageWriter())
    c128.save(bc_temp, options={
        'module_width': 0.35,
        'module_height': 12.0,
        'quiet_zone': 2.0,
        'background': 'white',
        'foreground': 'black',
        'write_text': False
    })
    
    bc_file = bc_temp + ".png"
    img_bc = Image.open(bc_file)
    
    canvas_img = Image.new("RGB", (WIDTH_PX, HEIGHT_PX), "white")
    draw = ImageDraw.Draw(canvas_img)
    
    # Nivel 1: Marca Header (Rojo Malbec · Sales & Blends / Tierra Lotus by Rojo Malbec para Tés)
    header_text = "Tierra Lotus by Rojo Malbec" if cat == "🍵 Tés" else "Rojo Malbec · Sales & Blends"
    bbox1 = draw.textbbox((0, 0), header_text, font=font_brand)
    w1 = bbox1[2] - bbox1[0]
    draw.text(((WIDTH_PX - w1) // 2, 8), header_text, fill="#555555", font=font_brand)
    
    # Nivel 2: Nombre del Producto
    bbox2 = draw.textbbox((0, 0), nombre[:26], font=font_product)
    w2 = bbox2[2] - bbox2[0]
    draw.text(((WIDTH_PX - w2) // 2, 32), nombre[:26], fill="black", font=font_product)
    
    # Nivel 3: Código de Barras Img
    bc_w, bc_h = img_bc.size
    target_w = 540
    target_h = 160
    img_bc_resized = img_bc.resize((target_w, target_h), Image.Resampling.LANCZOS)
    canvas_img.paste(img_bc_resized, ((WIDTH_PX - target_w) // 2, 80))
    
    # Nivel 4: Texto del Código al pie (RM-SAL-MALBEC)
    bbox4 = draw.textbbox((0, 0), code, font=font_code)
    w4 = bbox4[2] - bbox4[0]
    draw.text(((WIDTH_PX - w4) // 2, 252), code, fill="black", font=font_code)
    
    out_png_path = os.path.join(DESKTOP_PNG_DIR, f"{fn_clean}.png")
    canvas_img.save(out_png_path, "PNG")
    
    if os.path.exists(bc_file):
        os.remove(bc_file)

# 2. GENERAR PDFs INDIVIDUALES (4 NIVELES)
print("Generando PDFs Individuales de 4 Niveles...")
for nombre, cat, code in PRODUCTOS_DATA:
    fn_clean = re.sub(r'[^a-zA-Z0-9_]', '_', nombre).replace("__", "_").strip("_")
    png_path = os.path.join(DESKTOP_PNG_DIR, f"{fn_clean}.png")
    
    pdf_path = os.path.join(DESKTOP_INDIV_DIR, f"{fn_clean}.pdf")
    c = canvas.Canvas(pdf_path, pagesize=(50*mm, 25*mm))
    c.drawImage(png_path, 0, 0, width=50*mm, height=25*mm)
    c.showPage()
    c.save()

# 3. GENERAR PDF MASTER 2 COLUMNAS (100x25mm)
print("Generando PDF Master 2 Columnas de 4 Niveles...")
pdf_2col = os.path.join(DESKTOP_MAIN, "Etiquetas_100x25_DobleColumna_Labelife.pdf")
c_2col = canvas.Canvas(pdf_2col, pagesize=(100*mm, 25*mm))

for i in range(0, len(PRODUCTOS_DATA), 2):
    prod1 = PRODUCTOS_DATA[i]
    prod2 = PRODUCTOS_DATA[i+1] if i+1 < len(PRODUCTOS_DATA) else None
    
    fn1 = re.sub(r'[^a-zA-Z0-9_]', '_', prod1[0]).replace("__", "_").strip("_") + ".png"
    p1_path = os.path.join(DESKTOP_PNG_DIR, fn1)
    c_2col.drawImage(p1_path, 0*mm, 0*mm, width=50*mm, height=25*mm)
    
    if prod2:
        fn2 = re.sub(r'[^a-zA-Z0-9_]', '_', prod2[0]).replace("__", "_").strip("_") + ".png"
        p2_path = os.path.join(DESKTOP_PNG_DIR, fn2)
        c_2col.drawImage(p2_path, 50*mm, 0*mm, width=50*mm, height=25*mm)
        
    c_2col.showPage()

c_2col.save()

# Copiar PDF master a artifacts
ART_DIR = r"C:\Users\Eduardo\.gemini\antigravity\brain\9d4e23e1-0e6d-4d7c-9846-12f5ea046993"
if os.path.exists(pdf_2col):
    shutil.copy(pdf_2col, os.path.join(ART_DIR, "Etiquetas_100x25_DobleColumna_Labelife.pdf"))

print("¡4 NIVELES GENERADOS PERFECTAMENTE!")
