import nemo.collections.asr as nemo_asr
print("starting")
asr_model = nemo_asr.models.EncDecMultiTaskModel.from_pretrained(model_name='nvidia/canary-1b')
print("done")
