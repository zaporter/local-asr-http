default:
    just --list

build:
    docker build -t local-asr-http .

run port='9887':
    docker run \
    --gpus all \
    -it \
    --rm \
    --shm-size=8g \
    --ulimit memlock=-1 \
    --ulimit stack=67108864 \
    -p {{port}}:8000 \
    local-asr-http