import cv2
import requests
import threading
import uuid
from dotenv import load_dotenv
import os
import time

# Carrega as variáveis do .env
load_dotenv()

# Defina suas chaves da API e URLs diretamente no código
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
DETECT_URL = 'https://api-us.faceplusplus.com/facepp/v3/detect'
COMPARE_URL = 'https://api-us.faceplusplus.com/facepp/v3/compare'

# Definir a pasta que contém as imagens conhecidas
known_images_folder = "users-pictures"

# Carregar as imagens conhecidas e seus nomes
known_faces = []
known_names = []

for filename in os.listdir(known_images_folder):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        image_path = os.path.join(known_images_folder, filename)
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()
            response = requests.post(DETECT_URL, data={
                'api_key': API_KEY,
                'api_secret': API_SECRET,
            }, files={
                'image_file': image_data
            })
            response_data = response.json()
            print(f"Response for {filename}: {response_data}")
            faces = response_data.get('faces', [])
            if faces:
                face_token = faces[0]['face_token']
                known_faces.append(face_token)
                known_names.append(os.path.splitext(filename)[0])
                print(f"Loaded face for {filename}")
            else:
                print(f"No faces found in {filename}")

# Inicializar a webcam
video_capture = cv2.VideoCapture(0)

if not video_capture.isOpened():
    print("Erro ao acessar a webcam.")
    exit()

print("Posicione-se na frente da webcam. Pressione 'q' para sair.")

def process_frame(frame):
    # Salvar o frame capturado como um arquivo temporário com um nome único
    time.sleep(2)
    temp_frame_path = f'temp_frame_{uuid.uuid4()}.jpg'
    cv2.imwrite(temp_frame_path, frame)

    with open(temp_frame_path, 'rb') as image_file:
        time.sleep(2)
        image_data = image_file.read()
        response = requests.post(DETECT_URL, data={
            'api_key': API_KEY,
            'api_secret': API_SECRET,
        }, files={
            'image_file': image_data
        })
        response_data = response.json()
        print(f"Response for webcam frame: {response_data}")
        faces = response_data.get('faces', [])
        if faces:
            face_token = faces[0]['face_token']
            print("Face detected in webcam frame")

            for known_face, name in zip(known_faces, known_names):
                response = requests.post(COMPARE_URL, data={
                    'api_key': API_KEY,
                    'api_secret': API_SECRET,
                    'face_token1': face_token,
                    'face_token2': known_face,
                })
                compare_response_data = response.json()
                print(f"Comparison response for {name}: {compare_response_data}")
                if 'confidence' in compare_response_data and compare_response_data['confidence'] > 80:  # Ajuste o limiar conforme necessário
                    print(f"Bem-vindo {name}!")
                    break
                else:
                    print(f"No match for {name}, confidence: {compare_response_data.get('confidence', 0)}")
        else:
            print("Nenhum rosto detectado.")

    # Remover o arquivo temporário
    if os.path.exists(temp_frame_path):
        os.remove(temp_frame_path)

while True:
    time.sleep(2)
    # Capturar um único frame da webcam
    ret, frame = video_capture.read()
    if not ret:
        print("Erro ao capturar a imagem.")
        break

    # Redimensionar o frame para processamento mais rápido
    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

    # Iniciar uma thread para processar o frame
    threading.Thread(target=process_frame, args=(small_frame,)).start()

    # Mostrar o frame da webcam
    cv2.imshow('Webcam', frame)

    # Sair do loop se a tecla 'q' for pressionada
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar a webcam e fechar todas as janelas
video_capture.release()
cv2.destroyAllWindows()
