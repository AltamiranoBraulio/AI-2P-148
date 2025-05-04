# Importamos la librería OpenCV, que nos permite procesar imágenes y videos
import cv2  

# Importamos numpy para realizar operaciones matemáticas (aunque en este código no es indispensable)
import numpy as np  

# Abrimos la cámara web (el '0' indica la cámara por defecto)
# También podrías poner un archivo de video, por ejemplo: 'video.mp4'
cap = cv2.VideoCapture(0)

# Leemos el primer frame (imagen) de la cámara para usarlo como referencia inicial
ret, frame1 = cap.read()

# Convertimos esa imagen a escala de grises para simplificar el análisis
# Trabajar en escala de grises es más rápido que trabajar con color (3 canales RGB)
gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

# Aplicamos un desenfoque (blur) con un filtro Gaussiano
# Esto ayuda a eliminar pequeños ruidos y variaciones de luz que podrían confundirse con movimiento
gray1 = cv2.GaussianBlur(gray1, (21, 21), 0)

# Entramos en un bucle para procesar frame por frame mientras la cámara esté abierta
while cap.isOpened():

    # Leemos el siguiente frame (imagen) de la cámara
    ret, frame2 = cap.read()
    
    # Si no podemos leer el frame (por ejemplo, se desconectó la cámara), salimos del bucle
    if not ret:
        break  

    # Convertimos este nuevo frame a escala de grises también
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    # Lo desenfocamos igual que al primer frame, para que la comparación sea consistente
    gray2 = cv2.GaussianBlur(gray2, (21, 21), 0)

    # Restamos el frame actual al frame anterior para detectar diferencias (movimiento)
    # cv2.absdiff calcula la diferencia absoluta pixel por pixel
    delta_frame = cv2.absdiff(gray1, gray2)

    # Aplicamos un umbral: los píxeles cuya diferencia sea mayor que 25 se vuelven blancos (255)
    # Los demás se vuelven negros (0). Esto crea una imagen binaria (blanco/negro)
    thresh = cv2.threshold(delta_frame, 25, 255, cv2.THRESH_BINARY)[1]

    # Dilatamos la imagen binaria para rellenar pequeños agujeros en las zonas blancas
    # Esto hace que las áreas de movimiento sean más sólidas y fáciles de detectar
    thresh = cv2.dilate(thresh, None, iterations=2)

    # Buscamos contornos (bordes) en las zonas blancas (zonas de movimiento detectadas)
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Recorremos cada contorno detectado
    for contour in contours:

        # Si el área del contorno es menor a 500 píxeles, lo ignoramos
        # Esto evita que pequeños movimientos (como cambios de luz o insectos) activen el detector
        if cv2.contourArea(contour) < 500:
            continue  

        # Obtenemos las coordenadas (x, y) y dimensiones (ancho w y alto h) del rectángulo que encierra el movimiento
        (x, y, w, h) = cv2.boundingRect(contour)

        # Dibujamos un rectángulo verde alrededor de la zona que detectamos en movimiento
        # frame2 es la imagen original donde marcamos el resultado
        cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Mostramos la imagen con los rectángulos verdes en una ventana llamada 'Detección de Movimiento'
    cv2.imshow('Detección de Movimiento', frame2)

    # Esperamos 30 ms y verificamos si el usuario presionó la tecla 'q' para salir
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

    # Actualizamos el frame anterior (gray1) con el frame actual (gray2)
    # Así, en la próxima iteración, siempre comparamos el nuevo frame con el último visto
    gray1 = gray2

# Liberamos la cámara para que otros programas puedan usarla
cap.release()

# Cerramos todas las ventanas abiertas por OpenCV
cv2.destroyAllWindows()
