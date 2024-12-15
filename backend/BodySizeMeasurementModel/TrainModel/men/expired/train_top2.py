import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

data = pd.read_csv("../../Datasets/newmen/shirts_data.csv")  

label_encoder = LabelEncoder()
data['style'] = label_encoder.fit_transform(data['style'])
data['category'] = label_encoder.fit_transform(data['category'])
data['size'] = label_encoder.fit_transform(data['size'])

# weights = {
#     'chest_cm': 1,
#     'waist_cm': 1,
#     'neckline_cm': 1,
#     'arm_length_cm': 1
# }

# data['chest_cm'] = data['chest_cm'] * weights['chest_cm']
# data['waist_cm'] = data['waist_cm'] * weights['waist_cm']
# data['neckline_cm'] = data['neckline_cm'] * weights['neckline_cm']
# data['arm_length_cm'] = data['arm_length_cm'] * weights['arm_length_cm']

X = data[['style', 'category', 'chest_cm', 'waist_cm', 'arm_length_cm', 'neckline_cm']]  
y = data["size"]

scaler = StandardScaler()
X = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#-------------------------------------------------------------------------------------------------------------------#

# param_dist = {
#     'max_depth': [3, 5, 7, 9],
#     'learning_rate': [0.01, 0.05, 0.1, 0.15],
#     'n_estimators': [50, 100, 150, 200],
#     'subsample': [0.7, 0.8, 0.9],
#     'colsample_bytree': [0.7, 0.8, 0.9]
# }
# random_search = RandomizedSearchCV(xgb.XGBRegressor(objective='reg:squarederror'), param_dist, n_iter=10, cv=5, scoring='neg_mean_squared_error')
# random_search.fit(X_train, y_train)
# model = random_search.best_estimator_

#-------------------------------------------------------------------------------------------------------------------#

# param_grid = {
#     'max_depth': [3, 5, 7],
#     'learning_rate': [0.01, 0.1, 0.3],
#     'n_estimators': [50, 100, 150]
# }
# grid_search = GridSearchCV(xgb.XGBRegressor(objective='reg:squarederror'), param_grid, cv=5, scoring='neg_mean_squared_error')
# grid_search.fit(X_train, y_train)
# model = grid_search.best_estimator_

#-------------------------------------------------------------------------------------------------------------------#

# model = xgb.XGBRegressor(objective='reg:squarederror', max_depth=5, learning_rate=0.1, n_estimators=100)
# model.fit(X_train, y_train)

#-------------------------------------------------------------------------------------------------------------------#

# model = KNeighborsClassifier(n_neighbors=5)  # Set k=3, can be tuned for better accuracy
# model.fit(X_train, y_train)

#-------------------------------------------------------------------------------------------------------------------#

model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

#-------------------------------------------------------------------------------------------------------------------#

y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f"Mean Absolute Error: {mae}")

accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# import matplotlib.pyplot as plt
# correlation = data[['neckline_cm', 'arm_length_cm', 'chest_cm', 'waist_cm', 'size']].corr()
# print("Correlation Matrix:\n", correlation)
# plt.figure(figsize=(8, 5))
# correlation['size'].drop('size').plot(kind='barh', color='skyblue')
# plt.xlabel('Correlation with Size')
# plt.title('Feature Correlation with Size')
# plt.show()


# feature_importances = model.feature_importances_
# feature_names = ['category','style', 'chest_cm', 'waist_cm','arm_length_cm' ,'neckline_cm']

# plt.figure(figsize=(10, 6))
# plt.barh(feature_names, feature_importances, color='skyblue')
# plt.xlabel('Feature Importance')
# plt.title('Feature Importance in Predicting Body Size')
# plt.show()

# correlation = data[['neckline_cm','arm_length_cm','chest_cm', 'waist_cm','size']].corr()
# print(correlation)

def predict_size():
 
    category = input("Enter clothing category: ")
    style = input("Enter clothing style(regular/long): ")
    # chest_cm = float(input("Enter chest size (cm): ")) * weights['chest_cm']
    # waist_cm = float(input("Enter waist size (cm): ")) * weights['waist_cm']
    # neckline_cm = float(input("Enter neckline size (cm): ")) * weights['neckline_cm']
    # arm_length_cm = float(input("Enter arm length (cm): ")) * weights['arm_length_cm']
    
    chest_cm = float(input("Enter chest size (cm): ")) 
    waist_cm = float(input("Enter waist size (cm): ")) 
    neckline_cm = float(input("Enter neckline size (cm): ")) 
    arm_length_cm = float(input("Enter arm length (cm): ")) 
    
    label_encoder_category = LabelEncoder()
    label_encoder_style = LabelEncoder()
    label_encoder_size = LabelEncoder()
    
    label_encoder_category.fit(['shirts'])  
    label_encoder_style.fit(['regular','long'])
    label_encoder_size.fit(['XXS','XS','S','M','L','XL','XXL','3XL'])  

    category_encoded = label_encoder_category.transform([category])[0]
    style_encoded = label_encoder_style.transform([style])[0]

    user_input = pd.DataFrame({
        'category': [category_encoded],
        'style': [style_encoded],
        'chest_cm': [chest_cm],
        'waist_cm': [waist_cm],
        'arm_length_cm': [arm_length_cm],
        'neckline_cm': [neckline_cm],
    })

    predicted_size = model.predict(user_input)
    predicted_size_rounded = round(predicted_size[0])

    predicted_size_label = label_encoder_size.inverse_transform([predicted_size_rounded])[0]
    print(f"The predicted clothing size is: {predicted_size_label}")



predict_size()

# chest,waist,neckline,armlength = 98,81,37,56 in cm