from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from urllib.parse import unquote
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "/data"
MAX_STORAGE = 10 * 1024 * 1024  # 10 MB

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ── Utility: Calculate used storage ──
def get_folder_size():
    total = 0
    for f in os.listdir(UPLOAD_FOLDER):
        path = os.path.join(UPLOAD_FOLDER, f)
        if os.path.isfile(path):
            total += os.path.getsize(path)
    return total


# ── Utility: Safe path (prevent ../ attacks) ──
def safe_path(filename):
    filename = secure_filename(unquote(filename))
    return os.path.join(UPLOAD_FOLDER, filename)


# ── Health Check ──
@app.route('/health')
def health():
    return jsonify({"status": "healthy"})


# ── Upload ──
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    filename = secure_filename(file.filename)
    save_path = os.path.join(UPLOAD_FOLDER, filename)

    # Read size
    file_bytes = file.read()
    file_size = len(file_bytes)
    file.seek(0)

    # Storage quota check
    if get_folder_size() + file_size > MAX_STORAGE:
        return jsonify({"error": "Storage limit exceeded"}), 400

    # If file exists → rename (file_1.txt)
    if os.path.exists(save_path):
        name, ext = os.path.splitext(filename)
        counter = 1
        while True:
            new_name = f"{name}_{counter}{ext}"
            new_path = os.path.join(UPLOAD_FOLDER, new_name)
            if not os.path.exists(new_path):
                filename = new_name
                save_path = new_path
                break
            counter += 1

    file.save(save_path)

    return jsonify({
        "message": "uploaded",
        "filename": filename
    }), 200


# ── List Files + Storage Stats ──
@app.route('/files', methods=['GET'])
def list_files():
    files = []
    total_size = 0

    for f in os.listdir(UPLOAD_FOLDER):
        path = os.path.join(UPLOAD_FOLDER, f)
        if os.path.isfile(path):
            files.append(f)
            total_size += os.path.getsize(path)

    files.sort()

    return jsonify({
        "files": files,
        "used": total_size,
        "limit": MAX_STORAGE
    })


# ── Download ──
@app.route('/download/<path:filename>')
def download_file(filename):
    filename = secure_filename(unquote(filename))
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)


# ── Delete ──
@app.route('/delete/<path:filename>', methods=['DELETE'])
def delete_file(filename):
    filename = secure_filename(unquote(filename))
    path = os.path.join(UPLOAD_FOLDER, filename)

    if os.path.exists(path) and os.path.isfile(path):
        os.remove(path)
        return jsonify({"message": "deleted"}), 200

    return jsonify({"error": "File not found"}), 404


# ── Root ──
@app.route('/')
def home():
    return "VAULT Backend Running"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)