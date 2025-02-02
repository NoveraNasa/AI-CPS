import pandas as pd
from sklearn.model_selection import train_test_split

# File paths
input_file = "hotels_list_3000.csv"
output_cleaned_file = "joint_data_collection.csv"
output_training_file = "training_data.csv"
output_test_file = "test_data.csv"
output_activation_file = "activation_data.csv"

# Step 1: Load the dataset
try:
    data = pd.read_csv(input_file, encoding='ISO-8859-1')  # Adjust encoding if needed
    print("Column Names:", data.columns)  # Check column names
except UnicodeDecodeError as e:
    print("Error loading file:", e)
    exit()

# Step 2: Verify the review column exists
review_column = 'review_text'  # Update to use the correct column name
if review_column not in data.columns:
    print(f"Error: Column '{review_column}' not found in dataset.")
    print("Available columns:", data.columns)
    exit()

# Step 3: Data Cleaning
data[review_column] = data[review_column].str.lower()  # Normalize text
data = data.drop_duplicates().dropna(subset=[review_column])  # Drop missing reviews

# Step 4: Save cleaned dataset
data.to_csv(output_cleaned_file, index=False)

# Step 5: Split into training and test datasets
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)
train_data.to_csv(output_training_file, index=False)
test_data.to_csv(output_test_file, index=False)

# Step 6: Create activation data
activation_data = test_data.sample(n=1, random_state=42)
activation_data.to_csv(output_activation_file, index=False)

print("Data preparation completed successfully.")

