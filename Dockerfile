FROM node:24-slim AS frontend-builder

WORKDIR /frontend
COPY frontend-react/package*.json ./
RUN npm install
COPY frontend-react/ ./
RUN npm run build

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip && \
    python -m pip install --no-cache-dir \
    torch --index-url https://download.pytorch.org/whl/cpu && \
    python -m pip install --no-cache-dir \
    -r requirements.txt && \
    python -m pip install --no-cache-dir \
    aiofiles

COPY . .

COPY --from=frontend-builder /frontend/dist ./frontend-react/dist

RUN mkdir -p data/uploads data/chroma_db

EXPOSE 8000

CMD ["python", "run.py"]