import streamlit as st
from PIL import Image
import base64
import io

# ═══════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Portafolio · Interfaces Multimodales",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ═══════════════════════════════════════════════════════════════
# ESTILOS
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --bg: #f7f4ed;
        --paper: #ffffff;
        --ink: #14120e;
        --muted: #7a7468;
        --muted-2: #a8a196;
        --border: #eae6dd;
        --accent: #ff5a36;
        --accent-soft: #fff0eb;
    }

    html, body, [class*="css"], .stApp {
        font-family: 'Inter', sans-serif !important;
        color: var(--ink);
    }

    h1, h2, h3, h4, h5 {
        font-family: 'Instrument Serif', serif !important;
        font-weight: 600 !important;
        letter-spacing: -0.015em !important;
        color: var(--ink) !important;
    }

    .stApp {
        background-color: var(--bg) !important;
        background-image:
            radial-gradient(circle at 12% -5%, rgba(255, 90, 54, 0.09), transparent 42%),
            radial-gradient(circle at 88% 105%, rgba(255, 200, 100, 0.12), transparent 42%);
        background-attachment: fixed;
    }

    /* Ocultar chrome de Streamlit */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header[data-testid="stHeader"] { background: transparent; }

    .block-container {
        padding-top: 3rem !important;
        padding-bottom: 3rem !important;
        max-width: 1280px !important;
    }

    /* ═══ HERO ═══ */
    .hero-kicker {
        display: inline-flex;
        align-items: center;
        gap: 0.6rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: var(--accent);
        font-weight: 500;
        margin-bottom: 1.2rem;
    }
    .hero-kicker::before {
        content: '';
        display: inline-block;
        width: 24px;
        height: 2px;
        background: var(--accent);
    }
    .hero-title {
        font-family: 'Instrument Serif', serif !important;
        font-size: 3.4rem !important;
        line-height: 1.02 !important;
        letter-spacing: -0.025em !important;
        font-weight: 600 !important;
        margin: 0 0 1.25rem 0 !important;
        color: var(--ink) !important;
    }
    .hero-title em {
        font-style: italic;
        color: var(--accent);
        font-weight: 400;
    }
    .hero-desc {
        font-size: 1.08rem;
        line-height: 1.65;
        color: var(--muted);
        margin: 0 0 1.75rem 0;
        max-width: 580px;
    }
    .hero-desc strong {
        color: var(--ink);
        font-weight: 600;
    }

    /* Chips */
    .chips {
        display: flex;
        flex-wrap: wrap;
        gap: 0.55rem;
    }
    .chip {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        background: #ffffff;
        border: 1px solid var(--border);
        border-radius: 100px;
        padding: 0.5rem 0.95rem;
        font-size: 0.83rem;
        font-weight: 500;
        color: var(--ink);
        transition: all 0.2s ease;
        white-space: nowrap;
    }
    .chip:hover {
        border-color: var(--accent);
        color: var(--accent);
        transform: translateY(-2px);
    }

    /* Retrato */
    .portrait-wrap {
        text-align: center;
        padding: 1rem 0;
    }
    .portrait-frame {
        background: var(--paper);
        border: 2px solid var(--ink);
        border-radius: 28px;
        padding: 1.25rem;
        box-shadow: 10px 10px 0 var(--accent);
        transform: rotate(-2.5deg);
        transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
        display: inline-block;
        width: 100%;
        max-width: 340px;
    }
    .portrait-frame:hover {
        transform: rotate(0deg) translateY(-4px);
        box-shadow: 14px 14px 0 var(--accent);
    }
    .portrait-frame img {
        width: 100%;
        display: block;
        border-radius: 14px;
    }
    .portrait-fallback {
        aspect-ratio: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 7rem;
        border-radius: 14px;
        background: #fff8ec;
    }
    .portrait-caption {
        margin-top: 1.5rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: var(--muted);
    }

    /* ═══ SECCIONES ═══ */
    .section-head {
        display: flex;
        align-items: flex-start;
        gap: 1.5rem;
        padding: 3rem 0 1.75rem 0;
        border-bottom: 1px solid var(--border);
        margin-bottom: 2rem;
    }
    .section-num {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        font-weight: 500;
        color: var(--accent);
        padding-top: 0.55rem;
        min-width: 32px;
    }
    .section-title {
        font-family: 'Instrument Serif', serif !important;
        font-size: 2.2rem !important;
        font-weight: 600 !important;
        line-height: 1 !important;
        margin: 0 0 0.35rem 0 !important;
        color: var(--ink) !important;
    }
    .section-sub {
        font-size: 0.95rem;
        color: var(--muted);
        margin: 0;
        font-weight: 400;
    }

    /* ═══ TARJETAS DE APP ═══ */
    .app-card {
        display: block !important;
        background: var(--paper);
        border: 1px solid var(--border);
        border-radius: 22px;
        overflow: hidden;
        text-decoration: none !important;
        color: var(--ink) !important;
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
        margin-bottom: 0.5rem;
        box-shadow: 0 1px 2px rgba(20, 18, 14, 0.02);
    }
    .app-card:hover {
        border-color: var(--accent);
        transform: translateY(-8px);
        box-shadow:
            0 24px 48px -12px rgba(20, 18, 14, 0.12),
            0 8px 16px -8px rgba(255, 90, 54, 0.15);
        text-decoration: none !important;
        color: var(--ink) !important;
    }
    .app-card-image {
        background: linear-gradient(135deg, #f5f1e8, #faf7f0);
        padding: 1.5rem;
        aspect-ratio: 16/10;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        border-bottom: 1px solid var(--border);
    }
    .app-card-image img {
        max-width: 100%;
        max-height: 100%;
        object-fit: contain;
        display: block;
        border-radius: 8px;
        transition: transform 0.4s ease;
    }
    .app-card:hover .app-card-image img {
        transform: scale(1.06);
    }
    .app-card-body {
        padding: 1.35rem 1.4rem 1.5rem 1.4rem;
    }
    .app-tag {
        display: inline-block;
        background: var(--accent-soft);
        color: var(--accent);
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.63rem;
        font-weight: 500;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        padding: 0.28rem 0.65rem;
        border-radius: 100px;
        margin-bottom: 0.85rem;
    }
    .app-title {
        font-family: 'Instrument Serif', serif !important;
        font-size: 1.45rem !important;
        font-weight: 600 !important;
        line-height: 1.1 !important;
        margin: 0 0 0.55rem 0 !important;
        color: var(--ink) !important;
        letter-spacing: -0.015em !important;
    }
    .app-desc {
        font-size: 0.88rem;
        line-height: 1.6;
        color: var(--muted);
        margin: 0 0 1.15rem 0;
    }
    .app-link {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        font-size: 0.83rem;
        font-weight: 600;
        color: var(--accent);
        transition: gap 0.2s ease;
    }
    .app-card:hover .app-link {
        gap: 0.75rem;
    }

    /* ═══ FOOTER ═══ */
    .footer {
        text-align: center;
        padding: 3rem 0 1rem 0;
        border-top: 1px solid var(--border);
        margin-top: 4rem;
    }
    .footer-mark {
        font-size: 1.5rem;
        color: var(--accent);
        margin-bottom: 0.75rem;
        display: block;
    }
    .footer-text {
        font-family: 'Instrument Serif', serif;
        font-size: 1.1rem;
        font-style: italic;
        color: var(--ink);
        margin: 0 0 0.4rem 0;
    }
    .footer-sub {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        color: var(--muted);
        margin: 0;
    }

    /* Links generales */
    .stMarkdown a { text-decoration: none !important; }

    /* Responsive */
    @media (max-width: 768px) {
        .hero-title { font-size: 2.3rem !important; }
        .section-title { font-size: 1.6rem !important; }
        .app-title { font-size: 1.25rem !important; }
        .block-container { padding-top: 1.5rem !important; }
    }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════
@st.cache_data
def img_to_b64(path):
    """Convierte una imagen a base64 para incrustarla en HTML."""
    try:
        img = Image.open(path)
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        return base64.b64encode(buf.getvalue()).decode()
    except Exception:
        return None


def section_header(num, title, subtitle):
    st.markdown(f"""
        <div class="section-head">
            <div class="section-num">{num}</div>
            <div>
                <h2 class="section-title">{title}</h2>
                <p class="section-sub">{subtitle}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)


def app_card(image_path, tag, title, desc, url):
    b64 = img_to_b64(image_path)
    if b64:
        image_html = f'<img src="data:image/png;base64,{b64}" alt="{title}" />'
    else:
        image_html = '<div style="font-size:3rem;">🖼️</div>'
    return f"""
        <a href="{url}" target="_blank" class="app-card">
            <div class="app-card-image">{image_html}</div>
            <div class="app-card-body">
                <span class="app-tag">{tag}</span>
                <h3 class="app-title">{title}</h3>
                <p class="app-desc">{desc}</p>
                <span class="app-link">Abrir aplicación →</span>
            </div>
        </a>
    """


# ═══════════════════════════════════════════════════════════════
# HERO — ILUSTRACIÓN + PRESENTACIÓN
# ═══════════════════════════════════════════════════════════════
col_left, col_right = st.columns([1, 1.7], gap="large")

with col_left:
    b64 = img_to_b64('yo.png')
    if b64:
        st.markdown(f"""
            <div class="portrait-wrap">
                <div class="portrait-frame">
                    <img src="data:image/png;base64,{b64}" alt="Ilustración de perfil" />
                </div>
                <div class="portrait-caption">Diseño interactivo · 2026</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class="portrait-wrap">
                <div class="portrait-frame">
                    <div class="portrait-fallback">👋</div>
                </div>
                <div class="portrait-caption">Diseño interactivo · 2026</div>
            </div>
        """, unsafe_allow_html=True)

with col_right:
    st.markdown("""
        <div class="hero-kicker">Portafolio · 2026</div>
        <h1 class="hero-title">Hola, soy estudiante de <em>Diseño Interactivo</em></h1>
        <p class="hero-desc">
            Tengo <strong>20 años</strong> y estudio en <strong>EAFIT</strong>. Este portafolio reúne
            los proyectos que desarrollé en la materia de <strong>Interfaces Multimodales</strong>
            del 2026, donde exploramos cómo la inteligencia artificial puede extender nuestros
            sentidos y crear nuevas formas de interacción.
        </p>
        <div class="chips">
            <span class="chip">🎓 EAFIT</span>
            <span class="chip">🎨 Diseño Interactivo</span>
            <span class="chip">📅 20 años</span>
            <span class="chip">✨ Interfaces Multimodales 2026</span>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# SECCIÓN 01 · VISTA ARTIFICIAL
# ═══════════════════════════════════════════════════════════════
section_header(
    "01",
    "Vista artificial",
    "Modelos que interpretan imágenes y entienden lo que ven",
)

c1, c2, c3 = st.columns(3, gap="medium")
with c1:
    st.markdown(app_card(
        'OCD.PNG',
        'OCR · Texto en imágenes',
        'Lector de texto',
        'Detecta y extrae automáticamente el texto presente en cualquier imagen.',
        'https://reconocertextojplg-6juwyccehm7tzvrc4olrgc.streamlit.app/#lector-de-texto'
    ), unsafe_allow_html=True)
with c2:
    st.markdown(app_card(
        'DetectorYolo.PNG',
        'Objetos · YOLOv5',
        'Detector de objetos',
        'Identifica objetos del mundo físico en tiempo real usando el modelo YOLOv5.',
        'https://yolov5jplg-jhz4oyznamsgwqesdqsjur.streamlit.app/#deteccion-de-objetos'
    ), unsafe_allow_html=True)
with c3:
    st.markdown(app_card(
        'DetectorTM.PNG',
        'Emociones · Teachable Machine',
        'Detector de emociones',
        'Reconoce expresiones faciales entrenadas con Teachable Machine.',
        'https://tmjplg-mb3ejw24ybs3q9me8rjvnv.streamlit.app/'
    ), unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# SECCIÓN 02 · LENGUAJE Y SIGNIFICADO
# ═══════════════════════════════════════════════════════════════
section_header(
    "02",
    "Lenguaje y significado",
    "Cómo la IA lee, interpreta y visualiza el texto",
)

c1, c2, c3 = st.columns(3, gap="medium")
with c1:
    st.markdown(app_card(
        'AnalisisSentimiento.PNG',
        'NLP · Sentimiento',
        'Analizador de sentimientos',
        'Analiza la polaridad y subjetividad de cualquier frase en español.',
        'https://2mlysjdw4svsaudjglrkzt.streamlit.app/'
    ), unsafe_allow_html=True)
with c2:
    st.markdown(app_card(
        'TF.PNG',
        'Búsqueda · TF-IDF',
        'Recuperación de información',
        'Encuentra el documento más relevante a partir de una pregunta en lenguaje natural.',
        'https://tf-idf-jplg-pufez8g8jqz82ru5wbvp5e.streamlit.app/'
    ), unsafe_allow_html=True)
with c3:
    st.markdown(app_card(
        'Wordcloud.PNG',
        'Visual · Nube de palabras',
        'Nube de palabras',
        'Genera representaciones visuales del texto destacando las palabras más frecuentes.',
        'https://vision2-gpt4o.streamlit.app/'
    ), unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# SECCIÓN 03 · VOZ Y SONIDO
# ═══════════════════════════════════════════════════════════════
section_header(
    "03",
    "Voz y sonido",
    "Interfaces que escuchan, hablan y traducen",
)

c1, c2, c3 = st.columns(3, gap="medium")
with c1:
    st.markdown(app_card(
        'Voxlab.PNG',
        'Voz · Texto a voz',
        'Texto a voz',
        'Convierte cualquier texto escrito en audio con voz natural.',
        'https://imm1copiajplg-zdpnlzjgnlatk4cbll7wlj.streamlit.app/'
    ), unsafe_allow_html=True)
with c2:
    st.markdown(app_card(
        'VoxTranslate.PNG',
        'Voz · Voz a texto',
        'Voz a texto',
        'Escucha lo que dices, lo traduce y lo convierte en texto.',
        'https://traductorjplg-9zcgnf8wypri8t5yksyfsg.streamlit.app/'
    ), unsafe_allow_html=True)
with c3:
    st.markdown(app_card(
        'OCRTraductor.PNG',
        'OCR + Traducción + Audio',
        'OCR + texto a audio',
        'Detecta texto en imágenes, lo traduce y genera audio en una sola app.',
        'https://traductorextranjeros-jk7eekmjpdskckeba6x8mk.streamlit.app/'
    ), unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# SECCIÓN 04 · PRIMER PROYECTO
# ═══════════════════════════════════════════════════════════════
section_header(
    "04",
    "El primer paso",
    "Donde empezó todo este recorrido",
)

c1, c2, c3 = st.columns([1, 1, 1], gap="medium")
with c1:
    st.markdown(app_card(
        'Primera.PNG',
        'Origen · Streamlit',
        'Mi primera página web',
        'El primer proyecto que me introdujo al mundo de las apps interactivas con Streamlit.',
        'https://miprimerapagina-5gzdhzssqjm77bzqcehwe5.streamlit.app/'
    ), unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════
st.markdown("""
    <div class="footer">
        <span class="footer-mark">✦</span>
        <p class="footer-text">Hecho con curiosidad desde Medellín</p>
        <p class="footer-sub">EAFIT · Interfaces Multimodales · 2026</p>
    </div>
""", unsafe_allow_html=True)
