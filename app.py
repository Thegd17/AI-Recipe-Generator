# app.py
import os
import io
import traceback
from dotenv import load_dotenv

from flask import Flask, request, jsonify, render_template
from PIL import Image, UnidentifiedImageError

import google.genai as genai
from google.genai import types

# --- Load env ---
load_dotenv()  # make sure .env lines are plain KEY=VALUE (no `export`)

# --- Config ---
PORT = int(os.getenv("PORT", 10000))  # Changed to 10000 for Render
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")
MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", 8))
MAX_CONTENT_LENGTH = MAX_UPLOAD_MB * 1024 * 1024

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

# --- Init Gemini client (try explicit api_key first) ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = None
if GEMINI_API_KEY:
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        print("Gemini Client Initialized Successfully (using api_key).")
    except Exception as e:
        print("Error initializing Gemini client with api_key:", e)
        client = None
else:
    # fallback: try default constructor (e.g., if using Google Cloud/Vertex auth)
    try:
        client = genai.Client()
        print("Gemini Client Initialized Successfully (no explicit api_key).")
    except Exception as e:
        print("Error initializing Gemini client (no api_key):", e)
        client = None

# --- Helpers ---
ALLOWED_FORMATS = {"JPEG", "PNG", "GIF", "BMP", "WEBP"}


def pillow_detect_format(image_bytes: bytes):
    try:
        with Image.open(io.BytesIO(image_bytes)) as img:
            return img.format  # e.g. 'JPEG', 'PNG', ...
    except UnidentifiedImageError:
        return None
    except Exception:
        return None


def convert_to_jpeg_bytes(image_bytes: bytes) -> bytes:
    with Image.open(io.BytesIO(image_bytes)) as img:
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        out = io.BytesIO()
        img.save(out, format="JPEG", quality=90)
        return out.getvalue()


def pillow_format_to_mime(fmt: str) -> str:
    if not fmt:
        return "application/octet-stream"
    f = fmt.upper()
    if f == "JPEG":
        return "image/jpeg"
    if f == "PNG":
        return "image/png"
    if f == "GIF":
        return "image/gif"
    if f == "BMP":
        return "image/bmp"
    if f == "WEBP":
        return "image/webp"
    return "application/octet-stream"


# --- JSON-only error handlers (avoid HTML) ---
@app.errorhandler(413)
def handle_too_large(e):
    return jsonify({"error": "Uploaded file too large", "max_bytes": app.config["MAX_CONTENT_LENGTH"]}), 413


@app.errorhandler(404)
def handle_404(e):
    return jsonify({"error": "Not found", "path": request.path}), 404


@app.errorhandler(Exception)
def handle_all(e):
    print("Unhandled exception:", type(e).__name__, e)
    traceback.print_exc()
    return jsonify({"error": "Internal server error", "type": type(e).__name__}), 500


# --- Routes ---
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate-recipe", methods=["POST"])
def generate_recipe():
    # Fail-fast if client missing
    if client is None:
        return jsonify({"error": "Gemini client not initialized. Set GEMINI_API_KEY or configure Vertex credentials."}), 500

    if "image" not in request.files:
        return jsonify({"error": "No image file provided."}), 400

    image_file = request.files["image"]
    preferences = request.form.get("preferences", "").strip() or "None"

    if image_file.filename == "":
        return jsonify({"error": "Uploaded file has no filename."}), 400

    try:
        # Read raw bytes from upload
        image_file.stream.seek(0)
        image_bytes = image_file.read()
        if not image_bytes:
            return jsonify({"error": "Uploaded file is empty."}), 400

        # Validate image via Pillow
        detected_fmt = pillow_detect_format(image_bytes)
        if not detected_fmt or detected_fmt.upper() not in ALLOWED_FORMATS:
            return jsonify({"error": "Unsupported or invalid image type", "detected_format": detected_fmt}), 400

        # Normalize to JPEG if not JPEG (optional but avoids MIME mismatch)
        if detected_fmt.upper() != "JPEG":
            image_bytes = convert_to_jpeg_bytes(image_bytes)
            mime_type = "image/jpeg"
        else:
            mime_type = pillow_format_to_mime(detected_fmt)

        # Build prompt
        full_prompt = (
            "You are a professional recipe developer. "
            "1. **Identify** all ingredients visible in the photo. "
            "2. **Generate** a detailed, unique recipe using *only* those ingredients. "
            f"3. **Adhere strictly** to the user's notes and dietary needs: '{preferences}'. "
            "4. **Format** the entire response using clear **Markdown**, including: "
            "   - A catchy **Recipe Title** (Level 2 Heading: ##) "
            "   - **Prep Time** and **Cook Time** "
            "   - A bulleted **Ingredients List** with specific amounts. "
            "   - Numbered **Step-by-Step Instructions**. "
            "5. Do not include any introductory or conversational text outside of the recipe structure."
        )

        # --- IMPORTANT: use from_bytes (not from_image) ---
        image_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)

        contents = [
            image_part,
            full_prompt
        ]

        # Call Gemini
        response = client.models.generate_content(model=MODEL_NAME, contents=contents)

        # Extract text (SDKs vary; prefer .text if available)
        recipe_text = getattr(response, "text", None)
        if not recipe_text:
            # fallback to a string of the response to avoid crashing
            recipe_text = str(response)

        return jsonify({"recipe": recipe_text})

    except Exception as e:
        # Log full traceback server-side and return JSON error
        print("--- FAILED TO GENERATE RECIPE ---")
        print("EXCEPTION TYPE:", type(e).__name__)
        print("ERROR MESSAGE:", e)
        traceback.print_exc()
        return jsonify({"error": f"Failed to generate recipe: {type(e).__name__}"}), 500


# --- Run ---
if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=PORT, debug=debug_mode)  # Changed to 0.0.0.0 for Render
