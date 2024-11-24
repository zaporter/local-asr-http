ARG CUDA_VERSION=12.1.0

FROM nvidia/cuda:${CUDA_VERSION}-devel-ubuntu22.04 AS base

# Most of this is copied from the vllm dockerfile. If you want to save space, feel free to submit a PR! 
ARG CUDA_VERSION=12.1.0
ARG PYTHON_VERSION=3
ARG PYTHON_VERSION=3.12
ENV DEBIAN_FRONTEND=noninteractive

# Install Python and other dependencies
RUN echo 'tzdata tzdata/Areas select America' | debconf-set-selections \
    && echo 'tzdata tzdata/Zones/America select Los_Angeles' | debconf-set-selections \
    && apt-get update -y \
    && apt-get install -y ccache software-properties-common git curl sudo \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update -y \
    && apt-get install -y python${PYTHON_VERSION} python${PYTHON_VERSION}-dev python${PYTHON_VERSION}-venv \
    && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python${PYTHON_VERSION} 1 \
    && update-alternatives --set python3 /usr/bin/python${PYTHON_VERSION} \
    && ln -sf /usr/bin/python${PYTHON_VERSION}-config /usr/bin/python3-config \
    && curl -sS https://bootstrap.pypa.io/get-pip.py | python${PYTHON_VERSION} \
    && python3 --version && python3 -m pip --version

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY initialize.py .

RUN python3 initialize.py

COPY serve.py .

CMD ["python3", "serve.py"]