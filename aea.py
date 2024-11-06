import pyttsx3

# Inicializa el motor de texto a voz
engine = pyttsx3.init()

# Obtener todas las voces disponibles
voices = engine.getProperty('voices')

# Imprimir las voces y sus propiedades
for voice in voices:
    print(f"Nombre: {voice.name}")
    print(f"Idioma(s): {voice.languages}")
    print(f"Género: {'Masculino' if 'male' in voice.name.lower() else 'Femenino' if 'female' in voice.name.lower() else 'Desconocido'}")
    print("-" * 30)