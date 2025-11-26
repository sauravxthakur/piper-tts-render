FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    libsndfile1 curl unzip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Download Piper ARM64 from custom lightweight mirror (Render-safe)
RUN curl -L -o piper.zip https://raw.githubusercontent.com/heyitsarmaan/piper-mirror/main/piper_arm64.zip \
    && unzip piper.zip -d piper_bin \
    && mv piper_bin/piper /usr/local/bin/piper \
    && chmod +x /usr/local/bin/piper \
    && rm -rf piper.zip piper_bin

RUN pip install fastapi uvicorn python-multipart

# Download voices
RUN curl -L -o priyamvada.onnx https://huggingface.co/rhasspy/piper-voices/resolve/main/hi/hi_IN/priyamvada/medium/hi_IN-priyamvada-medium.onnx
RUN curl -L -o pratham.onnx https://huggingface.co/rhasspy/piper-voices/resolve/main/hi/hi_IN/pratham/medium/hi_IN-pratham-medium.onnx

COPY server.py server.py

EXPOSE 10000

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "10000"]
