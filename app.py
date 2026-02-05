from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv
import base64

load_dotenv()  # Load environment variables from .env

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")  # Securely load API key

@app.route("/", methods=["GET", "POST"])
def index():
    image_data = None
    error = None

    if request.method == "POST":
        prompt = request.form["prompt"]

        try:
            client = openai.OpenAI()

            img = client.images.generate(
                model="gpt-image-1-mini",
                prompt=prompt,
                size="1024x1024"
            )

            image_base64 = img.data[0].b64_json # encoded png img as string

            # en/decode for html display
            image_data = base64.b64encode(
                base64.b64decode(image_base64)
            ).decode("utf-8")

        except Exception as e:
            error = str(e)

    return render_template(
        "index.html",
        image_data=image_data,
        error=error
    )

if __name__ == "__main__":
    app.run(debug=True)  # Run locally for testing