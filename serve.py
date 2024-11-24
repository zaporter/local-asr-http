import nemo.collections.asr as nemo_asr
from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse
import uvicorn
import tempfile
import os

app = FastAPI()
asr_model = None

@app.on_event("startup")
async def startup_event():
    global asr_model
    print("Loading ASR model...")
    asr_model = nemo_asr.models.EncDecRNNTBPEModel.from_pretrained(model_name="nvidia/parakeet-tdt-1.1b")
    print("Model loaded successfully")

@app.get("/status")
async def status():
    return {"status": "ok"}

@app.post("/transcribe")
async def transcribe(audio_file: UploadFile):
    if not audio_file.filename.endswith('.wav'):
        return JSONResponse(
            status_code=400,
            content={"error": "Only WAV files are supported"}
        )
    
    # Save the uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
        content = await audio_file.read()
        temp_file.write(content)
        temp_path = temp_file.name

    try:
        # Transcribe the audio
        # TODO: do this without saving to disk.
        transcription = asr_model.transcribe([temp_path])
        
        # Clean up the temporary file
        os.unlink(temp_path)
        
        return {"transcription": transcription[0]}
    except Exception as e:
        # Clean up the temporary file in case of error
        os.unlink(temp_path)
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)