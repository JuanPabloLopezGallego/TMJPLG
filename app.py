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
# ESTILOS — CÁLIDO Y AMIGABLE
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

    /* ═══ FONDO CÁLIDO ═══ */
    .stApp {
        background-color: var(--bg) !important;
        background-image:
            radial-gradient(circle at 8% 0%, rgba(255, 214, 165, 0.45), transparent 42%),
            radial-gradient(circle at 92% 100%, rgba(124, 198, 255, 0.22), transparent 45%),
            radial-gradient(circle at 50% 50%, rgba(255, 182, 193, 0.10), transparent 60%);
        background-attachment: fixed;
    }

    /* ═══ HERO ═══ */
    .hero {
        text-align: center;
        padding: 0.5rem 0 1.75rem 0;
    }
    .hero-badge {
        display: inline-block;
        background: var(--coral-soft);
        color: var(--coral);
        padding: 0.4rem 1rem;
        border-radius: 100px;
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        margin-bottom: 0.9rem;
    }
    .hero h1 {
        font-family: 'Fraunces', serif !important;
        font-size: 3rem !important;
        font-weight: 700 !important;
        color: var(--text) !important;
        margin: 0 0 0.55rem 0 !important;
        line-height: 1.05 !important;
        letter-spacing: -0.02em !important;
    }
    .hero h1 em {
        font-style: italic;
        color: var(--coral);
    }
    .hero p {
        color: var(--muted) !important;
        font-size: 1.05rem !important;
        margin: 0 !important;
        line-height: 1.5 !important;
    }

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
        color: #ffffff !important;
        border: none !important;
        border-radius: 14px !important;
        font-family: 'Nunito', sans-serif !important;
        font-weight: 800 !important;
        font-size: 0.95rem !important;
        padding: 0.7rem 1.6rem !important;
        box-shadow: 0 4px 16px rgba(255, 107, 107, 0.35) !important;
        transition: all 0.2s ease !important;
    }
    [data-testid="stCameraInput"] button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 26px rgba(255, 107, 107, 0.5) !important;
    }
    [data-testid="stCameraInput"] video {
        border-radius: 16px !important;
    }

    /* ═══ TARJETA DE RESULTADO ═══ */
    .result {
        background: #ffffff;
        border-radius: 28px;
        padding: 2.75rem 2rem 2.25rem 2rem;
        text-align: center;
        box-shadow: 0 16px 48px rgba(45, 42, 38, 0.09);
        margin-top: 1.75rem;
        position: relative;
        overflow: hidden;
    }
    .result::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; height: 6px;
        background: var(--emotion-color, var(--coral));
    }
    .emoji {
        font-size: 5.5rem;
        line-height: 1;
        margin-bottom: 1.25rem;
        display: block;
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
        padding: 0.4rem 1.15rem;
        border-radius: 100px;
        font-weight: 800;
        font-size: 0.85rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 1.1rem;
    }
    .greeting {
        font-family: 'Fraunces', serif !important;
        font-size: 1.95rem !important;
        font-weight: 700 !important;
        color: var(--text) !important;
        margin: 0 0 0.75rem 0 !important;
        line-height: 1.15 !important;
        letter-spacing: -0.01em !important;
    }
    .message {
        color: var(--muted) !important;
        font-size: 1.02rem !important;
        line-height: 1.6 !important;
        max-width: 480px;
        margin: 0 auto 2rem auto;
        font-weight: 500;
    }
    .conf-label {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        font-size: 0.72rem;
        font-weight: 800;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: var(--muted);
        margin-bottom: 0.55rem;
    }
    .conf-label span:last-child {
        font-family: 'Fraunces', serif;
        font-size: 1.35rem;
        letter-spacing: -0.02em;
        color: var(--emotion-color, var(--coral));
        text-transform: none;
        font-weight: 700;
    }
    .conf-track {
        height: 10px;
        background: #f5ede1;
        border-radius: 100px;
        overflow: hidden;
    }
    .conf-fill {
        height: 100%;
        border-radius: 100px;
        background: linear-gradient(90deg, var(--emotion-color, var(--coral)), var(--emotion-color-2, #ff8e53));
        transition: width 0.6s cubic-bezier(.4,0,.2,1);
    }

    /* ═══ SIDEBAR ═══ */
    [data-testid="stSidebar"] {
        background: #ffffff !important;
        border-right: 1px solid #f2e8dc !important;
    }
    [data-testid="stSidebar"] * { color: var(--text) !important; }

    .sb-title {
        font-family: 'Fraunces', serif;
        font-size: 1.2rem;
        font-weight: 700;
        margin: 0 0 0.4rem 0;
        letter-spacing: -0.01em;
    }
    .sb-text {
        color: var(--muted) !important;
        font-size: 0.92rem;
        line-height: 1.6;
        font-weight: 500;
    }
    .sb-emotions {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        margin-top: 1rem;
    }
    .sb-emotion {
        display: flex;
        align-items: center;
        gap: 0.85rem;
        padding: 0.7rem 0.95rem;
        background: #fef9f3;
        border-radius: 12px;
        font-size: 0.92rem;
        font-weight: 700;
        border: 1px solid #f7ecdc;
    }
    .sb-emotion span:first-child { font-size: 1.35rem; }

    .sb-tip {
        background: linear-gradient(135deg, #fff5e6, #fff);
        border: 1px solid #ffe4b8;
        border-radius: 14px;
        padding: 0.9rem 1rem;
        font-size: 0.86rem;
        color: #8a6d3b !important;
        line-height: 1.5;
        margin-top: 1rem;
        font-weight: 600;
    }

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
    [data-testid="stExpander"] summary:hover {
        color: var(--coral) !important;
    }

    /* ═══ ALERTAS ═══ */
    [data-testid="stAlert"] {
        border-radius: 14px !important;
        border: none !important;
    }

    /* ═══ SPINNER ═══ */
    .stSpinner > div {
        border-top-color: var(--coral) !important;
    }

    /* ═══ SEPARADOR Y CAPTION ═══ */
    hr {
        border-color: #f2e8dc !important;
        margin: 2rem 0 1rem 0 !important;
    }
    .stCaption, [data-testid="stCaptionContainer"] {
        color: var(--muted) !important;
        font-size: 0.82rem !important;
        text-align: center;
        font-weight: 500;
    }

    /* ═══ SCROLLBAR ═══ */
    ::-webkit-scrollbar { width: 10px; height: 10px; }
    ::-webkit-scrollbar-track { background: #fef9f3; }
    ::-webkit-scrollbar-thumb {
        background: #ffd6a5;
        border-radius: 10px;
        border: 2px solid #fef9f3;
    }
    ::-webkit-scrollbar-thumb:hover { background: var(--coral); }

    /* ═══ RESPONSIVE ═══ */
    @media (max-width: 640px) {
        .hero h1 { font-size: 2.2rem !important; }
        .emoji { font-size: 4rem; }
        .greeting { font-size: 1.5rem !important; }
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
    labels = ['Feliz', 'Triste', 'Enojado', 'Sorprendido', 'Nada']

while len(labels) < 5:
    labels.append(f"Clase {len(labels)}")


# ═══════════════════════════════════════════════════════════════
# METADATOS DE CADA EMOCIÓN
# ═══════════════════════════════════════════════════════════════
EMOTIONS = {
    'feliz': {
        'emoji': '😊',
        'label': 'Feliz',
        'greeting': '¡Hola! 😊',
        'message': '¡Qué alegría verte tan feliz! Contagia esa buena energía a todos los que te rodean.',
        'color': '#f59e0b',
        'color2': '#fbbf24',
        'bg': '#fef3c7',
    },
    'triste': {
        'emoji': '😢',
        'label': 'Triste',
        'greeting': 'Hola...',
        'message': 'Te noto triste. Recuerda que los días grises también pasan. ¡Un abrazo y ánimo!',
        'color': '#3b82f6',
        'color2': '#60a5fa',
        'bg': '#dbeafe',
    },
    'enojado': {
        'emoji': '😠',
        'label': 'Enojado',
        'greeting': 'Hola...',
        'message': 'Pareces enojado. Respira profundo, tómate un momento y verás todo más claro.',
        'color': '#ef4444',
        'color2': '#f87171',
        'bg': '#fee2e2',
    },
    'sorprendido': {
        'emoji': '😲',
        'label': 'Sorprendido',
        'greeting': '¡Hola!',
        'message': '¡Vaya, qué cara de sorpresa! ¿Qué ha pasado? Cuéntame esa gran noticia.',
        'color': '#8b5cf6',
        'color2': '#a78bfa',
        'bg': '#ede9fe',
    },
    'nada': {
        'emoji': '😐',
        'label': 'Sin emoción clara',
        'greeting': 'Hola',
        'message': 'No detecto una emoción marcada en tu rostro. Puedes intentarlo de nuevo con mejor luz.',
        'color': '#94a3b8',
        'color2': '#cbd5e1',
        'bg': '#f1f5f9',
    },
}


def obtener_info_emocion(nombre):
    """Devuelve el diccionario de metadatos para la etiqueta detectada."""
    key = nombre.strip().lower()
    for k, v in EMOTIONS.items():
        if k in key or key in k:
            return v
    return EMOTIONS['nada']


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
    try:
        img_deco = Image.open('OIG5.jpg')
        st.image(img_deco, use_container_width=True)
    except FileNotFoundError:
        pass
    except Exception:
        pass

    st.markdown('<div class="sb-title">😊 ¿Qué detecta?</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sb-text">Modelo entrenado en Teachable Machine capaz de reconocer 5 estados de ánimo:</div>',
        unsafe_allow_html=True,
    )
    st.markdown("""
        <div class="sb-emotions">
            <div class="sb-emotion"><span>😊</span><span>Feliz</span></div>
            <div class="sb-emotion"><span>😢</span><span>Triste</span></div>
            <div class="sb-emotion"><span>😠</span><span>Enojado</span></div>
            <div class="sb-emotion"><span>😲</span><span>Sorprendido</span></div>
            <div class="sb-emotion"><span>😐</span><span>Sin emoción</span></div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="sb-tip">💡 <b>Consejo:</b> usa buena iluminación, mira directo a la cámara y mantén tu rostro centrado para obtener mejores resultados.</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.caption(f"Python {platform.python_version()}")


# ═══════════════════════════════════════════════════════════════
# CÁMARA
# ═══════════════════════════════════════════════════════════════
img_file_buffer = st.camera_input("Toma una foto")


# ═══════════════════════════════════════════════════════════════
# PREDICCIÓN Y RESULTADO
# ═══════════════════════════════════════════════════════════════
if img_file_buffer is not None:
    # Preparar imagen
    img = Image.open(img_file_buffer)
    img = img.resize((224, 224))
    img_array = np.array(img)
    normalized = (img_array.astype(np.float32) / 127.0) - 1

    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    data[0] = normalized

    # Predecir
    with st.spinner("Analizando tu rostro..."):
        prediction = model.predict(data)

    idx = int(np.argmax(prediction[0]))
    conf = float(prediction[0][idx])
    detected_label = labels[idx] if idx < len(labels) else "Nada"
    info = obtener_info_emocion(detected_label)

    pct = min(100, int(conf * 100))

    # Tarjeta de resultado
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

    # Detalle de todas las probabilidades
    with st.expander("🔍 Ver todas las probabilidades del modelo"):
        for i, lbl in enumerate(labels):
            if i >= len(prediction[0]):
                break
            p = float(prediction[0][i])
            st.markdown(f"**{lbl}** — {p*100:.1f}%")


st.markdown("---")
st.caption("Modelo entrenado con Teachable Machine · Clasificación de emociones en tiempo real")
