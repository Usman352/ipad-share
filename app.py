import os
import time
from flask import Flask, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename

BASE_DIR = os.path.expanduser('~/Downloads')
UPLOAD_FOLDER = BASE_DIR
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'pdf', 'heic', 'txt'])

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename: str) -> bool:
    # Check . is in filename
    # Split into [filename, extension] then check extension allowed
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def index():
    folder = app.config['UPLOAD_FOLDER']
    files = sorted(
        os.listdir(folder),
        key=lambda f: os.path.getmtime(os.path.join(folder, f)),
        reverse=True,
    )
    return render_template("index.html", files=files)

@app.route('/upload', methods=['POST'])
def upload():
    if "files" not in request.files:
        return redirect(url_for('index'))

    uploaded_files = request.files.getlist("files")

    for file in uploaded_files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # add timestamp prefix so file unique
            name, ext = os.path.splitext(filename)
            filename = f"{int(time.time())}_{name}{ext}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
