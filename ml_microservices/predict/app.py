from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import numpy as np
import tensorflow as tf
import os

UPLOAD_DIR = "uploads"
MODEL_PATH = "model/trained_model.h5"

model = None  # Global model reference

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    try:
        model = tf.keras.models.load_model(MODEL_PATH, compile=False)
        print("✅ Model loaded successfully")
    except Exception as e:
        print("⚠️ Model not loaded:", e)
    
    yield  # App runs here

    # Optional: cleanup code after shutdown

# Use lifespan in FastAPI constructor
app = FastAPI(title="Predict Service", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/predict")
def predict(filename: str = Query(...)):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    img = Image.open(file_path).convert('RGB')
    img = img.resize((224, 224))
    arr = np.array(img) / 255.0
    arr = np.expand_dims(arr, axis=0)
    
    preds = model.predict(arr)
    predicted_class = int(np.argmax(preds))
    
    return {"filename": filename, "prediction": predicted_class}
