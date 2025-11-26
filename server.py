from fastapi import FastAPI, Body
from fastapi.responses import Response
import subprocess
import tempfile
import os

app = FastAPI()

VOICE_MODELS = {
    "priyamvada": "priyamvada.onnx",
    "pratham": "pratham.onnx"
}

@app.post("/api/tts")
async def tts_api(payload: dict = Body(...)):
    text = payload.get("text", "")
    voice = payload.get("voice", "priyamvada")

    if voice not in VOICE_MODELS:
        voice = "priyamvada"

    model_path = VOICE_MODELS[voice]

    if not text.strip():
        return {"error": "Text missing"}

    # Temp file banayein
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    tmp.close()

    # Command setup
    cmd = [
        "piper",
        "--model", model_path,
        "--output_file", tmp.name
    ]

    try:
        # Text ko 'input' ke zariye bhejein aur errors capture karein
        result = subprocess.run(cmd, input=text, text=True, capture_output=True)

        # Agar command fail hui (Exit code 0 nahi hai)
        if result.returncode != 0:
            error_message = result.stderr.strip()
            print(f"❌ Piper Error: {error_message}") # Ye Render Logs mein dikhega
            raise Exception(f"Piper failed: {error_message}")

        # Agar file 0 bytes ki bani
        if os.path.getsize(tmp.name) == 0:
            raise Exception("Piper generated an empty file (0 bytes).")

    except Exception as e:
        if os.path.exists(tmp.name):
            os.remove(tmp.name)
        # Error client ko wapis bhejein taaki pata chale kya galat hua
        return Response(content=str(e), status_code=500)

    # Audio data read karein
    with open(tmp.name, "rb") as f:
        audio_data = f.read()

    os.remove(tmp.name)

    return Response(content=audio_data, media_type="audio/wav")
