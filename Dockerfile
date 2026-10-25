# Backend API image
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DATA_DIR=/app/data \
    HF_HOME=/app/data/hf-cache

WORKDIR /app

# CPU-only PyTorch first: the default wheel pulls in ~2 GB of CUDA libraries
# that the embedding model doesn't need.
RUN pip install torch --index-url https://download.pytorch.org/whl/cpu

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY alembic.ini .
COPY alembic ./alembic
COPY app ./app
COPY scripts ./scripts
COPY sample_docs ./sample_docs
COPY docker/entrypoint.sh /entrypoint.sh

RUN useradd --create-home --uid 1000 appuser \
    && mkdir -p /app/data \
    && chown -R appuser:appuser /app \
    && chmod +x /entrypoint.sh
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=15s --timeout=5s --start-period=30s --retries=5 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

ENTRYPOINT ["/entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
