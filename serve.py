import nemo.collections.asr as nemo_asr
from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse
import uvicorn
import tempfile
import os
import json

app = FastAPI()
asr_model = None

@app.on_event("startup")
async def startup_event():
    global asr_model
    print("Loading ASR model...")
    asr_model = nemo_asr.models.EncDecMultiTaskModel.from_pretrained(model_name='nvidia/canary-1b')
    decode_cfg = asr_model.cfg.decoding
    decode_cfg.beam.beam_size = 1
    asr_model.change_decoding_strategy(decode_cfg)
    print("Model loaded successfully")

@app.get("/status")
async def status():
    if asr_model is None:
        return JSONResponse(
            status_code=500,
            content={"error": "Model not loaded"}
        )
    return {"status": "ok"}


@app.post("/transcribe")
async def transcribe(audio_file: UploadFile):
    if not audio_file.filename.endswith('.wav'):
        return JSONResponse(
            status_code=400,
            content={"error": "Only WAV files are supported"}
        )
    
    audio_filepath = None
    json_filepath = None
    
    try:
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            content = await audio_file.read()
            temp_file.write(content)
            audio_filepath = temp_file.name
        
        # Verify the audio file exists and get its size
        audio_size = os.path.getsize(audio_filepath)
        print(f"Saved audio file at {audio_filepath} (size: {audio_size} bytes)")

        with tempfile.NamedTemporaryFile(delete=False, suffix='.json', mode='w') as temp_file:
            data = {
                "audio_filepath": audio_filepath,
                "duration": None,
                "taskname": "asr",  
                "source_lang": "en",
                "target_lang": "en",
                "pnc": "yes",
                "answer": "na",
            }
            json.dump(data, temp_file)
            json_filepath = temp_file.name

        # Verify the JSON file exists
        print(f"Saved JSON file at {json_filepath}")
        
        # Verify files exist before transcription
        if not os.path.exists(audio_filepath):
            raise Exception(f"Audio file {audio_filepath} does not exist before transcription")
        if not os.path.exists(json_filepath):
            raise Exception(f"JSON file {json_filepath} does not exist before transcription")

        # Transcribe the audio
        transcription = asr_model.transcribe(
            json_filepath,
            batch_size=1,
        )
        print(f"Transcription result: {transcription}")
        
        return {"transcription": transcription[0]}
    except Exception as e:
        print(f"Error during transcription: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
    finally:
        # Clean up files in finally block
        if audio_filepath and os.path.exists(audio_filepath):
            os.unlink(audio_filepath)
            print(f"Cleaned up audio file: {audio_filepath}")
        if json_filepath and os.path.exists(json_filepath):
            os.unlink(json_filepath)
            print(f"Cleaned up JSON file: {json_filepath}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)