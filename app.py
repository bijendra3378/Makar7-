import os
import io
from flask import Flask, request, render_template, send_file
from PIL import Image

app = Flask(__name__)

# इमेज अपलोड करने का साइज लिमिट (Optional: 16MB तक)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # 1. चेक करना कि यूजर ने फाइल सेलेक्ट की है या नहीं
        if 'image' not in request.files:
            return "कोई फाइल नहीं मिली!", 400
        
        file = request.files['image']
        
        if file.filename == '':
            return "कृपया एक इमेज सेलेक्ट करें!", 400

        if file:
            # ⭐ जादू यहाँ है: rembg को यहाँ अंदर इम्पोर्ट किया है
            # इससे Render ऐप को बिना किसी देरी के तुरंत 'Live' कर देगा!
            from rembg import remove
            
            # 2. अपलोड की गई इमेज को रीड करना
            input_image = file.read()
            
            # 3. rembg से बैकग्राउंड हटाना
            output_image = remove(input_image)
            
            # 4. बिना सर्वर पर सेव किए, सीधे यूजर को PNG फाइल डाउनलोड करवा देना
            return send_file(
                io.BytesIO(output_image),
                mimetype='image/png',
                as_attachment=True,
                download_name='bg_removed.png'
            )

    # GET Request: जब यूजर पहली बार वेबसाइट खोलेगा तो यह सिंपल फॉर्म दिखेगा
    return '''
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <title>AI Background Remover</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; background-color: #f4f4f9; }
            .container { background: white; padding: 30px; border-radius: 10px; display: inline-block; box-shadow: 0px 0px 10px #ccc; }
            input[type=file] { margin: 20px 0; }
            input[type=submit] { background: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; }
            input[type=submit]:hover { background: #0056b3; }
        </style>
      </head>
      <body>
        <div class="container">
            <h2>AI Background Remover 🤖</h2>
            <p>अपनी फोटो अपलोड करें और तुरंत बैकग्राउंड हटाएं</p>
            <form method="post" enctype="multipart/form-data">
              <input type="file" name="image" accept="image/*" required><br>
              <input type="submit" value="Remove Background & Download">
            </form>
        </div>
      </body>
    </html>
    '''

if __name__ == '__main__':
    # Render ऑटोमैटिकली PORT एनवायरनमेंट वेरिएबल देता है
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)