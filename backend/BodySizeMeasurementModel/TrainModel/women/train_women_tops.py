import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import LabelEncoder

data = pd.read_csv("../../Datasets/new/women_tops_size_data.csv")  

label_encoder = LabelEncoder()
data['gender'] = label_encoder.fit_transform(data['gender'])
data['category'] = label_encoder.fit_transform(data['category'])
data['size'] = label_encoder.fit_transform(data['size'])

weights = {
    'bust_cm': 1,
    'waist_cm': 1,
    'low_hip_cm': 1,
    'arm_length_cm': 1
}

data['bust_cm'] = data['bust_cm'] * weights['bust_cm']
data['waist_cm'] = data['waist_cm'] * weights['waist_cm']
data['low_hip_cm'] = data['low_hip_cm'] * weights['low_hip_cm']
data['arm_length_cm'] = data['arm_length_cm'] * weights['arm_length_cm']

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
feature_names = ['gender', 'category', 'bust_cm', 'waist_cm', 'low_hip_cm', 'arm_length_cm']

plt.figure(figsize=(10, 6))
plt.barh(feature_names, feature_importances, color='skyblue')
plt.xlabel('Feature Importance')
plt.title('Feature Importance in Predicting Body Size')
plt.show()

correlation = data[['low_hip_cm','arm_length_cm','bust_cm', 'waist_cm','size']].corr()
print(correlation)

def predict_size():
    # User input
    gender = input("Enter gender (men/women): ")
    category = input("Enter clothing category (tops/bottoms/shoes): ")
    bust_cm = float(input("Enter bust size (cm): ")) * weights['bust_cm']
    waist_cm = float(input("Enter waist size (cm): ")) * weights['waist_cm']
    low_hip_cm = float(input("Enter lower hip size (cm): ")) * weights['low_hip_cm']
    arm_length_cm = float(input("Enter arm length (cm): ")) * weights['arm_length_cm']
    
    label_encoder_gender = LabelEncoder()
    label_encoder_category = LabelEncoder()
    label_encoder_size = LabelEncoder()
    
    label_encoder_gender.fit(['men', 'women'])  
    label_encoder_category.fit(['tops', 'bottoms', 'shoes'])  
    label_encoder_size.fit(['XXS','XS','S','M','L','XL','2XL','3XL'])  

    gender_encoded = label_encoder_gender.transform([gender])[0]  
    category_encoded = label_encoder_category.transform([category])[0]

    user_input = pd.DataFrame({
        'gender': [gender_encoded],
        'category': [category_encoded],
        'bust_cm': [bust_cm],
        'waist_cm': [waist_cm],
        'low_hip_cm': [low_hip_cm],
        'arm_length_cm': [arm_length_cm]
    })

    predicted_size = model.predict(user_input)
    predicted_size_rounded = round(predicted_size[0])

    predicted_size_label = label_encoder_size.inverse_transform([predicted_size_rounded])[0]
    print(f"The predicted clothing size is: {predicted_size_label}")

predict_size()

# bust,waist,low hip,armlength = 84,65,90,57 in cm