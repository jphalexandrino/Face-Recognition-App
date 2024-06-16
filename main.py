import cv2
from deepface import DeepFace
import os
import tempfile
import time

# Definir a pasta que contém as imagens conhecidas
known_images_folder = "users-pictures"

# Verificar se a pasta existe
if not os.path.exists(known_images_folder):
    print(f"Pasta não encontrada: {known_images_folder}")
    exit()

# Inicializar a webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erro ao acessar a webcam.")
    exit()

print("Posicione-se na frente da webcam. Pressione 'q' para sair.")

# Carregar um classificador Haar para detecção de rosto
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

last_checked = time.time()
check_interval = 2  # Intervalo de tempo em segundos entre as verificações de reconhecimento

while True:
    # Capturar frame da webcam
    ret, frame = cap.read()
    if not ret:
        print("Erro ao capturar a imagem.")
        break

    # Mostrar o frame capturado
    cv2.imshow('Webcam', frame)

    # Detecção de rosto
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Verificar se há algum rosto detectado
    if len(faces) > 0 and (time.time() - last_checked) >= check_interval:
        last_checked = time.time()
        
        # Salvar o frame capturado como um arquivo temporário
        temp_frame_path = None
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
            temp_frame_path = temp_file.name
            cv2.imwrite(temp_frame_path, frame)

        # Iterar sobre as imagens conhecidas
        matched = False
        for filename in os.listdir(known_images_folder):
            known_image_path = os.path.join(known_images_folder, filename)
            person_name = os.path.basename(known_image_path).split('.')[0]

            try:
                result = DeepFace.verify(temp_frame_path, known_image_path, enforce_detection=False)
                if result["verified"]:
                    print(f"Bem-vindo {person_name}!")
                    matched = True
                    break
            except Exception as e:
                print(f"Erro no reconhecimento facial com {person_name}: {e}")

        if not matched:
            print("Pessoa não reconhecida.")

        # Remover o arquivo temporário
        if temp_frame_path and os.path.exists(temp_frame_path):
            os.remove(temp_frame_path)

    # Sair do loop se a tecla 'q' for pressionada
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar a webcam e fechar todas as janelas
cap.release()
cv2.destroyAllWindows()
