import pandas as pd
import statsmodels.api as sm
import pickle

# Load training data
train_df = pd.read_csv("training_data.csv")

# Data Cleaning
train_df = train_df[train_df['score'] != 'No Score']
train_df['score'] = train_df['score'].astype(float)
train_df['price'] = train_df['price'].str.replace(r'[^\d.]', '', regex=True).astype(float)
train_df['reviews_count'] = pd.to_numeric(train_df['reviews_count'], errors='coerce')
train_df['free_cancellation'] = train_df['free_cancellation'].apply(lambda x: 1 if 'Free' in x else 0)
train_df['review_text'] = train_df['review_text'].astype('category').cat.codes
train_df = train_df.dropna()

# Feature Selection
X_train = train_df[['price', 'reviews_count', 'review_text', 'free_cancellation']]
y_train = train_df['score']

# Add constant for OLS regression
X_train = sm.add_constant(X_train)

# Train OLS Model
ols_model = sm.OLS(y_train, X_train).fit()

# Save the trained model
with open("currentOlsSolution.pkl", "wb") as file:
    pickle.dump(ols_model, file)

# Print Model Summary
print(ols_model.summary())
