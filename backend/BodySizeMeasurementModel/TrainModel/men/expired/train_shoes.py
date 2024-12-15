import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import LabelEncoder


data = pd.read_csv("../../Datasets/men/men_shoes_size_data.csv")

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

feature_names = ['gender', 'category', 'foot_length_cm']  

plt.figure(figsize=(10, 6))
plt.barh(feature_names, feature_importances, color='skyblue')
plt.xlabel('Feature Importance')
plt.title('Feature Importance in Predicting Body Size')
plt.show()

correlation = data[['foot_length_cm', 'size']].corr()
print(correlation)

def predict_size():

    gender = input("Enter gender (men/women): ")
    category = input("Enter clothing category (tops/bottoms/shoes): ")
    foot_length_cm = float(input("Enter foot length (cm): "))
    
    label_encoder_gender = LabelEncoder()
    label_encoder_category = LabelEncoder()
    label_encoder_size = LabelEncoder()
    
    label_encoder_gender.fit(['men','women'])  
    label_encoder_category.fit(['tops', 'bottoms', 'shoes'])  
    label_encoder_size.fit(['US6', 'US7', 'US8', 'US9', 'US10','US11','US12', 'US13', 'US14'])  

    gender_encoded = label_encoder_gender.transform([gender])[0]  
    category_encoded = label_encoder_category.transform([category])[0]

    user_input = pd.DataFrame({
        'gender': [gender_encoded],
        'category': [category_encoded],
        'foot_length_cm': [foot_length_cm]
    })

    predicted_size = model.predict(user_input)
    predicted_size_rounded = round(predicted_size[0])

    predicted_size_label = label_encoder_size.inverse_transform([predicted_size_rounded])[0]
    print(f"The predicted clothing size is: {predicted_size_label}")

predict_size()

# foot_length_cm = 25 in cm

