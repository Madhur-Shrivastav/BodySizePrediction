from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

# Load the pre-trained model, label encoder, and imputer
model = joblib.load('./BodySizeMeasurementModel/body_size_predictor_rf_model.pkl')
label_encoder = joblib.load('./BodySizeMeasurementModel/label_encoder.pkl')
imputer = joblib.load('./BodySizeMeasurementModel/imputer.pkl')

app = FastAPI()

# Add CORS middleware to allow requests from React app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app's address
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods like GET, POST, etc.
    allow_headers=["*"],  # Allow all headers
)

class BodySizeInput(BaseModel):
    weight: float
    height: float
   
   
    waist_size: float
    
    

@app.post("/predict/")
def predict_body_size(input_data: BodySizeInput):
    # Prepare input data
    input_df = pd.DataFrame([[input_data.weight, input_data.height,
                              input_data.waist_size, 
                              ]],
                             columns=['Weight', 'Height',  
                                      'Waist Size', ])
    
    # Impute missing values
    input_imputed = imputer.transform(input_df)

    # Make prediction
    prediction = model.predict(input_imputed)
    
    # Decode the predicted size
    predicted_size = label_encoder.inverse_transform(prediction)
    print("For input:",input_imputed, "Predicted Size is:",predicted_size[0])
    
    return {"predicted_size": predicted_size[0]}

