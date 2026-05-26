import streamlit as st
import pandas as pd
import os
import sys

# --- RUTAS ---
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from modules.data_manager import load_catalog_data
from modules.utils import redondear_precio, extraer_descripcion, generar_mensaje_whatsapp

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Rojo Malbec B2B | Distribuidores",
    page_icon="🍷",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ESTILO PREMIUM ---
st.markdown("""
<style>
/* === BASE === */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

[data-testid="stAppViewContainer"] {
    background: linear-gradient(165deg, #0a0a0f 0%, #111118 50%, #0d0d14 100%);
    font-family: 'Inter', sans-serif;
}

/* === HEADER COMPACTO === */
.header-bar {
    background: linear-gradient(135deg, #8b0000 0%, #a02020 50%, #8b0000 100%);
    color: white;
    padding: 12px 20px;
    border-radius: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    box-shadow: 0 4px 20px rgba(139,0,0,0.3);
}
.header-bar h1 {
    margin: 0; font-size: 1.4em; color: white !important;
}
.header-bar span {
    font-size: 0.8em; opacity: 0.85;
}

/* === BUSCADOR === */
[data-testid="stTextInput"] > div > div > input {
    background-color: #1a1a24 !important;
    border: 2px solid #2a2a3a !important;
    border-radius: 12px !important;
    color: #e0e0e0 !important;
    padding: 12px 16px !important;
    font-size: 1em !important;
}
[data-testid="stTextInput"] > div > div > input:focus {
    border-color: #d4af37 !important;
    box-shadow: 0 0 0 2px rgba(212,175,55,0.2) !important;
}

/* === TABS ELEGANTES === */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: #12121a;
    padding: 4px;
    border-radius: 12px;
    margin-bottom: 20px;
}
.stTabs [data-baseweb="tab"] {
    color: #888 !important;
    border-radius: 8px;
    padding: 8px 16px !important;
    font-weight: 600;
    font-size: 0.85em;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #8b0000, #a02020) !important;
    color: white !important;
}

/* === TARJETA DE PRODUCTO === */
.card {
    background: linear-gradient(145deg, #16161f 0%, #1a1a26 100%);
    border-radius: 16px;
    padding: 18px;
    margin-bottom: 16px;
    border: 1px solid #22222e;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}
.card:hover {
    border-color: #d4af3780;
    box-shadow: 0 8px 30px rgba(212,175,55,0.08);
    transform: translateY(-2px);
}

/* Línea dorada superior */
.card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #d4af37, #f0d060, #d4af37);
}

/* === NOMBRE PRODUCTO === */
.prod-name {
    font-size: 1.15em;
    font-weight: 700;
    color: #f0f0f0;
    margin: 8px 0 12px 0;
    line-height: 1.3;
}

/* === PRECIOS === */
.price-row {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    gap: 10px;
    margin: 10px 0;
}
.price-main {
    font-size: 1.6em;
    font-weight: 800;
    color: #d4af37;
    line-height: 1;
}
.price-label {
    font-size: 0.7em;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 2px;
}
.price-pvp {
    text-align: right;
}
.price-pvp-value {
    font-size: 1em;
    font-weight: 600;
    color: #aaa;
}

/* === BADGE GANANCIA === */
.gain-badge {
    display: inline-block;
    background: linear-gradient(135deg, rgba(76,175,80,0.15), rgba(76,175,80,0.05));
    color: #66bb6a;
    padding: 6px 14px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 0.85em;
    border: 1px solid rgba(76,175,80,0.2);
    margin: 8px 0;
}

/* === BADGE CARRITO (en tarjeta) === */
.cart-badge {
    position: absolute;
    top: 12px; right: 12px;
    background: linear-gradient(135deg, #d4af37, #f0d060);
    color: #111;
    width: 28px; height: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 0.85em;
    z-index: 2;
    box-shadow: 0 2px 8px rgba(212,175,55,0.4);
}

/* === BOTÓN AGREGAR === */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #2e7d32, #388e3c) !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px !important;
}
.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #388e3c, #43a047) !important;
    box-shadow: 0 4px 15px rgba(56,142,60,0.3) !important;
}

/* === SIDEBAR CARRITO === */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111118, #0d0d14) !important;
}
[data-testid="stSidebar"] h1 {
    color: #d4af37 !important;
    font-size: 1.3em !important;
}

/* === EXPANDER === */
.streamlit-expanderHeader {
    font-size: 0.85em !important;
    color: #aaa !important;
}

/* === HEADINGS === */
h1, h2, h3 { color: #d4af37; }

/* === RESPONSIVE: MOBILE === */
@media (max-width: 768px) {
    .price-main { font-size: 1.3em; }
    .prod-name { font-size: 1.05em; }
    .card { padding: 14px; }
}

/* === SCROLLBAR === */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a0a0f; }
::-webkit-scrollbar-thumb { background: #333; border-radius: 3px; }

/* === INFO STRIP === */
.info-strip {
    background: #12121a;
    border: 1px solid #1e1e2a;
    border-radius: 10px;
    padding: 10px 16px;
    margin-bottom: 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.82em;
    color: #aaa;
}
.info-strip b { color: #d4af37; }

/* Ocultar label vacío de tabs */
.stTabs [data-baseweb="tab-list"] button[role="tab"] p { margin: 0; }
</style>
""", unsafe_allow_html=True)

# --- FUNCIONES AUXILIARES ---
def detectar_categoria(nombre_producto):
    nombre = str(nombre_producto).lower()
    if "sal " in nombre or nombre.startswith("sal"):
        return "🧂 Sales"
    elif "vital" in nombre:
        return "💚 Vital"
    elif "blend" in nombre or "bbq" in nombre or "curry" in nombre or "baharat" in nombre or "masala" in nombre or "joe" in nombre or "ranch" in nombre or "pesto" in nombre or "jerk" in nombre or "panko" in nombre or "criolla" in nombre or "muddica" in nombre or "nanami" in nombre or "panch phoron" in nombre or "vadouvan" in nombre or "españa" in nombre or "mexicano" in nombre or "glühwein" in nombre:
        return "🌿 Blends"
    elif "té " in nombre or nombre.startswith("te ") or " rooibos" in nombre or nombre.startswith("rooibos") or " karak" in nombre or nombre.startswith("karak"):
        return "🍵 Tés"
    elif "mocktail" in nombre:
        return "🍹 Mocktails"
    elif "pimienta" in nombre:
        return "🌶️ Pimientas"
    else:
        return "🌿 Blends"

def buscar_imagenes(nombre_producto):
    """
    Busca la imagen Frontal en la carpeta images.
    Devuelve la ruta (o None si no existe).
    """
    images_dir = os.path.join(current_dir, "images")
    if not os.path.exists(images_dir):
        return None, None
        
    term = nombre_producto.lower()
    
    # --- DICCIONARIO INTELIGENTE PARA CASOS ESPECIALES ---
    if "sloopy joe" in term or "sloppy" in term: term = "sloppyjoe"
    elif "sal al malbec" in term: term = "malbec"
    elif "sal negra" in term or "hawaiana" in term: term = "hawaiana"
    elif "ajo a las hierbas" in term: term = "ajohierbas"
    elif "bbq" in term or "barbacoa" in term: term = "barbacoa"
    elif "bosque y brasas" in term: term = "bosque"
    elif "kebab" in term: term = "kebab"
    elif "panko" in term or "sesamo y limon" in term: term = "sesamo"
    elif "españa profunda" in term or "espana" in term: term = "espana"
    elif "glühwein" in term or "gluhwein" in term: term = "gluhwein"
    elif "mocktail" in term: term = "botanico"
    elif "panch" in term: term = "panch"
    elif "criolla deshidratada" in term: term = "criolla"
    elif "rooibos" in term: term = "rooibos"
    elif "sal british" in term: term = "british"
    elif "esvanetian" in term: term = "svanetian"
    elif "rosas y romero" in term: term = "rosas"
    elif "del desierto" in term: term = "desierto"
    elif "vikinga" in term: term = "vikinga"
    elif "limon y chile" in term: term = "limonchile"
    elif "queso" in term: term = "queso"
    elif "parrilera" in term: term = "parrilera"
    elif "pimienta negra" in term: term = "pimientanegra"
    elif "pimienta roja" in term: term = "pimientaroja"
    elif "pimienta verde" in term: term = "pimientaverde"
    elif "jerk" in term: term = "jerk"
    elif "nanami" in term: term = "nanami"
    elif "pesto" in term: term = "pesto"
    elif "za'atar" in term or "zaatar" in term: term = "zaatar"
    else:
        # Limpiar espacios si no cayó en ningún caso especial
        term = term.replace(" ", "")
        
    term = term.replace("&", "").replace("(", "").replace(")", "").replace("ñ", "n").replace("ü", "u").replace("'", "").replace("ō", "o")
    
    # Filtrar archivos
    archivos_validos = []
    for f in os.listdir(images_dir):
        f_limpio = f.lower().replace("ñ", "n")
        
        # Ignorar COMPLETAMENTE cualquier cosa que diga "trasera" o "back"
        if "trasera" in f_limpio or "back" in f_limpio:
            continue
            
        f_sin_espacios = f_limpio.replace("_", "").replace(" ", "")
        
        # Si el término buscado está en el nombre del archivo
        if term in f_sin_espacios or term in f_limpio.replace("_", " "):
            archivos_validos.append(f)
            
    if not archivos_validos:
        return None, None
        
    # Preferir archivos que digan "clean" o "frontal"
    for f in archivos_validos:
        if "clean" in f.lower() or "frontal" in f.lower() or "color" in f.lower() or "premium" in f.lower():
            return os.path.join(images_dir, f), None
            
    # Si no, devolver el primero que encuentre
    return os.path.join(images_dir, archivos_validos[0]), None

# --- ESTADO DEL CARRITO ---
if "carrito" not in st.session_state:
    st.session_state.carrito = {}

# --- HEADER COMPACTO ---
total_items = sum(item['cantidad'] for item in st.session_state.carrito.values())
st.markdown(f"""
<div class='header-bar'>
    <div>
        <h1>🍷 Rojo Malbec</h1>
        <span>Portal Mayorista · Catálogo B2B</span>
    </div>
    <div style='text-align:right;'>
        <span style='font-size:1.5em;'>🛒 {total_items}</span><br>
        <span>productos</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- INFO STRIP ---
st.markdown("""
<div class='info-strip'>
    <span>🌿 Producción a pedido · Frescura garantizada</span>
    <b>Envío: 7 días hábiles</b>
</div>
""", unsafe_allow_html=True)

# --- CARGAR CATÁLOGO ---
with st.spinner("Actualizando catálogo..."):
    df_catalogo = load_catalog_data()

if df_catalogo.empty:
    st.error("No se pudo cargar el catálogo. Contacte a administración.")
    st.stop()

df_catalogo["Categoria"] = df_catalogo["Nombre"].apply(detectar_categoria)

# --- SIDEBAR: CARRITO Y CHECKOUT ---
st.sidebar.markdown("## 🛒 Tu Pedido")

if not st.session_state.carrito:
    st.sidebar.info("Agregá productos desde el catálogo.")
else:
    total_pedido = 0
    items_carrito = []
    
    for nombre, item_data in st.session_state.carrito.items():
        if item_data['cantidad'] > 0:
            subtotal = item_data['cantidad'] * item_data['precio']
            total_pedido += subtotal
            
            st.sidebar.markdown(f"**{nombre}**")
            cols_cart = st.sidebar.columns([2, 1, 1])
            with cols_cart[0]:
                st.write(f"{item_data['cantidad']} un. x ${item_data['precio']:,}")
            with cols_cart[1]:
                if st.button("➖", key=f"del_{nombre}"):
                    st.session_state.carrito[nombre]['cantidad'] -= 1
                    if st.session_state.carrito[nombre]['cantidad'] <= 0:
                        del st.session_state.carrito[nombre]
                    st.rerun()
            with cols_cart[2]:
                if st.button("➕", key=f"add_{nombre}_cart"):
                    st.session_state.carrito[nombre]['cantidad'] += 1
                    st.rerun()
            st.sidebar.markdown("---")
            
            items_carrito.append({
                'nombre': nombre,
                'cantidad': item_data['cantidad'],
                'precio': item_data['precio'],
                'subtotal': subtotal
            })

    if items_carrito:
        st.sidebar.markdown(f"### 💰 Total: $ {total_pedido:,}")
        
        st.sidebar.markdown("#### 📝 Datos de Envío")
        nombre_cliente = st.sidebar.text_input("Nombre del Local / Distribuidor")
        cuit = st.sidebar.text_input("CUIT (Opcional)")
        direccion = st.sidebar.text_input("Dirección de Envío")
        
        if st.sidebar.button("✅ ENVIAR PEDIDO POR WHATSAPP", type="primary", use_container_width=True):
            if not nombre_cliente:
                st.sidebar.error("Ingresá tu nombre.")
            else:
                link_wa = generar_mensaje_whatsapp(
                    carrito=items_carrito,
                    total_pedido=total_pedido,
                    telefono="5493544308380",
                    datos_cliente={"nombre": nombre_cliente, "cuit": cuit, "direccion": direccion}
                )
                st.sidebar.success("¡Pedido listo!")
                st.sidebar.markdown(f"[📲 Abrir WhatsApp]({link_wa})", unsafe_allow_html=True)
                if st.sidebar.button("🗑️ Vaciar Carrito"):
                    st.session_state.carrito = {}
                    st.rerun()

# --- BUSCADOR + BOTÓN CARRITO ---
col_search, col_cart_btn = st.columns([5, 1])
with col_search:
    search = st.text_input("🔍 Buscar producto...", placeholder="Ej: Sal, Curry, Vital...", label_visibility="collapsed")
with col_cart_btn:
    if st.button(f"🛒 ({total_items})", use_container_width=True, type="primary"):
        st.session_state["sidebar_state"] = "expanded"
        st.rerun()

# --- CATÁLOGO POR PESTAÑAS ---
categorias = ["🏠 Todos", "🧂 Sales", "🌿 Blends", "💚 Vital", "🍵 Tés", "🍹 Mocktails", "🌶️ Pimientas"]
tabs = st.tabs(categorias)

for i, tab in enumerate(tabs):
    with tab:
        cat_actual = categorias[i]
        
        df_tab = df_catalogo.copy()
        if cat_actual != "🏠 Todos":
            df_tab = df_tab[df_tab["Categoria"] == cat_actual]
            
        if search:
            df_tab = df_tab[df_tab["Nombre"].str.contains(search, case=False)]
            
        if df_tab.empty:
            st.info("No hay productos en esta categoría.")
            continue
        
        # --- GRILLA DE 2 COLUMNAS (mejor para mobile) ---
        cols = st.columns(2)
        for idx, row in df_tab.reset_index(drop=True).iterrows():
            nombre = row["Nombre"]
            precio_mayorista = float(row["Precio_Mayorista"])
            costo_redondeado = redondear_precio(precio_mayorista)
            
            # PVP: Leer directo de la BD (guardado por el simulador del ERP)
            pvp_guardado = float(row.get("PVP_Sugerido", 0))
            if pvp_guardado > 0:
                pvp_final = pvp_guardado
            else:
                # Si no lo guardaron en la ERP, lo calculamos EN VIVO usando el Markup de la base de datos
                markup_revendedor = float(row.get("Markup_Revendedor", 0))
                if markup_revendedor > 0:
                    pvp_final = precio_mayorista * (1 + markup_revendedor / 100)
                else:
                    # Fallback final si tampoco hay markup
                    pvp_final = precio_mayorista * 1.5
                    
            pvp_redondeado = redondear_precio(pvp_final)
            ganancia_neta = pvp_redondeado - costo_redondeado
            
            desc_path = os.path.join(current_dir, "Descripciones_RojoMalbec.md")
            descripcion = extraer_descripcion(nombre, desc_path)
            
            img_front, img_back = buscar_imagenes(nombre)
            
            qty_actual = st.session_state.carrito.get(nombre, {}).get("cantidad", 0)
            
            col_idx = idx % 2
            with cols[col_idx]:
                # Badge de cantidad en carrito
                badge_html = f"<div class='cart-badge'>{qty_actual}</div>" if qty_actual > 0 else ""
                
                html_card = f"""<div class='card'>
{badge_html}
<div class='prod-name'>{nombre}</div>
<div class='price-row'>
<div>
<div class='price-label'>Tu costo</div>
<div class='price-main'>$ {costo_redondeado:,}</div>
</div>
<div class='price-pvp'>
<div class='price-label'>PVP sugerido</div>
<div class='price-pvp-value'>$ {pvp_redondeado:,}</div>
</div>
</div>
<div class='gain-badge'>📈 Ganancia: $ {ganancia_neta:,}</div>
</div>"""
                st.markdown(html_card, unsafe_allow_html=True)
                
                # Imágenes (Solo Frontal para no ensuciar la vista)
                if img_front:
                    st.image(img_front, use_container_width=True)
                
                # Descripción colapsable
                with st.expander("🌿 Ingredientes y maridaje"):
                    st.markdown(f"<div style='font-size:0.88em; color:#ccc; white-space:pre-wrap;'>{descripcion}</div>", unsafe_allow_html=True)
                
                # --- CONTROLES DE CARRITO MEJORADOS ---
                if qty_actual == 0:
                    # Solo botón de agregar
                    if st.button(f"🛒 AGREGAR", key=f"add_{cat_actual}_{idx}", use_container_width=True, type="primary"):
                        st.session_state.carrito[nombre] = {"cantidad": 1, "precio": costo_redondeado}
                        st.rerun()
                else:
                    # Controles ➖ cantidad ➕
                    c1, c2, c3 = st.columns([1, 2, 1])
                    with c1:
                        if st.button("➖", key=f"minus_{cat_actual}_{idx}", use_container_width=True):
                            st.session_state.carrito[nombre]['cantidad'] -= 1
                            if st.session_state.carrito[nombre]['cantidad'] == 0:
                                del st.session_state.carrito[nombre]
                            st.rerun()
                    with c2:
                        st.markdown(f"<div style='text-align:center; padding:6px; font-weight:800; font-size:1.2em; color:#d4af37; background:#1a1a24; border-radius:8px;'>{qty_actual} en pedido</div>", unsafe_allow_html=True)
                    with c3:
                        if st.button("➕", key=f"plus_{cat_actual}_{idx}", use_container_width=True, type="primary"):
                            st.session_state.carrito[nombre]['cantidad'] += 1
                            st.rerun()
                
                # Separador visual entre tarjetas
                st.markdown("<div style='margin-bottom:10px;'></div>", unsafe_allow_html=True)
