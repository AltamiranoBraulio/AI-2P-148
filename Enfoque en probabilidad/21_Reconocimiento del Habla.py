import speech_recognition as sr

# Crear un objeto de reconocimiento
reconocedor = sr.Recognizer()

# Usar el micrófono como fuente
with sr.Microphone() as fuente:
    print("🎙️ Habla ahora, estoy escuchando...")
    # Ajusta al ruido ambiente
    reconocedor.adjust_for_ambient_noise(fuente)
    # Escuchar la voz
    audio = reconocedor.listen(fuente)

try:
    # Reconocer el audio usando Google
    texto = reconocedor.recognize_google(audio, language="es-ES")  # Español de España/Latinoamérica
    print("🔎 Texto reconocido:", texto)

except sr.UnknownValueError:
    print("😕 No entendí lo que dijiste.")
except sr.RequestError as e:
    print(f"❌ Error con el servicio de reconocimiento: {e}")
