# App B2B Rojo Malbec - Build trigger 2026-07-22
import streamlit as st
import pandas as pd
import os
import sys

# --- RUTAS ---
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from modules.data_manager import load_catalog_data, guardar_visibilidad
from modules.utils import redondear_precio, extraer_descripcion, generar_mensaje_whatsapp

# --- CONFIGURACIÓN DE PÁGINA ---
if "sidebar_state" not in st.session_state:
    st.session_state.sidebar_state = "collapsed"

st.set_page_config(
    page_title="Rojo Malbec B2B | Distribuidores",
    page_icon="🍷",
    layout="wide",
    initial_sidebar_state=st.session_state.sidebar_state
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

/* Ocultar TODO rastro de Streamlit Cloud y GitHub */
#MainMenu {visibility: hidden !important;}
footer {visibility: hidden !important; display: none !important;}
[data-testid="stToolbar"] {display: none !important;}
[data-testid="manage-app-button"] {display: none !important;}
[data-testid="viewerBadge"] {display: none !important;}
.stDeployButton {display: none !important;}
[class^="viewerBadge"] { display: none !important; }
[class*="viewerBadge"] { display: none !important; }
[class*="manage-app"] { display: none !important; }
a[href*="streamlit"] {display: none !important;}
a[href*="github"] {display: none !important;}
iframe[src*="streamlit"] {display: none !important;}

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

/* === ADMIN PANEL === */
.admin-header {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    border: 1px solid #d4af3740;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 16px;
}
.admin-header h3 {
    color: #d4af37 !important;
    margin: 0 0 4px 0;
    font-size: 1.1em;
}
.admin-header p {
    color: #888;
    margin: 0;
    font-size: 0.85em;
}
</style>
""", unsafe_allow_html=True)

# --- FUNCIONES AUXILIARES ---
import unicodedata

def detectar_categoria(nombre_producto):
    nombre_raw = str(nombre_producto)
    nombre = unicodedata.normalize('NFD', nombre_raw).encode('ascii', 'ignore').decode('utf-8').lower()
    palabras = nombre.replace("-", " ").replace(":", " ").split()
    
    # 1. TÉS (Prioridad #1)
    es_te = ("te" in palabras or "pu" in palabras or "erh" in palabras or 
             "puerh" in palabras or "rooibos" in palabras or 
             "karak" in palabras or "zoco" in palabras or nombre.startswith("te "))
    
    if es_te and "panko" not in palabras:
        return "🍵 Tés"

    # 2. SALES
    if "sal" in palabras or nombre.startswith("sal "):
        return "🧂 Sales"

    # 3. VITAL
    if "vital" in palabras:
        return "💚 Vital"

    # 4. MOCKTAILS
    if "mocktail" in palabras or "mocktail" in nombre:
        return "🍹 Mocktails"

    # 5. PIMIENTAS
    if "pimienta" in palabras or "pimienta" in nombre:
        return "🌶️ Pimientas"

    # 6. BLENDS (Default)
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
    elif "sal al malbec" in term or term == "sal malbec": term = "salmarinaalmalbec"
    elif "pu" in term and "erh" in term: term = "puerh"
    elif "zoco" in term: term = "zoco"
    elif "dry" in term or "honey" in term: term = "dryhothoney"
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
        
    term = term.replace("&", "").replace("(", "").replace(")", "").replace("-", "").replace("ñ", "n").replace("ü", "u").replace("'", "").replace("ō", "o")
    
    # Filtrar archivos
    archivos_validos = []
    for f in os.listdir(images_dir):
        f_limpio = f.lower().replace("ñ", "n")
        
        # Ignorar COMPLETAMENTE cualquier cosa que diga "trasera" o "back"
        if "trasera" in f_limpio or "back" in f_limpio:
            continue
            
        f_sin_espacios = f_limpio.replace("_", "").replace(" ", "").replace("-", "")
        
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

col_logo, col_titulo, col_cart = st.columns([1, 4, 2])
with col_logo:
    # Intentar cargar el logo si existe en la carpeta
    ruta_logo = os.path.join(current_dir, "logo.png")
    if os.path.exists(ruta_logo):
        st.image(ruta_logo, use_container_width=True)
    else:
        st.markdown("<h1 style='text-align:center;'>🍷</h1>", unsafe_allow_html=True)

with col_titulo:
    st.markdown("""
        <div style='padding-top: 10px;'>
            <h1 style='margin:0; font-size:2rem; color:#d4af37;'>Rojo Malbec</h1>
            <span style='color:#a0a0b0; font-size:1.1rem;'>Portal Mayorista · B2B</span>
        </div>
    """, unsafe_allow_html=True)

with col_cart:
    st.markdown(f"""
        <div style='text-align:right; padding-top: 15px;'>
            <span style='font-size:1.8em; font-weight:800; color:#d4af37;'>🛒 {total_items}</span><br>
            <span style='color:#a0a0b0;'>productos</span>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='margin-top:0; border-color:#333;'>", unsafe_allow_html=True)

# --- CARRITO INTEGRADO ---
if total_items > 0:
    with st.expander(f"🛒 VER MI PEDIDO ({total_items} productos)", expanded=False):
        st.markdown("### 📝 Resumen de tu pedido")
        total_pedido = 0
        items_carrito = []
        
        for nombre, item_data in st.session_state.carrito.items():
            if item_data['cantidad'] > 0:
                subtotal = item_data['cantidad'] * item_data['precio']
                total_pedido += subtotal
                
                st.markdown(f"**{nombre}**")
                cols_cart = st.columns([2, 1, 1])
                with cols_cart[0]:
                    st.write(f"{item_data['cantidad']} un. x ${item_data['precio']:,}")
                with cols_cart[1]:
                    opciones_cart = list(range(0, 101))
                    if item_data['cantidad'] not in opciones_cart:
                        opciones_cart.append(item_data['cantidad'])
                        opciones_cart.sort()
                        
                    new_qty = st.selectbox("Unidades", options=opciones_cart, index=opciones_cart.index(item_data['cantidad']), key=f"cart_{nombre}", label_visibility="collapsed")
                    if new_qty != item_data['cantidad']:
                        if new_qty == 0:
                            del st.session_state.carrito[nombre]
                        else:
                            st.session_state.carrito[nombre]['cantidad'] = new_qty
                        st.rerun()
                st.markdown("---")
                
                items_carrito.append({
                    'nombre': nombre,
                    'cantidad': item_data['cantidad'],
                    'precio': item_data['precio'],
                    'subtotal': subtotal
                })
        
        st.markdown(f"### 💰 Total a pagar: $ {total_pedido:,}")
        
        st.markdown("#### Datos de Envío")
        nombre_cliente = st.text_input("Nombre del Local / Distribuidor", key="cliente_nombre")
        cuit = st.text_input("CUIT (Opcional)", key="cliente_cuit")
        direccion = st.text_input("Dirección de Envío", key="cliente_dir")
        
        c_enviar, c_vaciar = st.columns([3, 1])
        with c_enviar:
            if st.button("✅ ENVIAR PEDIDO POR WHATSAPP", type="primary", use_container_width=True):
                if not nombre_cliente:
                    st.error("Ingresá tu nombre antes de enviar.")
                else:
                    link_wa = generar_mensaje_whatsapp(
                        carrito=items_carrito,
                        total_pedido=total_pedido,
                        telefono="5493544308380",
                        datos_cliente={"nombre": nombre_cliente, "cuit": cuit, "direccion": direccion}
                    )
                    st.success("¡Pedido listo para enviar!")
                    st.markdown(f"<a href='{link_wa}' target='_blank' style='display:block; text-align:center; background-color:#25D366; color:white; padding:12px; border-radius:8px; font-weight:bold; text-decoration:none;'>📲 ABRIR WHATSAPP</a>", unsafe_allow_html=True)
        with c_vaciar:
            if st.button("🗑️ Vaciar", use_container_width=True):
                st.session_state.carrito = {}
                st.rerun()

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

# --- PANEL ADMIN (protegido con clave) ---
if "admin_mode" not in st.session_state:
    st.session_state.admin_mode = False

col_admin_spacer, col_admin_btn = st.columns([6, 1])
with col_admin_btn:
    if st.button("⚙️", use_container_width=True, help="Panel de administración"):
        st.session_state.show_admin_login = not st.session_state.get("show_admin_login", False)
        if st.session_state.admin_mode:
            st.session_state.admin_mode = False
            st.session_state.show_admin_login = False
        st.rerun()

if st.session_state.get("show_admin_login", False) and not st.session_state.admin_mode:
    with st.container():
        st.markdown("<div class='admin-header'><h3>🔐 Acceso Administrador</h3><p>Ingresá tu clave para gestionar el catálogo</p></div>", unsafe_allow_html=True)
        clave = st.text_input("Clave", type="password", key="admin_pass")
        if st.button("Ingresar", type="primary"):
            if clave == "Livia2112":
                st.session_state.admin_mode = True
                st.session_state.show_admin_login = False
                st.rerun()
            else:
                st.error("❌ Clave incorrecta")

if st.session_state.admin_mode:
    st.markdown("<div class='admin-header'><h3>⚙️ Panel de Administración</h3><p>Seleccioná los productos que querés mostrar en el catálogo</p></div>", unsafe_allow_html=True)
    
    todos_los_nombres = df_catalogo["Nombre"].tolist()
    nombres_visibles_actuales = df_catalogo[df_catalogo["Visible_B2B"] == True]["Nombre"].tolist()
    
    # Botones rápidos
    col_sel_all, col_desel_all, col_guardar_vis = st.columns(3)
    with col_sel_all:
        if st.button("✅ Seleccionar Todos", use_container_width=True):
            st.session_state.productos_seleccionados = todos_los_nombres
            st.rerun()
    with col_desel_all:
        if st.button("❌ Deseleccionar Todos", use_container_width=True):
            st.session_state.productos_seleccionados = []
            st.rerun()
    
    # Inicializar selección
    if "productos_seleccionados" not in st.session_state:
        st.session_state.productos_seleccionados = nombres_visibles_actuales
    
    # Agrupar por categoría para que sea más fácil de gestionar
    st.markdown("---")
    categorias_admin = df_catalogo.groupby("Categoria")
    for cat_name, cat_df in categorias_admin:
        with st.expander(f"{cat_name} ({len(cat_df)} productos)", expanded=False):
            for _, row_admin in cat_df.iterrows():
                nombre_prod = row_admin["Nombre"]
                checked = nombre_prod in st.session_state.productos_seleccionados
                if st.checkbox(nombre_prod, value=checked, key=f"vis_{nombre_prod}"):
                    if nombre_prod not in st.session_state.productos_seleccionados:
                        st.session_state.productos_seleccionados.append(nombre_prod)
                else:
                    if nombre_prod in st.session_state.productos_seleccionados:
                        st.session_state.productos_seleccionados.remove(nombre_prod)
    
    st.markdown("---")
    n_seleccionados = len(st.session_state.productos_seleccionados)
    st.info(f"📊 Mostrando **{n_seleccionados}** de **{len(todos_los_nombres)}** productos")
    
    with col_guardar_vis:
        if st.button("💾 GUARDAR", type="primary", use_container_width=True):
            exito = guardar_visibilidad(st.session_state.productos_seleccionados, todos_los_nombres)
            if exito:
                st.success("✅ ¡Catálogo actualizado! Los cambios se verán en unos segundos.")
                st.rerun()
            else:
                st.error("Error al guardar. Intentá de nuevo.")
    
    st.markdown("---")

# --- FILTRAR PRODUCTOS VISIBLES (para visitantes) ---
if not st.session_state.admin_mode:
    df_catalogo = df_catalogo[df_catalogo["Visible_B2B"] == True]

# --- BUSCADOR ---
search = st.text_input("🔍 Buscar producto...", placeholder="Ej: Sal, Curry, Vital...", label_visibility="collapsed")

# --- CATÁLOGO POR PESTAÑAS ---
categorias = ["🏠 Todos", "🧂 Sales", "🌿 Blends", "💚 Vital", "🍵 Tés", "🍹 Mocktails", "🌶️ Pimientas"]
tabs = st.tabs(categorias)

for i, tab in enumerate(tabs):
    with tab:
        cat_actual = categorias[i]
        
        df_tab = df_catalogo.copy()
        if cat_actual != "🏠 Todos":
            df_tab = df_tab[df_tab["Categoria"] == cat_actual]
            
        # Poner DRY HOT HONEY arriba de todo en la pestaña Blends
        if cat_actual == "🌿 Blends" and not df_tab.empty:
            es_dry = df_tab["Nombre"].str.contains("dry|honey", case=False)
            df_tab = pd.concat([df_tab[es_dry], df_tab[~es_dry]])
            
        desc_path = os.path.join(current_dir, "Descripciones_RojoMalbec.md")
        
        if search:
            # Buscar coincidencia tanto en el nombre como en la descripción del producto
            mask_nombre = df_tab["Nombre"].str.contains(search, case=False, regex=False)
            mask_desc = df_tab["Nombre"].apply(lambda n: search.lower() in extraer_descripcion(n, desc_path).lower())
            df_tab = df_tab[mask_nombre | mask_desc]
            
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
                markup_revendedor = float(row.get("Markup_Revendedor", 0))
                if markup_revendedor > 0:
                    pvp_final = precio_mayorista * (1 + markup_revendedor / 100)
                else:
                    pvp_final = precio_mayorista * 1.5
                    
            pvp_redondeado = redondear_precio(pvp_final)
            ganancia_neta = pvp_redondeado - costo_redondeado
            
            descripcion = extraer_descripcion(nombre, desc_path)
            img_front, img_back = buscar_imagenes(nombre)
            
            qty_actual = st.session_state.carrito.get(nombre, {}).get("cantidad", 0)
            
            col_idx = idx % 2
            with cols[col_idx]:
                # Badge de cantidad en carrito o Novedad
                if qty_actual > 0:
                    badge_html = f"<div class='cart-badge'>{qty_actual}</div>"
                elif "dry" in nombre.lower() or "honey" in nombre.lower():
                    badge_html = "<div class='cart-badge' style='background:#d4af37; color:#000;'>🔥 NUEVO</div>"
                else:
                    badge_html = ""
                
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
                    # Selector de cantidad + botón de agregar
                    col_qty, col_btn = st.columns([1, 2])
                    with col_qty:
                        cant_elegida = st.selectbox("Cantidad", options=list(range(1, 101)), index=0, key=f"selqty_{cat_actual}_{idx}", label_visibility="collapsed")
                    with col_btn:
                        if st.button(f"🛒 AGREGAR ({cant_elegida} un.)", key=f"add_{cat_actual}_{idx}", use_container_width=True, type="primary"):
                            st.session_state.carrito[nombre] = {"cantidad": cant_elegida, "precio": costo_redondeado}
                            st.rerun()
                else:
                    # Ya está en el carrito
                    st.markdown(f"<div style='text-align:center; padding:6px; font-weight:800; font-size:1.1em; color:#d4af37; background:#1a1a24; border-radius:8px; margin-bottom:8px;'>{qty_actual} en pedido</div>", unsafe_allow_html=True)
                    
                    opciones_qty = list(range(1, 101))
                    idx_actual = opciones_qty.index(qty_actual) if qty_actual in opciones_qty else 0
                    
                    col_qty, col_btn = st.columns([1, 1])
                    with col_qty:
                        nueva_cant = st.selectbox("Cambiar cantidad", options=opciones_qty, index=idx_actual, key=f"qty_{cat_actual}_{idx}", label_visibility="collapsed")
                    with col_btn:
                        if st.button("✅ Actualizar", key=f"upd_{cat_actual}_{idx}", use_container_width=True):
                            st.session_state.carrito[nombre]['cantidad'] = nueva_cant
                            st.rerun()
                    
                    if st.button("🗑️ Quitar del pedido", key=f"del_{cat_actual}_{idx}", use_container_width=True):
                        del st.session_state.carrito[nombre]
                        st.rerun()
                
                # Separador visual entre tarjetas
                st.markdown("<div style='margin-bottom:10px;'></div>", unsafe_allow_html=True)
