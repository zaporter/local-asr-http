# local-asr-http
Simple HTTP server wrapped in docker to host the nvidia/parakeet-tdt-1.1b transcription model

Not production ready, stable, secure, or performant. If you want to use this, just fork it. Happy to accept PRs.

## Build

```sh
just build
```
(this can take 10-15 minutes -- the img is ~20GB (17 shared, 4.2 unique))


## Run

(starts server on port 9887 by default. Run with `just run port=<otherport>` to change.)
```sh
just run
```

## Using the server:
```sh
# Test status endpoint
curl http://localhost:9887/status

# Test transcribe endpoint
curl -X POST -F "audio_file=@/path/to/your/audio.wav" http://localhost:9887/transcribe
```




**The built docker image inclues parakeet-tdt 1.1b weights. Do not distribute the image -- it likely violates the license. (if you want to package this, let me know.)**


Links:
https://huggingface.co/spaces/hf-audio/open_asr_leaderboard
https://github.com/NVIDIA/NeMo/blob/main/tutorials/asr/Online_ASR_Microphone_Demo_Buffered_Streaming.ipynb
https://docs.nvidia.com/nemo-framework/user-guide/latest/nemotoolkit/asr/intro.html
