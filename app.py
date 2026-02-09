from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv
import base64

load_dotenv()

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    image_data = None
    interpretation = None
    error = None

    if request.method == "POST":
        prompt = request.form["prompt"]

        try:
            client = openai.OpenAI()

            ##### TEXT #####
            response = client.responses.create(
                model="gpt-4.1-nano",
                temperature=1.2,
                top_p=1.0,
                max_output_tokens=100,
                input=[
                    {
                        "role": "developer",
                        "content": "You are an assistant trained in Carl Jung’s analytical psychology. You interpret dreams symbolically, not literally, using Jungian concepts. Your interpretations are reflective and exploratory, not diagnostic or therapeutic. You focus on symbols, emotional tone, figures, and settings, and describe possible meanings as psychological patterns or unconscious themes."
                    },
                    {
                        "role": "user",
                        "content": f"""
                            Analyze the following dream using Jungian analytical psychology.

                            Dream: {prompt}

                            Please include:
                            1. Key symbols and figures
                            2. Possible Jungian archetypes involved
                            3. Emotional tone of the dream
                            4. A reflective interpretation of what the unconscious may be expressing
                        """
                    }
                ]
            )

            interpretation = response.output[0].content[0].text

            ##### IMAGE #####
            img = client.images.generate(
                model="gpt-image-1",
                # prompt="A surreal, symbolic illustration inspired by a Jungian dream interpretation. The image should feel dreamlike and psychological rather than realistic. Use archetypal symbolism, soft lighting, and abstract forms. Emphasize unconscious themes, emotional tension, and transformation. Dream content: {prompt}",
                prompt=interpretation,
                size="1024x1024"
            )

            image_base64 = img.data[0].b64_json

            image_data = base64.b64encode(
                base64.b64decode(image_base64)
            ).decode("utf-8")

        except Exception as e:
            error = str(e)

    return render_template(
        "index.html",
        image_data=image_data,
        text_interpretation=interpretation,
        error=error
    )

if __name__ == "__main__":
    app.run(debug=True)