import os
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error  # Removed accuracy_score for regression
from sklearn.feature_extraction.text import TfidfVectorizer

# Ensure the output directory exists
output_dir = "/Users/noveranasa/AI-CPS/Project/project/learningBase"
os.makedirs(output_dir, exist_ok=True)

# Step 1: Load Data
train_path = os.path.join(output_dir, "training_data.csv")
test_path = os.path.join(output_dir, "test_data.csv")

train_data = pd.read_csv(train_path)
test_data = pd.read_csv(test_path)

#  'review_text' is the feature and 'score' is the target
X_train = train_data['review_text']
y_train = train_data['score']
X_test = test_data['review_text']
y_test = test_data['score']

# Step 2: Data Preprocessing
# Convert text to numerical features using TF-IDF
vectorizer = TfidfVectorizer(max_features=5000)
X_train_vec = vectorizer.fit_transform(X_train).toarray()
X_test_vec = vectorizer.transform(X_test).toarray()

# Normalize the data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_vec)
X_test_scaled = scaler.transform(X_test_vec)

# Check if data conversion is successful
print("X_train_scaled dtype:", X_train_scaled.dtype)
print("X_train_scaled first 5 rows:\n", X_train_scaled[:5])
print("y_train dtype:", y_train.dtype)
print("y_train first 5 rows:\n", y_train[:5])

# Convert 'score' column to numeric, handling errors
y_train = pd.to_numeric(y_train, errors='coerce')  # Converts invalid values to NaN
y_test = pd.to_numeric(y_test, errors='coerce')  

# Replace NaN values (e.g., from 'No Score') with the mean score or another strategy
y_train.fillna(y_train.mean(), inplace=True)
y_test.fillna(y_test.mean(), inplace=True)

# Convert labels to float
y_train = y_train.astype('float32')
y_test = y_test.astype('float32')

# Check if any NaN values remain
if np.any(np.isnan(y_train)) or np.any(np.isnan(y_test)):
    print("Warning: NaN values found in y_train or y_test after conversion.")


# Step 3: Build the Model
model = Sequential([
    Dense(256, activation='relu', input_shape=(X_train_scaled.shape[1],)),
    Dropout(0.3),
    Dense(128, activation='relu'),
    Dropout(0.2),
    Dense(1, activation='linear')  # Using linear activation for regression
])

# Compile the model
model.compile(optimizer=Adam(learning_rate=0.001),
              loss='mean_squared_error',
              metrics=['mean_absolute_error'])

# Step 4: Train the Model
history = model.fit(X_train_scaled, y_train,
                    validation_data=(X_test_scaled, y_test),
                    epochs=20, batch_size=32)

# Step 5: Save the Model
model_path = os.path.join(output_dir, "currentAiSolution.h5")
model.save(model_path)
print(f"Model saved at {model_path}")

# Save model summary
summary_path = os.path.join(output_dir, "model_summary.txt")
with open(summary_path, "w") as f:
    model.summary(print_fn=lambda x: f.write(x + "\n"))

# Step 6: Evaluate the Model
test_predictions = model.predict(X_test_scaled)
mse = mean_squared_error(y_test, test_predictions)

# Save performance metrics
performance_metrics = f"Final Loss: {history.history['loss'][-1]}\n" \
                      f"Final Validation Loss: {history.history['val_loss'][-1]}\n" \
                      f"Test MSE: {mse}\n"
    
metrics_path = os.path.join(output_dir, "performance_metrics.txt")
with open(metrics_path, "w") as f:
    f.write(performance_metrics)

# Step 7: Generate Visualizations
# Training & Validation Loss
plt.figure(figsize=(8, 6))
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.title('Training and Validation Loss')
plt.savefig(os.path.join(output_dir, "training_validation_loss.png"))

# Training Diagnostic: Scatter plot (predicted vs actual)
plt.figure(figsize=(8, 6))
plt.scatter(y_test, test_predictions, alpha=0.6)
plt.xlabel('Actual Scores')
plt.ylabel('Predicted Scores')
plt.title('Predicted vs Actual Scores')
plt.savefig(os.path.join(output_dir, "scatter_plot.png"))

