FROM python:3.10-slim

# install dependencies
RUN apt-get update && apt-get install -y \
    libsndfile1 curl \
    && rm -rf /var/lib/apt/lists/*

# install python libs
RUN pip install piper-tts fastapi uvicorn python-multipart

WORKDIR /app

# download Priyamvada (female)
RUN curl -L -o priyamvada.onnx https://huggingface.co/rhasspy/piper-voices/resolve/main/hi/hi_IN/priyamvada/medium/hi_IN-priyamvada-medium.onnx

# download Pratham (male)
RUN curl -L -o pratham.onnx https://huggingface.co/rhasspy/piper-voices/resolve/main/hi/hi_IN/pratham/medium/hi_IN-pratham-medium.onnx

# copy server code
COPY server.py server.py

EXPOSE 10000

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "10000"]