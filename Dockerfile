FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    libsndfile1 curl tar \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Download Piper ARM64 binary from fast CDN (Render Free Tier compatible)
RUN curl -L -o piper.tar.gz https://huggingface.co/datasets/mtk7/piper-binaries/resolve/main/piper_linux_aarch64.tar.gz \
    && tar -xzf piper.tar.gz \
    && mv piper_linux_aarch64/piper /usr/local/bin/piper \
    && chmod +x /usr/local/bin/piper \
    && rm -rf piper.tar.gz piper_linux_aarch64

RUN pip install fastapi uvicorn python-multipart

# Download voices
RUN curl -L -o priyamvada.onnx https://huggingface.co/rhasspy/piper-voices/resolve/main/hi/hi_IN/priyamvada/medium/hi_IN-priyamvada-medium.onnx
RUN curl -L -o pratham.onnx https://huggingface.co/rhasspy/piper-voices/resolve/main/hi/hi_IN/pratham/medium/hi_IN-pratham-medium.onnx

COPY server.py server.py

EXPOSE 10000

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "10000"]
