import os

from transformers import AutoModel, AutoFeatureExtractor, AutoModelForImageClassification
import torch
from PIL import Image

# ---------------------------------------------------------------
# Load transformers model
# ---------------------------------------------------------------
def loadModel(modelFile: str):
    '''
    Load model from file
    input:
        modelFile: name of the model file (str)
    output:
        model: loaded model (keras.model)
    '''
    return AutoModel.from_pretrained(modelFile)

# ---------------------------------------------------------------
# Run first prediction
# ---------------------------------------------------------------
def runFirstPrediction(modelName: str):
    '''
    Run first prediction
    input:
        model: loaded model (str)
    output:
        predictions: list of predictions (list)
    '''
    predictions = []
    path = 'images/CERN-THESIS-2020-410/'
    for image in os.listdir(path):
        image = Image.open(path+image).convert('RGB')
        feature_extractor = AutoFeatureExtractor.from_pretrained(modelName)
        model = AutoModelForImageClassification.from_pretrained(modelName)
        inputs = feature_extractor(images=image, return_tensors="pt")
        outputs = model(**inputs)
        logits = outputs.logits
        predicted_class_idx = logits.argmax(-1).item()
        print(f"Predicted class for image {image}: {model.config.id2label[predicted_class_idx]}")
    return predictions