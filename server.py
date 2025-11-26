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

    cmd = [
        "piper",
        "--model", model_path,
        "--output_file", tmp.name
    ]

    try:
        # CHANGE: capture_output=True add kiya taki hum error padh sakein
        result = subprocess.run(cmd, input=text, text=True, capture_output=True)
        
        # Agar Piper fail hua (return code 0 nahi hai)
        if result.returncode != 0:
            error_msg = result.stderr.strip()
            print(f"❌ Piper Error Logs: {error_msg}")  # Ye Render logs me dikhega
            raise Exception(f"Piper failed: {error_msg}")

        # Check karein agar file khali hai
        if os.path.getsize(tmp.name) == 0:
            raise Exception("Piper generated an empty file (0 bytes).")

    except Exception as e:
        if os.path.exists(tmp.name):
            os.remove(tmp.name)
        print(f"❌ System Error: {e}")
        return Response(content=str(e), status_code=500)

    with open(tmp.name, "rb") as f:
        audio_data = f.read()

    os.remove(tmp.name)

    return Response(content=audio_data, media_type="audio/wav")
