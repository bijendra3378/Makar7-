import os
import io
from flask import Flask, request, render_template, send_file

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 1. आपके HTML फॉर्म से फोटो को पकड़ना
        # (यह 'file' या 'image' दोनों में से जो भी नाम होगा, उसे ढूंढ लेगा)
        uploaded_file = request.files.get('file') or request.files.get('image')
        
        if not uploaded_file or uploaded_file.filename == '':
            return "गलती: कृपया एक सही इमेज सेलेक्ट करें!", 400

        try:
            # ⭐ Lazy Loading: rembg को यहाँ अंदर इम्पोर्ट किया है 
            # इससे Render बिना किसी टाइमआउट एरर के तुरंत 5 सेकंड में Live हो जाएगा!
            from rembg import remove
            
            # 2. इमेज रीड करना और बैकग्राउंड हटाना
            input_image = uploaded_file.read()
            output_image = remove(input_image)
            
            # 3. सीधे रिमूव की हुई PNG फाइल यूजर को डाउनलोड करवा देना
            return send_file(
                io.BytesIO(output_image),
                mimetype='image/png',
                as_attachment=True,
                download_name='bg_removed.png'
            )
        except Exception as e:
            return f"इमेज प्रोसेस करने में एरर आया: {str(e)}", 500

    # GET Request: जब वेबसाइट खुलेगी तो आपका index.html लोड होगा
    return render_template('index.html')

if __name__ == '__main__':
    # Render ऑटोमैटिकली PORT देता है, उसे सेट करना जरूरी है
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)