import base64
import io
from flask import Flask, request, jsonify, render_template
from PIL import Image
from rembg import remove, new_session

app = Flask(__name__, template_folder="templates")

# मॉडल सेशन को शुरुआत में None रखेंगे ताकि स्टार्टअप पर लोड न पड़े
model_session = None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/remove-bg", methods=["POST"])
def remove_bg():
    global model_session
    try:
        data = request.get_json()
        if not data or "image" not in data:
            return jsonify({"success": False, "message": "No image data provided"}), 400

        image_data = data["image"]
        target_color = data.get("color", "original")

        if "," in image_data:
            header, image_data = image_data.split(",", 1)

        img_bytes = base64.b64decode(image_data)
        input_image = Image.open(io.BytesIO(img_bytes))

        # जब पहली बार कोई बैकग्राउंड चेंज करने की रिक्वेस्ट भेजेगा, मॉडल तब डाउनलोड होगा
        # इससे ऐप स्टार्टअप के समय कभी क्रैश नहीं होगा
        if model_session is None:
            model_session = new_session("u2netp")

        output_image = remove(input_image, session=model_session)

        if target_color in ["white", "blue"]:
            if target_color == "white":
                bg_color = (255, 255, 255, 255)
            else:
                bg_color = (0, 112, 192, 255)

            solid_bg = Image.new("RGBA", output_image.size, bg_color)
            final_image = Image.alpha_composite(solid_bg, output_image.convert("RGBA"))
        else:
            final_image = output_image

        buffered = io.BytesIO()
        final_image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

        return jsonify({
            "success": True,
            "image": f"data:image/png;base64,{img_str}"
        })

    except Exception as e:
        print("Error during processing:", str(e))
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)