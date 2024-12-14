import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import LabelEncoder


data = pd.read_csv("../../Datasets/men/men_bottoms_size_data.csv")

label_encoder = LabelEncoder()
data['gender'] = label_encoder.fit_transform(data['gender'])
data['category'] = label_encoder.fit_transform(data['category'])
data['size'] = label_encoder.fit_transform(data['size'])


X = data.drop(columns=["size"])  
y = data["size"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = xgb.XGBRegressor(objective='reg:squarederror', max_depth=5, learning_rate=0.1, n_estimators=100)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f"Mean Absolute Error: {mae}")

import matplotlib.pyplot as plt

feature_importances = model.feature_importances_

feature_names = ['gender', 'category', 'waist_cm', 'low_hip_cm', 'inseam_cm']  

plt.figure(figsize=(10, 6))
plt.barh(feature_names, feature_importances, color='skyblue')
plt.xlabel('Feature Importance')
plt.title('Feature Importance in Predicting Body Size')
plt.show()

correlation = data[['waist_cm', 'low_hip_cm', 'inseam_cm', 'size']].corr()
print(correlation)

def predict_size():
    # User input
    gender = input("Enter gender (men/women): ")
    category = input("Enter clothing category (tops/bottoms/shoes): ")
    waist_cm = float(input("Enter waist size (cm): "))
    low_hip_cm = float(input("Enter lower hip size (cm): "))
    inseam_cm = float(input("Enter inseam size (cm): "))
    
    label_encoder_gender = LabelEncoder()
    label_encoder_category = LabelEncoder()
    label_encoder_size = LabelEncoder()
    
    label_encoder_gender.fit(['men', 'women'])  
    label_encoder_category.fit(['tops', 'bottoms', 'shoes'])  
    label_encoder_size.fit(['XS','S','M','L','XL','XXL','3XL','4XL','5XL','6XL','7XL','8XL'])  

    gender_encoded = label_encoder_gender.transform([gender])[0]  
    category_encoded = label_encoder_category.transform([category])[0]

    user_input = pd.DataFrame({
        'gender': [gender_encoded],
        'category': [category_encoded],
        'waist_cm': [waist_cm],
        'low_hip_cm': [low_hip_cm],
        'inseam_cm': [inseam_cm]
    })

    predicted_size = model.predict(user_input)
    predicted_size_rounded = round(predicted_size[0])

    predicted_size_label = label_encoder_size.inverse_transform([predicted_size_rounded])[0]
    print(f"The predicted clothing size is: {predicted_size_label}")

predict_size()

# arm,waist,chest,neck= 81 74 94 in cm