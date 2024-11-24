import nemo.collections.asr as nemo_asr
print("starting")
asr_model = nemo_asr.models.EncDecRNNTBPEModel.from_pretrained(model_name="nvidia/parakeet-tdt-1.1b")
print("done")