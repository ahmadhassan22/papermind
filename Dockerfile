FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip && \
    python -m pip install --timeout 180 --retries 10 --no-cache-dir \
    torch --index-url https://download.pytorch.org/whl/cpu && \
    python -m pip install --timeout 180 --retries 10 --no-cache-dir \
    -i https://pypi.tuna.tsinghua.edu.cn/simple \
    -r requirements.txt

COPY . .

RUN mkdir -p data/uploads data/chroma_db

EXPOSE 8000

CMD ["python", "run.py"]