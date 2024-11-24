ARG CUDA_VERSION=12.1.0

FROM nvidia/cuda:${CUDA_VERSION}-devel-ubuntu22.04 AS base

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY serve.py .

CMD ["python", "serve.py"]