import streamlit as st
import cv2
import numpy as np
from PIL import Image as Image, ImageOps as ImagOps
from keras.models import load_model
import platform

# ═══════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Detector de Emociones",
    page_icon="😊",
    layout="centered",
)

# ═══════════════════════════════════════════════════════════════
# ESTILOS
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Nunito:wght@400;500;600;700;800&display=swap');

    :root {
        --bg: #fef9f3;
        --card: #ffffff;
        --text: #2d2a26;
        --muted: #8a8078;
        --coral: #ff6b6b;
        --coral-soft: #ffe5e5;
    }

    html, body, [class*="css"], .stApp {
        font-family: 'Nunito', sans-serif !important;
        color: var(--text) !important;
    }

    .stApp {
        background-color: var(--bg) !important;
        background-image:
            radial-gradient(circle at 8% 0%, rgba(255, 214, 165, 0.45), transparent 42%),
            radial-gradient(circle at 92% 100%, rgba(124, 198, 255, 0.22), transparent 45%),
            radial-gradient(circle at 50% 50%, rgba(255, 182, 193, 0.10), transparent 60%);
        background-attachment: fixed;
    }

    /* ═══ HERO ═══ */
    .hero { text-align: center; padding: 0.5rem 0 1.75rem 0; }
    .hero-badge {
        display: inline-block;
        background: var(--coral-soft); color: var(--coral);
        padding: 0.4rem 1rem; border-radius: 100px;
        font-size: 0.72rem; font-weight: 800;
        letter-spacing: 0.14em; text-transform: uppercase;
        margin-bottom: 0.9rem;
    }
    .hero h1 {
        font-family: 'Fraunces', serif !important;
        font-size: 3rem !important; font-weight: 700 !important;
        color: var(--text) !important;
        margin: 0 0 0.55rem 0 !important;
        line-height: 1.05 !important; letter-spacing: -0.02em !important;
    }
    .hero h1 em { font-style: italic; color: var(--coral); }
    .hero p { color: var(--muted) !important; font-size: 1.05rem !important; margin: 0 !important; }

    /* ═══ TIP PROMINENTE ANTES DE LA CÁMARA ═══ */
    .pro-tip {
        display: flex;
        align-items: flex-start;
        gap: 1rem;
        background: linear-gradient(135deg, #fff5e6 0%, #fffefb 100%);
        border: 1.5px solid #ffe0b3;
        border-left: 5px solid #f59e0b;
        border-radius: 16px;
        padding: 1.1rem 1.3rem;
        margin: 0 0 1.25rem 0;
        box-shadow: 0 4px 16px rgba(245, 158, 11, 0.08);
    }
    .pro-tip .icon {
        font-size: 1.8rem;
        line-height: 1;
        flex-shrink: 0;
    }
    .pro-tip .body { flex: 1; }
    .pro-tip .title {
        font-weight: 800;
        font-size: 0.95rem;
        color: #7c5f1c;
        margin-bottom: 0.35rem;
        letter-spacing: 0.01em;
    }
    .pro-tip .text {
        font-size: 0.9rem;
        color: #8a6d3b;
        line-height: 1.55;
        font-weight: 500;
    }
    .pro-tip .text b { color: #7c5f1c; font-weight: 800; }

    /* ═══ CAMERA INPUT ═══ */
    [data-testid="stCameraInput"] {
        background: #ffffff !important;
        border: 2px dashed #ecdcc8 !important;
        border-radius: 24px !important;
        padding: 1.4rem !important;
        box-shadow: 0 8px 32px rgba(255, 107, 107, 0.07) !important;
    }
    [data-testid="stCameraInput"] button {
        background: linear-gradient(135deg, #ff6b6b, #ff8e53) !important;
        color: #ffffff !important; border: none !important;
        border-radius: 14px !important;
        font-family: 'Nunito', sans-serif !important;
        font-weight: 800 !important; font-size: 0.95rem !important;
        padding: 0.7rem 1.6rem !important;
        box-shadow: 0 4px 16px rgba(255, 107, 107, 0.35) !important;
        transition: all 0.2s ease !important;
    }
    [data-testid="stCameraInput"] button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 26px rgba(255, 107, 107, 0.5) !important;
    }
    [data-testid="stCameraInput"] video { border-radius: 16px !important; }

    /* ═══ TARJETA DE RESULTADO ═══ */
    .result {
        background: #ffffff; border-radius: 28px;
        padding: 2.75rem 2rem 2.25rem 2rem;
        text-align: center;
        box-shadow: 0 16px 48px rgba(45, 42, 38, 0.09);
        margin-top: 1.75rem;
        position: relative; overflow: hidden;
    }
    .result::before {
        content: ''; position: absolute;
        top: 0; left: 0; right: 0; height: 6px;
        background: var(--emotion-color, var(--coral));
    }
    .emoji {
        font-size: 5.5rem; line-height: 1;
        margin-bottom: 1.25rem; display: block;
        animation: floaty 2.4s ease-in-out infinite;
    }
    @keyframes floaty {
        0%, 100% { transform: translateY(0) rotate(0deg); }
        50%      { transform: translateY(-10px) rotate(-3deg); }
    }
    .emotion-label {
        display: inline-block;
        background: var(--emotion-bg, var(--coral-soft));
        color: var(--emotion-color, var(--coral));
        padding: 0.4rem 1.15rem; border-radius: 100px;
        font-weight: 800; font-size: 0.85rem;
        letter-spacing: 0.12em; text-transform: uppercase;
        margin-bottom: 1.1rem;
    }
    .greeting {
        font-family: 'Fraunces', serif !important;
        font-size: 1.95rem !important; font-weight: 700 !important;
        color: var(--text) !important;
        margin: 0 0 0.75rem 0 !important; line-height: 1.15 !important;
    }
    .message {
        color: var(--muted) !important;
        font-size: 1.02rem !important; line-height: 1.6 !important;
        max-width: 480px; margin: 0 auto 2rem auto; font-weight: 500;
    }
    .conf-label {
        display: flex; justify-content: space-between; align-items: baseline;
        font-size: 0.72rem; font-weight: 800;
        letter-spacing: 0.14em; text-transform: uppercase;
        color: var(--muted); margin-bottom: 0.55rem;
    }
    .conf-label span:last-child {
        font-family: 'Fraunces', serif;
        font-size: 1.35rem; letter-spacing: -0.02em;
        color: var(--emotion-color, var(--coral));
        text-transform: none; font-weight: 700;
    }
    .conf-track {
        height: 10px; background: #f5ede1;
        border-radius: 100px; overflow: hidden;
    }
    .conf-fill {
        height: 100%; border-radius: 100px;
        background: linear-gradient(90deg, var(--emotion-color, var(--coral)), var(--emotion-color-2, #ff8e53));
        transition: width 0.6s cubic-bezier(.4,0,.2,1);
    }

    /* ═══ DISTRIBUCIÓN DE PROBABILIDADES ═══ */
    .dist-card {
        background: #ffffff; border-radius: 22px;
        padding: 1.5rem 1.6rem;
        box-shadow: 0 8px 28px rgba(45, 42, 38, 0.06);
        margin-top: 1.5rem;
    }
    .dist-title {
        font-family: 'Fraunces', serif;
        font-size: 1.15rem; font-weight: 700;
        margin: 0 0 1.1rem 0; color: var(--text);
        display: flex; justify-content: space-between; align-items: center;
    }
    .dist-title small {
        font-family: 'Nunito', sans-serif;
        font-size: 0.72rem; font-weight: 700;
        letter-spacing: 0.1em; text-transform: uppercase;
        color: var(--muted);
    }
    .dist-row {
        display: grid;
        grid-template-columns: 34px 100px 1fr 52px;
        align-items: center;
        gap: 0.75rem;
        padding: 0.55rem 0.85rem;
        border-radius: 12px;
        transition: background 0.15s ease;
    }
    .dist-row.top { background: #fff8ec; }
    .dist-row .e { font-size: 1.4rem; line-height: 1; }
    .dist-row .n {
        font-weight: 700; font-size: 0.9rem;
        color: var(--text); text-transform: capitalize;
    }
    .dist-row .b {
        height: 8px; background: #f5ede1;
        border-radius: 100px; overflow: hidden;
    }
    .dist-row .b > div {
        height: 100%; border-radius: 100px;
        transition: width 0.5s ease;
    }
    .dist-row .p {
        font-family: 'Fraunces', serif;
        font-size: 1rem; font-weight: 700;
        text-align: right; color: var(--text);
        font-variant-numeric: tabular-nums;
    }

    /* ═══ AVISO ═══ */
    .warn {
        background: linear-gradient(135deg, #fff8e1, #fffaf0);
        border: 1px solid #fde68a;
        border-left: 4px solid #f59e0b;
        border-radius: 14px;
        padding: 1rem 1.15rem;
        margin-top: 1.2rem;
        font-size: 0.92rem;
        color: #7c5f1c !important;
        line-height: 1.55;
        font-weight: 600;
    }
    .warn b { color: #7c5f1c !important; }
    .warn em { font-style: italic; color: #a16207 !important; }

    /* ═══ SIDEBAR ═══ */
    [data-testid="stSidebar"] {
        background: #ffffff !important;
        border-right: 1px solid #f2e8dc !important;
    }
    [data-testid="stSidebar"] * { color: var(--text) !important; }

    .sb-title {
        font-family: 'Fraunces', serif;
        font-size: 1.2rem; font-weight: 700;
        margin: 0 0 0.4rem 0;
    }
    .sb-text {
        color: var(--muted) !important;
        font-size: 0.92rem; line-height: 1.6; font-weight: 500;
    }

    /* ═══ TARJETA DECORATIVA EN SIDEBAR (reemplaza OIG5.jpg) ═══ */
    .sb-hero-card {
        background: linear-gradient(135deg, #fff5e6 0%, #ffe5e5 55%, #fef3c7 100%);
        border-radius: 20px;
        padding: 1.4rem 1.2rem;
        text-align: center;
        margin-bottom: 1.4rem;
        position: relative;
        overflow: hidden;
        border: 1px solid #ffe0b3;
    }
    .sb-hero-card::before {
        content: '';
        position: absolute;
        top: -30px; right: -30px;
        width: 100px; height: 100px;
        background: radial-gradient(circle, rgba(255, 107, 107, 0.20), transparent 70%);
        border-radius: 50%;
    }
    .sb-hero-card .camera {
        font-size: 2.8rem;
        line-height: 1;
        display: block;
        margin-bottom: 0.5rem;
        filter: drop-shadow(0 4px 12px rgba(255, 107, 107, 0.35));
    }
    .sb-hero-card .tagline {
        font-family: 'Fraunces', serif;
        font-size: 1.05rem;
        font-weight: 700;
        color: var(--text);
        letter-spacing: -0.01em;
        line-height: 1.2;
    }
    .sb-hero-card .sub {
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: #b8854a;
        margin-top: 0.45rem;
    }

    /* ═══ GRID DE EMOCIONES EN SIDEBAR ═══ */
    .sb-emo-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0.6rem;
        margin-top: 1rem;
    }
    .sb-emo {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 0.75rem 0.5rem;
        background: #fef9f3;
        border-radius: 12px;
        border: 1px solid #f7ecdc;
        transition: all 0.15s ease;
    }
    .sb-emo:hover {
        background: #fff4e6;
        border-color: #ffe0b3;
        transform: translateY(-2px);
    }
    .sb-emo .face { font-size: 1.8rem; line-height: 1; margin-bottom: 0.35rem; }
    .sb-emo .name {
        font-size: 0.78rem;
        font-weight: 700;
        color: var(--text);
        text-transform: capitalize;
    }

    /* ═══ TIPS EN SIDEBAR ═══ */
    .sb-tip {
        background: linear-gradient(135deg, #fff5e6, #fff);
        border: 1px solid #ffe4b8;
        border-radius: 14px;
        padding: 1rem 1.05rem;
        font-size: 0.86rem;
        color: #8a6d3b !important;
        line-height: 1.55;
        margin-top: 1.2rem;
        font-weight: 500;
    }
    .sb-tip .h {
        display: block;
        font-weight: 800;
        color: #7c5f1c !important;
        margin-bottom: 0.5rem;
        font-size: 0.8rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }
    .sb-tip ul {
        margin: 0;
        padding-left: 1.1rem;
    }
    .sb-tip li {
        margin-bottom: 0.35rem;
        color: #8a6d3b !important;
    }
    .sb-tip b { color: #7c5f1c !important; font-weight: 800; }

    /* ═══ EXPANDER ═══ */
    [data-testid="stExpander"] {
        background: #ffffff !important;
        border: 1px solid #f2e8dc !important;
        border-radius: 16px !important;
        overflow: hidden;
    }
    [data-testid="stExpander"] summary {
        font-weight: 700 !important;
        color: var(--text) !important;
        padding: 0.85rem 1rem !important;
    }
    [data-testid="stExpander"] summary:hover { color: var(--coral) !important; }

    /* ═══ ALERTAS / SPINNER / HR / CAPTION ═══ */
    [data-testid="stAlert"] { border-radius: 14px !important; border: none !important; }
    .stSpinner > div { border-top-color: var(--coral) !important; }
    hr { border-color: #f2e8dc !important; margin: 2rem 0 1rem 0 !important; }
    .stCaption, [data-testid="stCaptionContainer"] {
        color: var(--muted) !important;
        font-size: 0.82rem !important;
        text-align: center; font-weight: 500;
    }

    /* ═══ SCROLLBAR ═══ */
    ::-webkit-scrollbar { width: 10px; height: 10px; }
    ::-webkit-scrollbar-track { background: #fef9f3; }
    ::-webkit-scrollbar-thumb {
        background: #ffd6a5; border-radius: 10px;
        border: 2px solid #fef9f3;
    }
    ::-webkit-scrollbar-thumb:hover { background: var(--coral); }

    @media (max-width: 640px) {
        .hero h1 { font-size: 2.2rem !important; }
        .emoji { font-size: 4rem; }
        .greeting { font-size: 1.5rem !important; }
        .dist-row { grid-template-columns: 30px 80px 1fr 44px; gap: 0.5rem; }
    }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# CARGA DEL MODELO
# ═══════════════════════════════════════════════════════════════
@st.cache_resource
def cargar_modelo():
    return load_model('keras_model.h5')

try:
    model = cargar_modelo()
except Exception as e:
    st.error(f"❌ No se pudo cargar el modelo: {e}")
    st.stop()


# ═══════════════════════════════════════════════════════════════
# ETIQUETAS DE CLASE
# ═══════════════════════════════════════════════════════════════
try:
    with open('labels.txt', 'r', encoding='utf-8') as f:
        labels = []
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(' ', 1)
            if len(parts) == 2 and parts[0].isdigit():
                labels.append(parts[1].strip())
            else:
                labels.append(line)
except FileNotFoundError:
    labels = ['Feliz', 'Triste', 'Sorprendido', 'Nada', 'Enojado']

while len(labels) < 5:
    labels.append(f"Clase {len(labels)}")


# ═══════════════════════════════════════════════════════════════
# EXCLUIR LA CATEGORÍA "ENOJADO" (y variantes)
# ═══════════════════════════════════════════════════════════════
EXCLUDE_KEYWORDS = ('enojad', 'angry', 'enojo', 'ira', 'furia', 'rage')

def es_excluida(nombre):
    n = nombre.strip().lower()
    return any(k in n for k in EXCLUDE_KEYWORDS)

# Índices válidos = los que NO corresponden a la categoría excluida
valid_indices = [i for i, lbl in enumerate(labels) if not es_excluida(lbl)]
if not valid_indices:
    valid_indices = list(range(len(labels)))


# ═══════════════════════════════════════════════════════════════
# METADATOS DE CADA EMOCIÓN (sin "enojado")
# ═══════════════════════════════════════════════════════════════
EMOTIONS = {
    'feliz': {
        'emoji': '😊', 'label': 'Feliz', 'greeting': '¡Hola! 😊',
        'message': '¡Qué alegría verte tan feliz! Contagia esa buena energía a todos los que te rodean.',
        'color': '#f59e0b', 'color2': '#fbbf24', 'bg': '#fef3c7',
    },
    'triste': {
        'emoji': '😢', 'label': 'Triste', 'greeting': 'Hola...',
        'message': 'Te noto triste. Recuerda que los días grises también pasan. ¡Un abrazo y ánimo!',
        'color': '#3b82f6', 'color2': '#60a5fa', 'bg': '#dbeafe',
    },
    'sorprendido': {
        'emoji': '😲', 'label': 'Sorprendido', 'greeting': '¡Hola!',
        'message': '¡Vaya, qué cara de sorpresa! ¿Qué ha pasado? Cuéntame esa gran noticia.',
        'color': '#8b5cf6', 'color2': '#a78bfa', 'bg': '#ede9fe',
    },
    'nada': {
        'emoji': '😐', 'label': 'Sin emoción clara', 'greeting': 'Hola',
        'message': 'No detecto una emoción marcada en tu rostro. Intenta exagerar tu expresión y vuelve a probar.',
        'color': '#94a3b8', 'color2': '#cbd5e1', 'bg': '#f1f5f9',
    },
    'neutral': {
        'emoji': '😐', 'label': 'Neutral', 'greeting': 'Hola',
        'message': 'Tu rostro se ve tranquilo y neutral. Todo en calma por aquí.',
        'color': '#94a3b8', 'color2': '#cbd5e1', 'bg': '#f1f5f9',
    },
}


def obtener_info_emocion(nombre):
    key = nombre.strip().lower()
    for k, v in EMOTIONS.items():
        if k in key or key in k:
            return v
    return EMOTIONS['nada']


def color_de_emocion(nombre):
    return obtener_info_emocion(nombre)['color']


# ═══════════════════════════════════════════════════════════════
# HERO
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
    <div class="hero-badge">Reconocimiento facial · IA</div>
    <h1>Detector de <em>emociones</em></h1>
    <p>Mira a la cámara y descubre qué emoción refleja tu rostro.</p>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    # Tarjeta decorativa (reemplaza OIG5.jpg)
    st.markdown("""
        <div class="sb-hero-card">
            <span class="camera">📷</span>
            <div class="tagline">Tu rostro,<br>en tiempo real</div>
            <div class="sub">Modelo · Teachable Machine</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-title">😊 ¿Qué detecta?</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sb-text">Modelo entrenado en Teachable Machine capaz de reconocer 4 estados de ánimo:</div>',
        unsafe_allow_html=True,
    )

    st.markdown("""
        <div class="sb-emo-grid">
            <div class="sb-emo"><span class="face">😊</span><span class="name">Feliz</span></div>
            <div class="sb-emo"><span class="face">😢</span><span class="name">Triste</span></div>
            <div class="sb-emo"><span class="face">😲</span><span class="name">Sorprendido</span></div>
            <div class="sb-emo"><span class="face">😐</span><span class="name">Sin emoción</span></div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="sb-tip">
            <span class="h">✨ Cómo mejorar la detección</span>
            <ul>
                <li><b>Exagera</b> la expresión facial, no la hagas sutil.</li>
                <li>Usa <b>buena iluminación frontal</b>, sin contraluz.</li>
                <li>Mantén el rostro <b>centrado y cerca</b> de la cámara.</li>
                <li>Evita gorras, gafas oscuras o mascarillas.</li>
                <li>Haz la expresión y <b>espera 2 segundos</b> antes de capturar.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.caption(f"Python {platform.python_version()}")


# ═══════════════════════════════════════════════════════════════
# TIP PROMINENTE ANTES DE LA CÁMARA
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div class="pro-tip">
    <div class="icon">💡</div>
    <div class="body">
        <div class="title">Exagera tu expresión para mejores resultados</div>
        <div class="text">
            El modelo aprende mejor con gestos <b>marcados</b>. Si quieres aparecer
            <b>feliz</b>, sonríe ampliamente mostrando los dientes. Si estás <b>sorprendido</b>,
            abre bien los ojos y la boca. Las expresiones sutiles suelen clasificarse como
            <b>"sin emoción"</b>.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# CÁMARA
# ═══════════════════════════════════════════════════════════════
img_file_buffer = st.camera_input("Toma una foto")


# ═══════════════════════════════════════════════════════════════
# PREDICCIÓN Y RESULTADO
# ═══════════════════════════════════════════════════════════════
if img_file_buffer is not None:
    img = Image.open(img_file_buffer)
    img = img.resize((224, 224))
    img_array = np.array(img)
    normalized = (img_array.astype(np.float32) / 127.0) - 1

    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    data[0] = normalized

    with st.spinner("Analizando tu rostro..."):
        prediction = model.predict(data)

    probs = prediction[0]

    # ── Enmascaramos la clase excluida (enojado) ──
    masked = probs.copy()
    for i in range(len(masked)):
        if i not in valid_indices:
            masked[i] = -1.0

    idx = int(np.argmax(masked))
    conf = float(probs[idx])
    detected_label = labels[idx] if idx < len(labels) else "Nada"
    info = obtener_info_emocion(detected_label)
    pct = min(100, int(conf * 100))

    # ── Tarjeta principal ──
    st.markdown(f"""
        <div class="result" style="
            --emotion-color: {info['color']};
            --emotion-color-2: {info['color2']};
            --emotion-bg: {info['bg']};
        ">
            <span class="emoji">{info['emoji']}</span>
            <div class="emotion-label">{info['label']}</div>
            <div class="greeting">{info['greeting']}</div>
            <p class="message">{info['message']}</p>
            <div class="conf-label">
                <span>Confianza</span>
                <span>{pct}%</span>
            </div>
            <div class="conf-track">
                <div class="conf-fill" style="width: {pct}%;"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # ── Barras con las probabilidades (excluyendo enojado) ──
    orden = [i for i in np.argsort(probs)[::-1] if i in valid_indices]
    rows_html = ""
    for pos, real_idx in enumerate(orden):
        lbl = labels[real_idx] if real_idx < len(labels) else f"Clase {real_idx}"
        p = float(probs[real_idx])
        ppct = p * 100
        emoji_e = obtener_info_emocion(lbl)['emoji']
        color_e = color_de_emocion(lbl)
        top_class = " top" if pos == 0 else ""
        rows_html += f"""
            <div class="dist-row{top_class}">
                <div class="e">{emoji_e}</div>
                <div class="n">{lbl}</div>
                <div class="b"><div style="width:{ppct}%; background:{color_e};"></div></div>
                <div class="p">{ppct:.1f}%</div>
            </div>
        """

    st.markdown(f"""
        <div class="dist-card">
            <div class="dist-title">
                Distribución de probabilidades
                <small>ordenado de mayor a menor</small>
            </div>
            {rows_html}
        </div>
    """, unsafe_allow_html=True)

    # ── Aviso si la decisión no es clara ──
    valid_probs = np.array([probs[i] for i in valid_indices])
    sorted_valid = np.sort(valid_probs)[::-1]
    if len(sorted_valid) >= 2:
        gap = sorted_valid[0] - sorted_valid[1]
        if conf < 0.5 or gap < 0.15:
            top1 = labels[orden[0]]
            top2 = labels[orden[1]]
            st.markdown(f"""
                <div class="warn">
                    ⚠️ <b>Resultado poco claro.</b> El modelo duda entre
                    <em>{top1}</em> y <em>{top2}</em>.
                    Intenta <b>exagerar más la expresión</b>, mejora la iluminación
                    o acerca el rostro a la cámara.
                </div>
            """, unsafe_allow_html=True)

    # ── Valores crudos ──
    with st.expander("🔍 Ver valores exactos del modelo"):
        for i, lbl in enumerate(labels):
            if i >= len(probs):
                break
            p = float(probs[i])
            excluida = " *(excluida)*" if i not in valid_indices else ""
            st.markdown(f"**{lbl}**{excluida} — `{p:.6f}`")


st.markdown("---")
st.caption("Modelo entrenado con Teachable Machine · Clasificación de emociones en tiempo real")
