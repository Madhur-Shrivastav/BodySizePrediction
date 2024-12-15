import pandas as pd
<<<<<<< HEAD
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

df = pd.read_csv("../../Datasets/women/tops_data.csv")

style_encoder = LabelEncoder()
category_encoder = LabelEncoder()
size_encoder = LabelEncoder()

df['style'] = style_encoder.fit_transform(df['style'])
df['category'] = category_encoder.fit_transform(df['category'])
df['size'] = size_encoder.fit_transform(df['size'])

X = df[['style', 'category', 'chest_cm', 'waist_cm', 'low_hip_cm']]
y = df['size']

scaler = StandardScaler()
X = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100}%")

size_mapping = {index: label for index, label in enumerate(size_encoder.classes_)}
print("Size Mapping:", size_mapping)

valid_styles = style_encoder.classes_
valid_categories = category_encoder.classes_

print("\nValid Styles:", valid_styles)
print("Valid Categories:", valid_categories)

def match_category_input(user_input, categories):
    user_input = user_input.strip().lower()
    for category in categories:
        parts = category.split('_')
        if user_input in parts or user_input == category:
            return category
    return None

def predict_size():
    print("\n--- Enter the following details to predict your size ---")
    try:
        style = input(f"Style (choose from {list(valid_styles)}): ")
        if style not in valid_styles:
            raise ValueError(f"Invalid style. Choose from {list(valid_styles)}.")

        category = input(f"Category (enter full name or components): ").strip()
        matched_category = match_category_input(category, valid_categories)

        if not matched_category:
            raise ValueError(f"Invalid category. Please enter a valid full category or component.")

        chest_cm = float(input("Chest size (in cm): "))
        waist_cm = float(input("Waist size (in cm): "))
        low_hip_cm = float(input("Low Hip size (in cm): "))

        style_encoded = style_encoder.transform([style])[0]
        category_encoded = category_encoder.transform([matched_category])[0]

        input_data = pd.DataFrame(
            [[style_encoded, category_encoded, chest_cm, waist_cm, low_hip_cm]],
            columns=['style', 'category', 'chest_cm', 'waist_cm', 'low_hip_cm']
        )

        input_scaled = scaler.transform(input_data)
        predicted_size_index = model.predict(input_scaled)[0]
        predicted_size = size_mapping.get(predicted_size_index, "Unknown")
        print(f"\nPredicted Size: {predicted_size}")

    except ValueError as ve:
        print(f"Input Error: {ve}")
    except Exception as e:
        print(f"Error: {e}\nPlease ensure the inputs are correct.")


predict_size()

=======
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
>>>>>>> 71c0661c0e7e537aa71dec2e942c463d0d4ca099
