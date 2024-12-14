import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import random

df = pd.read_csv("../../Datasets/men/jeans_trousers_data.csv")

size_encoder = LabelEncoder()
category_encoder = LabelEncoder()

df['category'] = category_encoder.fit_transform(df['category'])
df['size'] = size_encoder.fit_transform(df['size'])

base_features = ['category', 'waist_cm', 'low_hip_cm']
length_columns = ['30inch_length_cm', '32inch_length_cm', '34inch_length_cm']

size_mapping = {index: label for index, label in enumerate(size_encoder.classes_)}
valid_categories = category_encoder.classes_

def train_model(length_column):
    features = base_features + [length_column]
    X = df[features]
    y = df['size']

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy (using {length_column}): {accuracy * 100:.2f}%")
    return model, scaler

def predict_size():
    print("\n--- Enter the following details to predict your jeans/trousers size ---")
    try:
        category = input(f"Category (choose from {list(valid_categories)}): ")
        if category not in valid_categories:
            raise ValueError(f"Invalid category. Choose from {list(valid_categories)}.")
        
        waist_cm = float(input("Waist size (in cm): "))
        low_hip_cm = float(input("Low hip size (in cm): "))
        
        print("\nSelect the length option:")
        print("1. 30 inch")
        print("2. 32 inch")
        print("3. 34 inch")
        
        length_option = int(input("Enter 1, 2, or 3: "))
        
        if length_option == 1:
            selected_length = '30inch_length_cm'
        elif length_option == 2:
            selected_length = '32inch_length_cm'
        elif length_option == 3:
            selected_length = '34inch_length_cm'
        else:
            raise ValueError("Invalid option. Please choose 1, 2, or 3.")
        
        model, scaler = train_model(selected_length)
        
        # length_value = float(input(f"Enter the {selected_length} value (in cm): "))
        
        # input_data = pd.DataFrame(
        #     [[category_encoder.transform([category])[0], waist_cm, low_hip_cm, length_value]],
        #     columns=base_features + [selected_length]
        # )
        
        random_length_value = random.choice(df[selected_length].dropna().values)
        print(f"\nRandomly selected {selected_length} value: {random_length_value} cm")
        
        input_data = pd.DataFrame(
            [[category_encoder.transform([category])[0], waist_cm, low_hip_cm, random_length_value]],
            columns=base_features + [selected_length]
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

# my waist,hip,inseam= 81,94,80 in cm