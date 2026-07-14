from flask import Flask, request, send_file, render_template
from rembg import remove
import io

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    file = request.files.get('image')
    if not file: return "No image", 400
    input_data = file.read()
    output_data = remove(input_data)
    return send_file(io.BytesIO(output_data), mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)