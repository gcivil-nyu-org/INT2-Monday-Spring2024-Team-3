from sagemaker.huggingface import HuggingFacePredictor

endpoint_name = "huggingface-pytorch-inference-2024-04-10-04-28-53-172"
predictor = HuggingFacePredictor(endpoint_name=endpoint_name)


def detect_hate_speech(text: str):
    response = predictor.predict({"inputs": text})
    return response
