FROM python:3.10-slim

# 1. Install necessary system dependencies
RUN apt-get update && apt-get install -y \
    libsndfile1 curl tar \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2. Download Correct Piper Binary for Render (AMD64 / x86_64)
# Hum .tar.gz use kar rahe hain kyunki ye Linux ke liye standard hai
RUN curl -L -o piper.tar.gz https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_linux_x86_64.tar.gz \
    && tar -xzf piper.tar.gz \
    && mv piper /usr/local/share/piper \
    && ln -s /usr/local/share/piper/piper /usr/local/bin/piper \
    && rm piper.tar.gz

# 3. Install Python Dependencies
RUN pip install fastapi uvicorn python-multipart

# 4. Download Voice Models AND JSON Configs (Important!)
# Priyamvada
RUN curl -L -o priyamvada.onnx https://huggingface.co/rhasspy/piper-voices/resolve/main/hi/hi_IN/priyamvada/medium/hi_IN-priyamvada-medium.onnx
RUN curl -L -o priyamvada.onnx.json https://huggingface.co/rhasspy/piper-voices/resolve/main/hi/hi_IN/priyamvada/medium/hi_IN-priyamvada-medium.onnx.json

# Pratham
RUN curl -L -o pratham.onnx https://huggingface.co/rhasspy/piper-voices/resolve/main/hi/hi_IN/pratham/medium/hi_IN-pratham-medium.onnx
RUN curl -L -o pratham.onnx.json https://huggingface.co/rhasspy/piper-voices/resolve/main/hi/hi_IN/pratham/medium/hi_IN-pratham-medium.onnx.json

COPY server.py server.py

EXPOSE 10000

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "10000"]
