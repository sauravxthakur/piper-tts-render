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
    voice = payload.get("voice", "priyamvada")  # default = female

    # fallback
    if voice not in VOICE_MODELS:
        voice = "priyamvada"

    model_path = VOICE_MODELS[voice]

    if not text.strip():
        return {"error": "Text missing"}

    # temp wav file
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    tmp.close()

    # run Piper
    cmd = [
        "piper",
        "--model", model_path,
        "--output_file", tmp.name,
        "--text", text
    ]
    subprocess.run(cmd)

    # read output
    with open(tmp.name, "rb") as f:
        audio_data = f.read()

    os.remove(tmp.name)

    return Response(content=audio_data, media_type="audio/wav")