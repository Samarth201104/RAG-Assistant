
FROM python:3.10-slim

# ============================================================
# Environment Variables
# ============================================================

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

# ============================================================
# Working Directory
# ============================================================

WORKDIR /app

# ============================================================
# System Dependencies
# ============================================================

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libgl1 \
    libglib2.0-0 \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*



COPY requirements-docker.txt .

RUN pip install --upgrade pip

# Install CPU-only PyTorch
RUN pip install \
    --index-url https://download.pytorch.org/whl/cpu \
    torch \
    torchvision


RUN pip install -r requirements-docker.txt


COPY . .

EXPOSE 8000


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]