import os
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import numpy as np
import tensorflow as tf
import uvicorn

UPLOAD_DIR = os.path.join("..", "upload", "uploads")
MODEL_PATH = r"C:\Users\globa\Downloads\MIT\B.Tech\TY\S1\CCD\End-to-End-Chest-Cancer-Classification-using-MLfLow-DVC\model\trained_model.h5"

app = FastAPI(title="Predict Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

model = None

@app.on_event("startup")
def load_model():
    global model
    try:
        # Load the model without compiling to avoid reduction argument error
        model = tf.keras.models.load_model(MODEL_PATH, compile=False)
        print("✅ Model loaded successfully")
    except Exception as e:
        print("⚠️ Model not loaded:", e)

@app.get("/predict")
def predict(filename: str = Query(...)):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    img=Image.open(file_path).convert('RGB')
    img = img.resize((224, 224))
    arr = np.array(img) / 255.0
    arr = np.expand_dims(arr, axis=0)
    preds = model.predict(arr)
    predicted_class = int(np.argmax(preds))
    return {"filename": filename, "prediction": predicted_class}
