from fastapi import FastAPI, Body, HTTPException
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

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    tmp.close()

    # Piper command without --text flag
    cmd = [
        "piper",
        "--model", model_path,
        "--output_file", tmp.name
    ]

    try:
        # Text ko 'input' ke through bheja ja raha hai (Pipe)
        subprocess.run(cmd, input=text, text=True, check=True)
        
        # Check karein agar file khali hai
        if os.path.getsize(tmp.name) == 0:
            raise Exception("Piper generated an empty file")

    except Exception as e:
        if os.path.exists(tmp.name):
            os.remove(tmp.name)
        print(f"Error: {e}")
        return Response(content=str(e), status_code=500)

    with open(tmp.name, "rb") as f:
        audio_data = f.read()

    os.remove(tmp.name)

    return Response(content=audio_data, media_type="audio/wav")
