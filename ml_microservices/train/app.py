import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pathlib import Path

from cnnClassifier.entity.config_entity import TrainingConfig
from cnnClassifier.components.model_trainer import Training

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/train")
async def train_model(request: Request):
    try:
        # Use in-container paths
        model_dir = Path("model")
        training_data_path = Path("data/train")

        os.makedirs(model_dir, exist_ok=True)

        updated_base_model_path = model_dir / "model.h5"
        trained_model_path = model_dir / "trained_model.h5"

        config = TrainingConfig(
            root_dir=Path("."),
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
        import traceback
        traceback.print_exc()
        return JSONResponse(content={"detail": f"Training failed: {str(e)}"}, status_code=500)
