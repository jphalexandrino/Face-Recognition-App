import cv2
import requests
import json
import os
from dotenv import load_dotenv
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

# Carrega as variáveis do .env
load_dotenv()

# Chaves da API
Api_Key = os.getenv('API_KEY')
Api_Secret = os.getenv('API_SECRET')
Detect_Url = os.getenv('DETECT_URL')
Compare_Url = os.getenv('COMPARE_URL')

# Definir a pasta que contém as imagens conhecidas
known_images_folder = "users-pictures"

# Crie a pasta se ela não existir
if not os.path.exists(known_images_folder):
    os.makedirs(known_images_folder)

# Carregar as imagens conhecidas e seus nomes
known_faces = []
known_names = []

for filename in os.listdir(known_images_folder):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        image_path = os.path.join(known_images_folder, filename)
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()
            response = requests.post(Detect_Url, data={
                'api_key': Api_Key,
                'api_secret': Api_Secret,
            }, files={
                'image_file': image_data
            })
            faces = response.json().get('faces', [])
            if faces:
                face_token = faces[0]['face_token']
                known_faces.append(face_token)
                known_names.append(os.path.splitext(filename)[0])

# Inicializar a webcam
video_capture = cv2.VideoCapture(0)

if not video_capture.isOpened():
    print("Erro ao acessar a webcam.")
    exit()

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file.save(os.path.join(known_images_folder, file.filename))
    return 'File uploaded successfully!'

@app.route('/recognize', methods=['POST'])
def recognize():
    ret, frame = video_capture.read()
    if not ret:
        return jsonify({"error": "Erro ao capturar a imagem."}), 500

    # Redimensionar o frame para processamento mais rápido
    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

    # Salvar o frame capturado como um arquivo temporário
    temp_frame_path = 'temp_frame.jpg'
    cv2.imwrite(temp_frame_path, small_frame)

    with open(temp_frame_path, 'rb') as image_file:
        image_data = image_file.read()
        response = requests.post(Detect_Url, data={
            'api_key': Api_Key,
            'api_secret': Api_Secret,
        }, files={
            'image_file': image_data
        })
        faces = response.json().get('faces', [])
        if faces:
            face_token = faces[0]['face_token']

            for known_face, name in zip(known_faces, known_names):
                response = requests.post(Compare_Url, data={
                    'api_key': Api_Key,
                    'api_secret': Api_Secret,
                    'face_token1': face_token,
                    'face_token2': known_face,
                })
                result = response.json()
                if result.get('confidence', 0) > 80:  # Ajuste o limiar conforme necessário
                    return jsonify({"name": name})

        return jsonify({"error": "Nenhum rosto detectado ou sem correspondência."}), 404

    if os.path.exists(temp_frame_path):
        os.remove(temp_frame_path)

if __name__ == '__main__':
    app.run(port=5001)
