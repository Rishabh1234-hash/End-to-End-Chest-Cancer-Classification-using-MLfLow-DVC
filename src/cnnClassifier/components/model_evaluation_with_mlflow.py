import tensorflow as tf
from pathlib import Path
import mlflow
import mlflow.keras
from urllib.parse import urlparse
from cnnClassifier.entity.config_entity import EvaluationConfig
from cnnClassifier.utils.common import read_yaml, create_directories,save_json


class Evaluation:
    def __init__(self, config: EvaluationConfig):
        self.config = config

    def _valid_generator(self):
        datagenerator_kwargs = dict(
            rescale=1./255,
            validation_split=0.30
        )

        dataflow_kwargs = dict(
            target_size=self.config.params_image_size[:-1],
            batch_size=self.config.params_batch_size,
            interpolation="bilinear"
        )

        valid_datagenerator = tf.keras.preprocessing.image.ImageDataGenerator(
            **datagenerator_kwargs
        )

        self.valid_generator = valid_datagenerator.flow_from_directory(
            directory=self.config.training_data,
            subset="validation",
            shuffle=False,
            **dataflow_kwargs
        )

    @staticmethod
    def load_model(path: Path) -> tf.keras.Model:
        return tf.keras.models.load_model(path)

    def evaluation(self):
        self.model = self.load_model(self.config.path_of_model)
        self._valid_generator()

        # Evaluate model loss & accuracy
        self.score = self.model.evaluate(self.valid_generator)

        # Get predictions for additional metrics
        y_true = self.valid_generator.classes
        y_pred_probs = self.model.predict(self.valid_generator)
        y_pred = np.argmax(y_pred_probs, axis=1)

        # Compute metrics
        self.precision = precision_score(y_true, y_pred, average="weighted")
        self.recall = recall_score(y_true, y_pred, average="weighted")
        self.f1 = f1_score(y_true, y_pred, average="weighted")
        self.conf_matrix = confusion_matrix(y_true, y_pred).tolist()

        self.save_score()

    def save_score(self):
        scores = {
            "loss": self.score[0],
            "accuracy": self.score[1],
            "precision": self.precision,
            "recall": self.recall,
            "f1_score": self.f1,
            "confusion_matrix": self.conf_matrix
        }
        save_json(path=Path("scores.json"), data=scores)

    def log_into_mlflow(self):
        mlflow.set_tracking_uri(self.config.mlflow_uri)
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        with mlflow.start_run():
            mlflow.log_params(self.config.all_params)
            mlflow.log_metrics({
                "loss": self.score[0],
                "accuracy": self.score[1],
                "precision": self.precision,
                "recall": self.recall,
                "f1_score": self.f1
            })

            # Do NOT use model registry if using DagsHub
            if "dagshub" in self.config.mlflow_uri.lower():
                mlflow.keras.log_model(self.model, "model")  # Without registry
            elif tracking_url_type_store != "file":
                mlflow.keras.log_model(self.model, "model", registered_model_name="VGG16Model")
            else:
                mlflow.keras.log_model(self.model, "model")
