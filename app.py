# ─────────────────────────────────────────────
# CARGA DEL MODELO
# ─────────────────────────────────────────────
@st.cache_resource
def cargar_modelo():
    return load_model('keras_model.h5')

try:
    model = cargar_modelo()
except Exception as e:
    st.error(f"❌ No se pudo cargar el modelo: {e}")
    st.stop()

# Intentar leer labels.txt
try:
    with open('labels.txt', 'r', encoding='utf-8') as f:
        labels = [l.strip() for l in f.readlines() if l.strip()]
    # Quitar prefijo numérico tipo "0 Feliz" → "Feliz"
    labels = [l.split(' ', 1)[1] if l[0].isdigit() else l for l in labels]
except FileNotFoundError:
    labels = ['Feliz', 'Triste', 'Enojado', 'Sorprendido', 'Nada']

# Asegurar 5 clases
while len(labels) < 5:
    labels.append(f"Clase {len(labels)}")

# ─────────────────────────────────────────────
# METADATOS DE CADA EMOCIÓN
# ─────────────────────────────────────────────
EMOTIONS = {
    'feliz': {
        'emoji': '😊',
        'label': 'Feliz',
        'greeting': '¡Hola! 😊',
        'message': '¡Qué alegría verte tan feliz! Contagia tu buena energía a todos.',
        'color': '#f59e0b',
        'color2': '#fbbf24',
        'bg': '#fef3c7',
    },
    'triste': {
        'emoji': '😢',
        'label': 'Triste',
        'greeting': 'Hola...',
        'message': 'Te noto triste. Recuerda que todo pasa y los días grises también terminan. ¡Ánimo!',
        'color': '#3b82f6',
        'color2': '#60a5fa',
        'bg': '#dbeafe',
    },
    'enojado': {
        'emoji': '😠',
        'label': 'Enojado',
        'greeting': 'Hola...',
        'message': 'Pareces enojado. Respira profundo, tómate un momento y todo se verá más claro.',
        'color': '#ef4444',
        'color2': '#f87171',
        'bg': '#fee2e2',
    },
    'sorprendido': {
        'emoji': '😲',
        'label': 'Sorprendido',
        'greeting': '¡Hola!',
        'message': '¡Vaya, qué cara de sorpresa! ¿Qué ha pasado? Cuéntame.',
        'color': '#8b5cf6',
        'color2': '#a78bfa',
        'bg': '#ede9fe',
    },
    'nada': {
        'emoji': '😐',
        'label': 'Sin emoción',
        'greeting': 'Hola',
        'message': 'No detecto una emoción clara en tu rostro. Puedes intentar de nuevo con mejor luz.',
        'color': '#94a3b8',
        'color2': '#cbd5e1',
        'bg': '#f1f5f9',
    },
}

def get_emotion_info(label_name):
    key = label_name.strip().lower()
    # Buscar por substring
    for k, v in EMOTIONS.items():
        if k in key or key in k:
            return v
    return EMOTIONS['nada']
