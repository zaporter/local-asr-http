default:
    just --list

build:
    docker build -t local-asr-http .

run port='9887':
    docker run -p {{port}}:8080 local-asr-http