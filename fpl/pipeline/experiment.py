"""Example implementation of MLFLOW tracking.

Further details on: https://www.mlflow.org/docs/latest/tracking.html
"""
import os

import mlflow

# Loading environment settings from file.
MLFLOW_URL = os.getenv("MLFLOW_URL") or "http://0.0.0.0:5000"


def experiment():
    """Run training as MLFlow Experiment."""
    # Set tracking server.
    mlflow.set_tracking_uri(MLFLOW_URL)

    # Try to create new experiment, else reuse old.
    try:
        experiment_id = mlflow.create_experiment("Timeseries-LSTM")
    except mlflow.exceptions.RestException:
        experiment_id = mlflow.get_experiment_by_name("Timeseries-LSTM").experiment_id

    with mlflow.start_run(run_name="First try", experiment_id=experiment_id):
        # Documentation https://www.mlflow.org/docs/latest/python_api/mlflow.html
        mlflow.log_params({"Params example": 1})
        mlflow.log_metric("Metric example", 100)
        mlflow.log_text("example output", "example.txt")
        mlflow.log_artifacts("test", "test")


if __name__ == "__main__":
    experiment()
