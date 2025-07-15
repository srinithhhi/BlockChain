from flask import Flask, render_template, request, send_file, redirect, url_for
import os
from werkzeug.utils import secure_filename
from encrypt_file import encrypt_file
from decrypt_file import decrypt_file
from generate_rsa_keys import generate_rsa_keys
import base64

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint to generate RSA keys
@app.route('/generate_keys', methods=['POST'])
def generate_keys():
    generate_rsa_keys()
    return "Keys generated successfully!"

@app.route('/encrypt', methods=['POST'])
def encrypt():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        output_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'encrypted_' + filename)

        # Encrypt the file and get the encrypted AES key and IV
        encrypted_key, iv = encrypt_file(filepath, output_filepath)

        # Convert the encrypted key and IV to base64 strings for displaying
        encrypted_key_str = base64.b64encode(encrypted_key).decode('utf-8')
        iv_str = base64.b64encode(iv).decode('utf-8')

        # Render the result in the encrypted.html page
        return render_template('encrypted.html', filename='encrypted_' + filename, encrypted_key=encrypted_key_str, iv=iv_str)

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # Check if the file exists
    if not os.path.exists(file_path):
        return "File not found", 404

    return send_file(file_path, as_attachment=True)

@app.route('/decrypt', methods=['POST'])
def decrypt():
    if 'file' not in request.files or 'encrypted_key' not in request.form or 'iv' not in request.form:
        return redirect(request.url)

    file = request.files['file']
    encrypted_key = request.form['encrypted_key']
    iv = request.form['iv']

    if file.filename == '':
        return redirect(request.url)

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        output_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'decrypted_' + filename)

        # Decode the base64-encoded encrypted key and IV
        encrypted_key_bytes = base64.b64decode(encrypted_key)
        iv_bytes = base64.b64decode(iv)

        # Pass the encrypted AES key and IV along with the file to decrypt
        decrypt_file(filepath, output_filepath, encrypted_key_bytes, iv_bytes)

        return send_file(output_filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
