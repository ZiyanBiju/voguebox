from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from flask_uploads import UploadSet, configure_uploads, IMAGES
import os
import random  # For mock AI outfit suggestions (replace with AI model later)

app = Flask(__name__)

# Configuration
app.config['UPLOADED_CLOTHES_DEST'] = 'static/uploads'  # Directory for uploaded images
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max file size 16 MB

# UploadSet for clothing images
clothes = UploadSet('clothes', IMAGES)
configure_uploads(app, clothes)

# Ensure the upload directory exists
if not os.path.exists(app.config['UPLOADED_CLOTHES_DEST']):
    os.makedirs(app.config['UPLOADED_CLOTHES_DEST'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files.get('file')
        user_id = request.form.get('user_id', 'default_user')  # Example user ID

        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOADED_CLOTHES_DEST'], filename)
            file.save(file_path)
            return redirect(url_for('upload') + '?message=Upload%20successful&type=success')
        else:
            return redirect(url_for('upload') + '?message=Please%20select%20a%20valid%20file&type=error')

    return render_template('upload.html')

@app.route('/wardrobe/<user_id>')
def wardrobe(user_id):
    clothes_items = [
        'uploads/clothing1.jpg',
        'uploads/clothing2.jpg',
        # You could dynamically load wardrobe items from the database here.
    ]
    return render_template('wardrobe.html', clothes=clothes_items)

@app.route('/suggest_outfit/<user_id>', methods=['GET'])
def suggest_outfit(user_id):
    # For now, returning random items as suggestions. Replace with AI model logic.
    clothing_items = ['clothing1.jpg', 'clothing2.jpg', 'clothing3.jpg']  # Example items
    suggested_outfit = random.sample(clothing_items, 2)  # Randomly suggest two items
    outfit_paths = [os.path.join('static', 'uploads', item) for item in suggested_outfit]
    return jsonify({
        'outfit': outfit_paths,
        'message': 'AI-generated outfit suggestions'
    })

if __name__ == '__main__':
    app.run(debug=True)
