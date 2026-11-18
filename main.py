from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

# 1. Initialize the FastAPI app
app = FastAPI(title="CPU Thermal & Overheat Prediction API")

# 2. Load your saved Scikit-Learn model
model = joblib.load("my_thermal_model.joblib")

# 3. Define what JSON inputs the API expects
class SensorInput(BaseModel):
    Ambient_Temp: float
    CPU_Usage_Pct: float

# 4. Create the /predict web endpoint
@app.post("/predict")
def predict_temperature(data: SensorInput):
    # Put the incoming JSON numbers into a 1-row table
    input_df = pd.DataFrame(
        [[data.Ambient_Temp, data.CPU_Usage_Pct]],
        columns=["Ambient_Temp", "CPU_Usage_%"]
    )
    
    # Ask the model to predict CPU temperature
    predicted_temp = float(model.predict(input_df)[0])
    
    # Check if the temperature crosses the 75°C safety warning threshold
    overheat_warning = predicted_temp > 75.0
    
    # Return the result as clean JSON
    return {
        "predicted_cpu_temp_c": round(predicted_temp, 2),
        "overheat_warning": overheat_warning,
        "status": "CRITICAL - HIGH TEMP" if overheat_warning else "NORMAL"
    }
