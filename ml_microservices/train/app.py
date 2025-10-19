import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from cnnClassifier.entity.config_entity import TrainingConfig
from cnnClassifier.components.model_trainer import Training
from pathlib import Path

app = FastAPI()

# Allow CORS if your frontend and backend are on different origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/train")
async def train_model(request: Request):
    try:
        # Assume project root is 3 levels above this file
        project_root = Path(__file__).resolve().parent.parent.parent
        
        # --- MODIFICATION START ---

        # Define the directory path for the models
        model_dir = project_root / "model" # <-- ADDED LINE
        
        # Ensure the directory to save the model exists
        os.makedirs(model_dir, exist_ok=True) # <-- ADDED LINE

        # Compose absolute paths using the defined model directory
        updated_base_model_path = model_dir / "model.h5"
        trained_model_path = model_dir / "trained_model.h5"
        
        # --- MODIFICATION END ---
        
        training_data_path = project_root / "data" / "train"

        # Create TrainingConfig with absolute paths
        config = TrainingConfig(
            root_dir=project_root,
            trained_model_path=trained_model_path,
            updated_base_model_path=updated_base_model_path,
            training_data=training_data_path,
            params_epochs=10,
            params_batch_size=32,
            params_is_augmentation=True,
            params_image_size=[224, 224, 3],
        )

        trainer = Training(config)
        trainer.get_base_model()
        trainer.train_valid_generator()
        trainer.train()

        return JSONResponse(content={"message": "Training completed successfully"})
    except Exception as e:
        # It's helpful to log the full error to the console for debugging
        import traceback
        traceback.print_exc()
        return JSONResponse(content={"detail": f"Training failed: {str(e)}"}, status_code=500)
