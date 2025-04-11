import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Load the datasets
health_data = pd.read_csv('health_monitoring.csv')
safety_data = pd.read_csv('safety_monitoring.csv')

# Display raw data for debugging
print("Raw Health Monitoring Data (First 5 Rows):")
print(health_data.head().to_string())
print("\nRaw Safety Monitoring Data (First 5 Rows):")
print(safety_data.head().to_string())

# Data Cleaning for Health Monitoring Data
def clean_health_data(df):
    # Fill or drop missing values
    df = df.fillna({
        'Heart Rate': '0 Yes',
        'Glucose Levels': '0 Yes',
        'Blood Pressure': '0/0',
        'Oxygen Saturation (SpO₂%)': '0 No',
        'Alert Triggered (Yes/No)': 'No',
        'Caregiver Notified (Yes/No)': 'No'
    })
    
    # Extract numeric values and standardize format
    # Heart Rate: Extract number, validate, and keep as float for now
    df['Heart Rate'] = df['Heart Rate'].astype(str).apply(
        lambda x: float(x.split()[0]) if ' ' in x and x.split()[0].replace('.', '', 1).isdigit() else float(x) if x.replace('.', '', 1).isdigit() else 0.0
    )
    # Glucose Levels: Same approach
    df['Glucose Levels'] = df['Glucose Levels'].astype(str).apply(
        lambda x: float(x.split()[0]) if ' ' in x and x.split()[0].replace('.', '', 1).isdigit() else float(x) if x.replace('.', '', 1).isdigit() else 0.0
    )
    # Blood Pressure: Extract systolic (before '/')
    df['Blood Pressure'] = df['Blood Pressure'].astype(str).apply(
        lambda x: x.split('/')[0] if '/' in x else '0'
    ).astype(float)
    # Oxygen Saturation: Extract number
    df['Oxygen Saturation (SpO₂%)'] = df['Oxygen Saturation (SpO₂%)'].astype(str).apply(
        lambda x: float(x.split()[0]) if ' ' in x and x.split()[0].replace('.', '', 1).isdigit() else float(x) if x.replace('.', '', 1).isdigit() else 0.0
    )
    
    # Convert Timestamp to datetime
    df['Timestamp'] = pd.to_datetime(
        df['Timestamp'].str.extract(r'(\d{1,2}[-/]\d{1,2}[-/]\d{4} \d{1,2}:\d{2})')[0], 
        errors='coerce'
    )
    
    # Validate ranges
    df['Heart Rate'] = df['Heart Rate'].apply(
        lambda x: x if 30 <= x <= 200 else 60.0
    )
    df['Glucose Levels'] = df['Glucose Levels'].apply(
        lambda x: x if 50 <= x <= 400 else 100.0
    )
    
    return df

# Data Cleaning for Safety Monitoring Data
def clean_safety_data(df):
    # Fill or drop missing values
    df = df.fillna({
        'Movement Activity': 'No Movement',
        'Fall Detected (Yes/No)': 'No',
        'Impact Force Level': '-',
        'Post-Fall Inactivity Duration (Seconds)': 0,
        'Location': 'Unknown',
        'Alert Triggered (Yes/No)': 'No',
        'Caregiver Notified (Yes/No)': 'No'
    })
    
    # Convert Timestamp to datetime
    df['Timestamp'] = pd.to_datetime(
        df['Timestamp'].str.extract(r'(\d{1,2}[-/]\d{1,2}[-/]\d{4} \d{1,2}:\d{2})')[0], 
        errors='coerce'
    )
    
    return df

# Clean the datasets
health_data = clean_health_data(health_data)
safety_data = clean_safety_data(safety_data)

# Feature Engineering
features = ['Heart Rate', 'Glucose Levels', 'Blood Pressure', 'Oxygen Saturation (SpO₂%)']

# Target variable
health_data['Caregiver Notified (Yes/No)'] = health_data['Caregiver Notified (Yes/No)'].map({'Yes': 1, 'No': 0})

# Split data into features and target
X = health_data[features]
y = health_data['Caregiver Notified (Yes/No)']

# Handle missing values in features
X = X.fillna(X.mean())

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict on test set
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"\nModel Accuracy: {accuracy:.2f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Visualize feature importance
importances = model.feature_importances_
plt.figure(figsize=(10, 5))
plt.bar(features, importances)
plt.title('Feature Importance')
plt.xlabel('Features')
plt.ylabel('Importance')
plt.show()

# Save the model
joblib.dump(model, 'health_model.pkl')

# import pandas as pd
# import matplotlib.pyplot as plt
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import accuracy_score, classification_report

# # Load the datasets
# health_data = pd.read_csv('health_monitoring.csv')
# safety_data = pd.read_csv('safety_monitoring.csv')

# # Display raw data for debugging
# print("Raw Health Monitoring Data (First 5 Rows):")
# print(health_data.head().to_string())
# print("\nRaw Safety Monitoring Data (First 5 Rows):")
# print(safety_data.head().to_string())

# # Data Cleaning for Health Monitoring Data
# def clean_health_data(df):
#     # Fill or drop missing values
#     df = df.fillna({
#         'Heart Rate': '0 Yes',
#         'Glucose Levels': '0 Yes',
#         'Blood Pressure': '0/0',
#         'Oxygen Saturation (SpO₂%)': '0 No',
#         'Alert Triggered (Yes/No)': 'No',
#         'Caregiver Notified (Yes/No)': 'No'
#     })
    
#     # Extract numeric values and standardize format
#     df['Heart Rate'] = df['Heart Rate'].astype(str).apply(lambda x: x.split()[0] if ' ' in x else x).astype(float).astype(str) + ' Yes'
#     df['Glucose Levels'] = df['Glucose Levels'].astype(str).apply(lambda x: x.split()[0] if ' ' in x else x).astype(float).astype(str) + ' Yes'
#     df['Blood Pressure'] = df['Blood Pressure'].astype(str).apply(lambda x: x.split()[0] if ' ' in x else x.replace('/', ' ').split()[0] + '/' + x.replace('/', ' ').split()[1] if '/' in x else '0/0')
    
#     # Convert Timestamp to datetime
#     df['Timestamp'] = pd.to_datetime(df['Timestamp'].str.extract(r'(\d{1,2}[-/]\d{1,2}[-/]\d{4} \d{1,2}:\d{2})')[0], errors='coerce')
    
#     # Validate ranges (optional, adjust thresholds)
#     df['Heart Rate'] = df.apply(lambda row: row['Heart Rate'] if (int(row['Heart Rate'].split()[0]) <= 200 and int(row['Heart Rate'].split()[0]) >= 30) else '60 Yes', axis=1)
#     df['Glucose Levels'] = df.apply(lambda row: row['Glucose Levels'] if (int(row['Glucose Levels'].split()[0]) <= 400 and int(row['Glucose Levels'].split()[0]) >= 50) else '100 Yes', axis=1)
    
#     return df

# # Data Cleaning for Safety Monitoring Data
# def clean_safety_data(df):
#     # Fill or drop missing values
#     df = df.fillna({
#         'Movement Activity': 'No Movem',
#         'Fall Detected (Yes/No)': 'No',
#         'Impact Force Level': '-',
#         'Post-Fall Inactivity Duration (Seconds)': 0,
#         'Location': '0 Unknown',
#         'Alert Triggered (Yes/No)': 'No',
#         'Caregiver Notified (Yes/No)': 'No'
#     })
    
#     # Convert Timestamp to datetime
#     df['Timestamp'] = pd.to_datetime(df['Timestamp'].str.extract(r'(\d{1,2}[-/]\d{1,2}[-/]\d{4} \d{1,2}:\d{2})')[0], errors='coerce')
    
#     return df

# # Clean the datasets
# health_data = clean_health_data(health_data)
# safety_data = clean_safety_data(safety_data)

# # Feature Engineering (combine health and safety if needed)
# # For simplicity, use health data features
# features = ['Heart Rate', 'Glucose Levels', 'Blood Pressure', 'Oxygen Saturation (SpO₂%)']
# for feature in features:
#     if feature in ['Heart Rate', 'Glucose Levels']:
#         health_data[feature] = health_data[feature].astype(str).str.extract(r'(\d+)')[0].astype(float)
#     elif feature == 'Blood Pressure':
#         health_data[feature] = health_data[feature].astype(str).apply(lambda x: float(x.split('/')[0]) if '/' in x else 0.0)
#     else:  # Oxygen Saturation
#         health_data[feature] = health_data[feature].astype(str).str.extract(r'(\d+)')[0].astype(float)

# # Target variable
# health_data['Caregiver Notified (Yes/No)'] = health_data['Caregiver Notified (Yes/No)'].map({'Yes': 1, 'No': 0})

# # Split data into features and target
# X = health_data[features]
# y = health_data['Caregiver Notified (Yes/No)']

# # Handle missing values in features
# X = X.fillna(X.mean())

# # Split the data into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Train the Random Forest Classifier
# model = RandomForestClassifier(n_estimators=100, random_state=42)
# model.fit(X_train, y_train)

# # Predict on test set
# y_pred = model.predict(X_test)

# # Evaluate the model
# accuracy = accuracy_score(y_test, y_pred)
# print(f"\nModel Accuracy: {accuracy:.2f}")
# print("\nClassification Report:")
# print(classification_report(y_test, y_pred))

# # Optional: Visualize feature importance
# importances = model.feature_importances_
# feature_names = features
# plt.figure(figsize=(10, 5))
# plt.bar(feature_names, importances)
# plt.title('Feature Importance')
# plt.xlabel('Features')
# plt.ylabel('Importance')
# plt.show()

# # Optional: Save the model
# import joblib
# joblib.dump(model, 'health_model.pkl')


# import pandas as pd
# import matplotlib.pyplot as plt
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import accuracy_score, classification_report

# # Load the datasets
# health_data = pd.read_csv('health_monitoring.csv')
# safety_data = pd.read_csv('safety_monitoring.csv')

# # Display raw data for debugging
# print("Raw Health Monitoring Data (First 5 Rows):")
# print(health_data.head().to_string())
# print("\nRaw Safety Monitoring Data (First 5 Rows):")
# print(safety_data.head().to_string())

# # Data Cleaning for Health Monitoring Data
# def clean_health_data(df):
#     # Fill or drop missing values
#     df = df.fillna({'Heart Rate': '0 Yes', 'Glucose Levels': '0 Yes', 'Blood Pressure': '0/0', 'Oxygen Saturation (SpOâ‚‚%)': '0 No',
#                     'Bel. Alert': 'No', 'Trig': 'No', 'Caregiver Notified (Yes/No)': 'No'})
    
#     # Extract numeric values and standardize format
#     df['Heart Rate'] = df['Heart Rate'].astype(str).apply(lambda x: x.split()[0] if ' ' in x else x).astype(float).astype(str) + ' Yes'
#     df['Glucose Levels'] = df['Glucose Levels'].astype(str).apply(lambda x: x.split()[0] if ' ' in x else x).astype(float).astype(str) + ' Yes'
#     df['Blood Pressure'] = df['Blood Pressure'].astype(str).apply(lambda x: x.split()[0] if ' ' in x else x.replace('/', ' ').split()[0] + '/' + x.replace('/', ' ').split()[1] if '/' in x else '0/0')
    
#     # Convert Timestamp to datetime
#     df['Timestamp'] = pd.to_datetime(df['Device-ID/Timestamp'].str.extract(r'(\d{1,2}[-/]\d{1,2}[-/]\d{4} \d{1,2}:\d{2})')[0], errors='coerce')
    
#     # Validate ranges (optional, adjust thresholds)
#     df['Heart Rate'] = df.apply(lambda row: row['Heart Rate'] if (int(row['Heart Rate'].split()[0]) <= 200 and int(row['Heart Rate'].split()[0]) >= 30) else '60 Yes', axis=1)
#     df['Glucose Levels'] = df.apply(lambda row: row['Glucose Levels'] if (int(row['Glucose Levels'].split()[0]) <= 400 and int(row['Glucose Levels'].split()[0]) >= 50) else '100 Yes', axis=1)
    
#     return df

# # Data Cleaning for Safety Monitoring Data
# def clean_safety_data(df):
#     # Fill or drop missing values
#     df = df.fillna({'Movement': 'No Movem', 'Fall Detect': 'No', 'Impact For Post-Fall': '-', 'Location': '0 Unknown',
#                     'Alert Trigge': 'No', 'Caregiver Notified (Yes/No)': 'No'})
    
#     # Convert Timestamp to datetime
#     df['Timestamp'] = pd.to_datetime(df['Device-ID/Timestamp'].str.extract(r'(\d{1,2}[-/]\d{1,2}[-/]\d{4} \d{1,2}:\d{2})')[0], errors='coerce')
    
#     return df

# # Clean the datasets
# health_data = clean_health_data(health_data)
# safety_data = clean_safety_data(safety_data)

# # Feature Engineering (combine health and safety if needed)
# # For simplicity, use health data features
# features = ['Heart Rate', 'Glucose Levels', 'Blood Pressure', 'Oxygen Saturation (SpOâ‚‚%)']
# for feature in features:
#     health_data[feature] = health_data[feature].astype(str).str.extract(r'(\d+)')[0].astype(float)

# # Target variable
# health_data['Caregiver Notified (Yes/No)'] = health_data['Caregiver Notified (Yes/No)'].map({'Yes': 1, 'No': 0})

# # Split data into features and target
# X = health_data[features]
# y = health_data['Caregiver Notified (Yes/No)']

# # Handle missing values in features
# X = X.fillna(X.mean())

# # Split the data into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Train the Random Forest Classifier
# model = RandomForestClassifier(n_estimators=100, random_state=42)
# model.fit(X_train, y_train)

# # Predict on test set
# y_pred = model.predict(X_test)

# # Evaluate the model
# accuracy = accuracy_score(y_test, y_pred)
# print(f"\nModel Accuracy: {accuracy:.2f}")
# print("\nClassification Report:")
# print(classification_report(y_test, y_pred))

# # Optional: Visualize feature importance
# importances = model.feature_importances_
# feature_names = features
# plt.figure(figsize=(10, 5))
# plt.bar(feature_names, importances)
# plt.title('Feature Importance')
# plt.xlabel('Features')
# plt.ylabel('Importance')
# plt.show()

# # Optional: Save the model (if needed)
# import joblib
# joblib.dump(model, 'health_model.pkl')

# import pandas as pd
# import matplotlib.pyplot as plt

# # Load the datasets
# health_data = pd.read_csv('health_monitoring.csv')
# safety_data = pd.read_csv('safety_monitoring.csv')

# # Display the first few rows to verify loading
# print("Health Monitoring Data:")
# print(health_data.head().to_string())
# print("\nSafety Monitoring Data:")
# print(safety_data.head().to_string())

# # Function to check health alerts
# def check_health_alerts(row):
#     alert = False
#     if row['Heart Rate'] != 'No' and int(row['Heart Rate'].split()[0]) > 120:  # Example threshold
#         alert = True
#     if row['Glucose L'] != 'No' and int(row['Glucose L'].split()[0]) > 140:  # Example threshold
#         alert = True
#     if row['Blood Pres'] != 'No' and any(int(x) > 140 for x in row['Blood Pres'].split()[0].split('/')):  # Example threshold
#         alert = True
#     return alert

# # Function to check safety alerts
# def check_safety_alerts(row):
#     alert = False
#     if row['Fall Detect'] == 'Yes' or row['Impact For Post-Fall'] != '-':
#         alert = True
#     elif row['Movement'] == 'No Movem' and row['Timestamp'] < pd.Timestamp.now() - pd.Timedelta(hours=12):  # Example inactivity threshold
#         alert = True
#     return alert

# # Apply alert checks
# health_data['Health_Alert'] = health_data.apply(check_health_alerts, axis=1)
# safety_data['Safety_Alert'] = safety_data.apply(check_safety_alerts, axis=1)

# # Update caregiver notification based on alerts
# health_data['Caregiver Notified (Yes/No)'] = health_data['Health_Alert'].map({True: 'Yes', False: 'No'})
# safety_data['Caregiver Notified (Yes/No)'] = safety_data['Safety_Alert'].map({True: 'No', False: 'No'})  # Assuming no prior notifications

# # Display updated data
# print("\nHealth Monitoring Data with Alerts:")
# print(health_data)
# print("\nSafety Monitoring Data with Alerts:")
# print(safety_data)

# # Optional: Save updated data
# health_data.to_csv('updated_health_monitoring.csv', index=False)
# safety_data.to_csv('updated_safety_monitoring.csv', index=False)

# # Open canvas panel for visualization
# print("\nOpening canvas panel for visualization...")
# # Convert Timestamp to datetime
# health_data['Timestamp'] = pd.to_datetime(health_data['Device-ID/Timestamp'].str.extract(r'(\d{1,2}/\d{1,2}/\d{4} \d{1,2}:\d{2})')[0])
# plt.figure(figsize=(10, 5))
# plt.plot(health_data['Timestamp'], health_data['Heart Rate'].str.extract(r'(\d+)').astype(float), marker='o')
# plt.title('Heart Rate Over Time')
# plt.xlabel('Timestamp')
# plt.ylabel('Heart Rate')
# plt.grid()
# plt.show()

# # [Add your model training code here]
# # Example: If you want to train a model (e.g., using scikit-learn)
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import train_test_split

# # Prepare features and target (example)
# X = health_data[['Heart Rate', 'Glucose L', 'Blood Pres']].apply(lambda x: x.str.extract(r'(\d+)')[0].astype(float) if x.name != 'Blood Pres' else x.str.extract(r'(\d+)/')[0].astype(float))
# y = health_data['Health_Alert'].map({'True': 1, 'False': 0})

# # Handle missing values (if any)
# X = X.fillna(X.mean())
# y = y.fillna(0)

# # Split data
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Train model
# model = RandomForestClassifier(n_estimators=100, random_state=42)
# model.fit(X_train, y_train)

# # Evaluate
# accuracy = model.score(X_test, y_test)
# print(f"\nModel Accuracy: {accuracy}")


# import pandas as pd
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import train_test_split
# import joblib
# import os

# # Load dataset (replace with your health_data.xlsx)
# try:
#     df = pd.read_excel("health_data.xlsx")
# except FileNotFoundError:
#     print("❌ Place 'health_data.xlsx' in the root folder and retry.")
#     exit(1)

# # Features and target
# X = df[["heart_rate", "bp_systolic", "bp_diastolic"]]
# y = df["is_critical"]

# # Split and train
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# model = RandomForestClassifier()
# model.fit(X_train, y_train)

# # Save model
# os.makedirs("models", exist_ok=True)
# joblib.dump(model, "models/health_model.pkl")
# print(f"✅ Model trained and saved. Accuracy on test set: {model.score(X_test, y_test):.2f}")