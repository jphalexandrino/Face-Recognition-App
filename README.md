# Facial Recognition using DeepFace

This project uses the DeepFace library along with OpenCV to perform real-time facial recognition using a webcam. It captures video frames from the webcam, detects faces using Haar cascades, and matches them against known images stored locally.

## Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/sondercs/Facial-Recognition.git
   cd Facial-Recognition
   ```

2. **Install dependencies:**

   Make sure you have Python 3.12.1 installed. Use pip to install required libraries:

   ```bash
   pip install deepface opencv-python
   ```

3. **Download the Haar Cascade file:**

   The facial detection uses the Haar Cascade classifier from OpenCV. You can download it from the official OpenCV GitHub repository or use the default one provided with OpenCV.

   ```python
   # Example using OpenCV's provided Haar Cascade
   face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
   ```

## Usage

1. **Prepare known images:**

   Add images of individuals you want to recognize in the `users-pictures` folder. Name each image with the person's name (e.g., `Joao.jpg`, `Maria.jpg`).

2. **Run the application:**

   Execute the main Python script to start the facial recognition:

   ```bash
   python main.py
   ```

3. **Interact with the application:**

   - Position yourself in front of the webcam.
   - Press 'q' to exit the application.
   - The application will attempt to recognize each face captured by the webcam against the known images.
   - If a match is found, it will print "Welcome [person's name]!".

## Notes

- Ensure proper lighting conditions and avoid obstructing the face for better recognition accuracy.
- Adjust the `check_interval` variable in `main.py` to control how often the application performs recognition checks.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
```

Replace `sondercs` with your GitHub username and ensure the project structure and file names match those in your actual repository (`main.py`, `users-pictures` folder, etc.). This README provides basic setup instructions, usage guidelines, and customization tips for your facial recognition project using DeepFace and OpenCV. Adjust and expand it as needed based on additional features or specific requirements of your project.