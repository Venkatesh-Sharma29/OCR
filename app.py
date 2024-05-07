# app.py
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import pytesseract
from PIL import Image
pytesseract.pytesseract.tesseract_cmd = r'E:\ALl programs\Tesseract\tesseract.exe'


app = Flask(__name__)

# Configure upload folder and allowed extensions

app.config['UPLOAD_FOLDER'] = 'E:/ALl programs/OCRFILES'  # Corrected path format
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'pdf'}

# Function to check if a file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Route for file upload
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        
        file = request.files['file']

        if file.filename == '':
            return 'No selected file'

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = app.config['UPLOAD_FOLDER'] + '/' + filename
            file.save(filepath)

            # Perform OCR
            extracted_text = ocr(filepath)

            # Save extracted text to a text file
            output_text_file = 'output.txt'
            with open(output_text_file, 'w') as f:
                f.write(extracted_text)

            return send_file(output_text_file, as_attachment=True)

    return render_template('upload.html')

# Function to perform OCR
def ocr(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text

if __name__ == '__main__':
    app.run(debug=True)
