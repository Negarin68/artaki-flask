
from flask import Flask, request, jsonify
import cv2
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return "<h2>ArtakiApp API is running.</h2>"

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({"error": "No video uploaded"}), 400

    video = request.files['video']
    filename = secure_filename(video.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    video.save(filepath)

    result = analyze_fight(filepath)
    return jsonify(result)

def analyze_fight(filepath):
    cap = cv2.VideoCapture(filepath)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    punches = 10  # فرضی
    kicks = 6     # فرضی
    winner = "Red Fighter" if punches > kicks else "Blue Fighter"

    cap.release()
    return {
        "total_frames": total_frames,
        "punches": punches,
        "kicks": kicks,
        "winner": winner
    }

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
