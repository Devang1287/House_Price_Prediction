# =============================================================================
# Course: SYBCA-AI (Sem-III)
# Subject: 303 Machine Learning - Practical Journal Submission (Mini Project)
# Project Title: House Price Prediction
# Roll No: 524, 553
# =============================================================================

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import r2_score, mean_squared_error

# -----------------------------------------------------------------------------
# PATH CONFIGURATION (Dynamic path so it runs anywhere)
# -----------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
DATASET_PATH = os.path.join(PROJECT_DIR, "Dataset", "dataset.csv")
REPORTS_DIR = os.path.join(PROJECT_DIR, "Reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

print("=" * 70)
print("  SYBCA-AI (Sem-III) - 303 Machine Learning Mini Project")
print("  PROJECT: House Price Prediction")
print("=" * 70)


# =============================================================================
# STEP 1 & 2: DATASET COLLECTION & ATTRIBUTE STUDY
# =============================================================================
print("\n[STEP 1 & 2] Loading and Inspecting Dataset...")
df = pd.read_csv(DATASET_PATH)

print(f"Total Records Loaded : {df.shape[0]}")
print(f"Total Features/Columns: {df.shape[1]}")
print("\nFirst 5 Records:")
print(df.head())


# =============================================================================
# STEP 3: UNDERSTANDING DATA (Unit-1)
# =============================================================================
print("\n" + "=" * 70)
print("  STEP 3: UNDERSTANDING DATA (Unit-1)")
print("=" * 70)

# Identify Numerical and Categorical Columns
num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
cat_cols = df.select_dtypes(include=["object", "string"]).columns.tolist()

print(f"Numerical Columns   ({len(num_cols)}): {num_cols}")
print(f"Categorical Columns ({len(cat_cols)}): {cat_cols}")

# Check Missing Values
print("\nMissing Values Count:")
print(df.isnull().sum())

# Check Duplicate Values
duplicate_count = df.duplicated().sum()
print(f"\nDuplicate Records Count: {duplicate_count}")

# Statistical Summary
print("\nStatistical Summary (Describe):")
print(df.describe())


# =============================================================================
# STEP 4: EXPLORATORY DATA ANALYSIS - EDA (Unit-1 & Unit-2)
# =============================================================================
print("\n" + "=" * 70)
print("  STEP 4: EXPLORATORY DATA ANALYSIS (Unit-1 & Unit-2)")
print("=" * 70)

# Set visual style
sns.set_theme(style="whitegrid")

# 1. Histogram: Distribution of House Prices
plt.figure(figsize=(8, 5))
plt.hist(df["price"] / 100000, bins=25, color="skyblue", edgecolor="black")
plt.title("1. Histogram - House Price Distribution (in Lakhs)", fontsize=13, fontweight="bold")
plt.xlabel("Price (in Lakhs INR)")
plt.ylabel("Frequency / Count")
plt.tight_layout()
plt.savefig(os.path.join(REPORTS_DIR, "eda_histogram.png"), dpi=200)
plt.close()
print(" -> Saved: eda_histogram.png")

# 2. Box Plot: Price Distribution & Initial Outliers
plt.figure(figsize=(7, 5))
plt.boxplot(df["price"] / 100000, patch_artist=True, boxprops=dict(facecolor="lightcoral"))
plt.title("2. Box Plot - House Prices Before Outlier Removal", fontsize=13, fontweight="bold")
plt.ylabel("Price (in Lakhs INR)")
plt.tight_layout()
plt.savefig(os.path.join(REPORTS_DIR, "eda_boxplot_before.png"), dpi=200)
plt.close()
print(" -> Saved: eda_boxplot_before.png")

# 3. Pie Chart: Furnishing Status Distribution
plt.figure(figsize=(6, 6))
furnishing_counts = df["furnishing"].value_counts()
colors = ["#ff9999", "#66b3ff", "#99ff99"]
plt.pie(furnishing_counts, labels=furnishing_counts.index, autopct="%1.1f%%", startangle=140, colors=colors)
plt.title("3. Pie Chart - Furnishing Status Distribution", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig(os.path.join(REPORTS_DIR, "eda_pie_chart.png"), dpi=200)
plt.close()
print(" -> Saved: eda_pie_chart.png")

# 4. Bar Chart: Average Price by BHK
plt.figure(figsize=(8, 5))
avg_price_bhk = df.groupby("bhk")["price"].mean() / 100000
plt.bar(avg_price_bhk.index.astype(str) + " BHK", avg_price_bhk.values, color="teal", edgecolor="black")
plt.title("4. Bar Chart - Average House Price by BHK", fontsize=13, fontweight="bold")
plt.xlabel("BHK Configuration")
plt.ylabel("Average Price (in Lakhs INR)")
plt.tight_layout()
plt.savefig(os.path.join(REPORTS_DIR, "eda_barchart.png"), dpi=200)
plt.close()
print(" -> Saved: eda_barchart.png")

# 5. Correlation Matrix Heatmap
plt.figure(figsize=(7, 5))
numeric_subset = df[num_cols]
corr_matrix = numeric_subset.corr()
sns.heatmap(corr_matrix, annot=True, cmap="Blues", fmt=".2f", linewidths=0.5)
plt.title("5. Correlation Matrix Heatmap", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig(os.path.join(REPORTS_DIR, "eda_correlation_matrix.png"), dpi=200)
plt.close()
print(" -> Saved: eda_correlation_matrix.png")
print("EDA plots created and saved successfully.")


# =============================================================================
# STEP 5: DATA PREPROCESSING & OUTLIER HANDLING (Unit-2)
# =============================================================================
print("\n" + "=" * 70)
print("  STEP 5: DATA PREPROCESSING & OUTLIER HANDLING (Unit-2)")
print("=" * 70)

# A. Remove Duplicate Records
initial_len = len(df)
df_clean = df.drop_duplicates().copy()
removed_dups = initial_len - len(df_clean)
print(f"Removed Duplicate Records: {removed_dups}")
print(f"Records Remaining: {len(df_clean)}")

# B. Missing Value Handling
# Checking if any missing values need imputation
if df_clean.isnull().sum().sum() > 0:
    df_clean = df_clean.dropna()
    print("Handled missing values by dropping null rows.")
else:
    print("No missing values detected in dataset.")

# C. Outlier Handling using IQR (Interquartile Range) Method
Q1 = df_clean["price"].quantile(0.25)
Q3 = df_clean["price"].quantile(0.75)
IQR = Q3 - Q1
lower_limit = Q1 - 1.5 * IQR
upper_limit = Q3 + 1.5 * IQR

print("\nIQR Outlier Calculation for 'price':")
print(f"Q1 (25th Percentile) : Rs. {Q1:,.2f}")
print(f"Q3 (75th Percentile) : Rs. {Q3:,.2f}")
print(f"IQR                  : Rs. {IQR:,.2f}")
print(f"Lower Cutoff Limit   : Rs. {lower_limit:,.2f}")
print(f"Upper Cutoff Limit   : Rs. {upper_limit:,.2f}")

# Filter out outliers
before_outlier_count = len(df_clean)
df_clean = df_clean[(df_clean["price"] >= lower_limit) & (df_clean["price"] <= upper_limit)].copy()
after_outlier_count = len(df_clean)

# Box Plot After Outlier Handling
plt.figure(figsize=(7, 5))
plt.boxplot(df_clean["price"] / 100000, patch_artist=True, boxprops=dict(facecolor="lightgreen"))
plt.title("Box Plot - House Prices After Outlier Removal", fontsize=13, fontweight="bold")
plt.ylabel("Price (in Lakhs INR)")
plt.tight_layout()
plt.savefig(os.path.join(REPORTS_DIR, "eda_boxplot_after.png"), dpi=200)
plt.close()

# Before vs After Comparison Report
print("\n--- Before vs After Preprocessing Summary ---")
print(f"Total Rows Before Preprocessing: {initial_len}")
print(f"Total Rows After Duplicates Drop: {before_outlier_count}")
print(f"Outliers Removed from 'price'   : {before_outlier_count - after_outlier_count}")
print(f"Final Cleaned Dataset Records   : {after_outlier_count}")


# =============================================================================
# STEP 6: AUTOMATED EDA (Unit-2)
# =============================================================================
print("\n" + "=" * 70)
print("  STEP 6: AUTOMATED EDA (Unit-2)")
print("=" * 70)

html_report_path = os.path.join(REPORTS_DIR, "EDA_Report.html")
if os.path.exists(html_report_path):
    print(f"Automated EDA HTML Report already exists at: {html_report_path}")
else:
    print("Generating Automated EDA Report using ydata-profiling...")
    try:
        from ydata_profiling import ProfileReport
        profile = ProfileReport(df, title="House Price Prediction - Automated EDA Report", explorative=True)
        profile.to_file(html_report_path)
        print("Generated HTML report: EDA_Report.html")
    except Exception as e:
        print(f"Note on Automated EDA: {e}")


# =============================================================================
# STEP 7: FEATURE SELECTION & TRAIN-TEST SPLIT
# =============================================================================
print("\n" + "=" * 70)
print("  STEP 7: FEATURE SELECTION & TRAIN-TEST SPLIT")
print("=" * 70)

# Target Variable (Dependent Variable)
y = df_clean["price"]

# Feature Variables (Independent Variables)
X = df_clean[["square_feet", "transaction", "furnishing", "price_per_sqft", "bhk", "location"]]

print("Target Variable (y) : price")
print("Feature Variables(X): ['square_feet', 'transaction', 'furnishing', 'price_per_sqft', 'bhk', 'location']")

# Convert Categorical variables using One-Hot Encoding
X_encoded = pd.get_dummies(X, columns=["transaction", "furnishing", "location"], drop_first=True)
print(f"Features after One-Hot Encoding: {X_encoded.shape[1]} columns")

# Split Dataset into Training (80%) and Testing (20%)
X_train, X_test, y_train, y_test = train_test_split(
    X_encoded, y, test_size=0.20, random_state=42
)

print(f"Training Set Size : {X_train.shape[0]} records ({X_train.shape[1]} features)")
print(f"Testing Set Size  : {X_test.shape[0]} records")


# =============================================================================
# STEP 8: BUILD MACHINE LEARNING MODEL - LINEAR REGRESSION (Unit-4)
# =============================================================================
print("\n" + "=" * 70)
print("  STEP 8: BUILD ML MODEL - LINEAR REGRESSION (Unit-4)")
print("=" * 70)

# Instantiate Linear Regression Model
linear_model = LinearRegression()

# Train Model on Training Data
linear_model.fit(X_train, y_train)
print("Linear Regression Model trained successfully!")


# =============================================================================
# STEP 9: MODEL EVALUATION (Unit-3 & Unit-4)
# =============================================================================
print("\n" + "=" * 70)
print("  STEP 9: MODEL EVALUATION (Unit-3 & Unit-4)")
print("=" * 70)

# Predict on Test Data
y_pred_linear = linear_model.predict(X_test)

# Calculate Evaluation Metrics
lr_r2 = r2_score(y_test, y_pred_linear)
lr_mse = mean_squared_error(y_test, y_pred_linear)
lr_rmse = np.sqrt(lr_mse)

print("Linear Regression Evaluation Metrics:")
print(f"1. R-Squared (R2) Score : {lr_r2:.4f} (Explains {lr_r2 * 100:.2f}% of price variance)")
print(f"2. Mean Squared Error    : {lr_mse:,.2f}")
print(f"3. Root Mean Squared Error: Rs. {lr_rmse:,.2f}")

# Display Sample of Actual vs Predicted Prices
sample_comparison = pd.DataFrame({
    "Actual Price (Rs.)": y_test.values[:5],
    "Predicted Price (Rs.)": y_pred_linear[:5],
    "Difference (Error)": np.abs(y_test.values[:5] - y_pred_linear[:5])
})
print("\nSample Actual vs Predicted Prices (First 5):")
print(sample_comparison.to_string(index=False))


# =============================================================================
# STEP 10: IMPROVE MODEL - CROSS VALIDATION & REGULARIZATION (Unit-4)
# =============================================================================
print("\n" + "=" * 70)
print("  STEP 10: IMPROVE MODEL - CROSS VALIDATION & REGULARIZATION (Unit-4)")
print("=" * 70)

# A. 5-Fold Cross Validation for Linear Regression
kf = KFold(n_splits=5, shuffle=True, random_state=42)
cv_linear_scores = cross_val_score(LinearRegression(), X_encoded, y, cv=kf, scoring="r2")
cv_linear_mean = cv_linear_scores.mean()

print("5-Fold Cross Validation Scores (Linear Regression):")
for fold_idx, score in enumerate(cv_linear_scores, start=1):
    print(f"  Fold {fold_idx}: R2 = {score:.4f}")
print(f"Average CV R2 Score : {cv_linear_mean:.4f}")

# B. Regularization using Ridge Regression (L2 Penalty)
ridge_model = Ridge(alpha=1.0)
ridge_model.fit(X_train, y_train)
y_pred_ridge = ridge_model.predict(X_test)

ridge_r2 = r2_score(y_test, y_pred_ridge)
ridge_mse = mean_squared_error(y_test, y_pred_ridge)
ridge_rmse = np.sqrt(ridge_mse)

cv_ridge_scores = cross_val_score(Ridge(alpha=1.0), X_encoded, y, cv=kf, scoring="r2")
cv_ridge_mean = cv_ridge_scores.mean()

# C. Compare Models in a Structured Table
comparison_df = pd.DataFrame({
    "Model Name": ["Linear Regression", "Ridge Regression (Regularized)"],
    "Test R2 Score": [f"{lr_r2:.4f}", f"{ridge_r2:.4f}"],
    "Test RMSE (Rs.)": [f"{lr_rmse:,.2f}", f"{ridge_rmse:,.2f}"],
    "Mean 5-Fold CV R2": [f"{cv_linear_mean:.4f}", f"{cv_ridge_mean:.4f}"]
})

print("\n========== MODEL COMPARISON TABLE ==========")
print(comparison_df.to_string(index=False))


# =============================================================================
# STEP 11 & 12 & 13: RESULTS, CONCLUSION & FUTURE SCOPE
# =============================================================================
print("\n" + "=" * 70)
print("  CONCLUSION & FINDINGS")
print("=" * 70)

if ridge_r2 > lr_r2:
    best_model_name = "Ridge Regression"
    print("Finding: Ridge Regression slightly outperforms standard Linear Regression")
    print("         because L2 regularization helps mitigate multicollinearity.")
else:
    best_model_name = "Linear Regression"
    print("Finding: Linear Regression provides a strong linear baseline.")

print(f"\nFinal Best Selected Model: {best_model_name}")
print(f"Model Accuracy (R2 Score): {max(lr_r2, ridge_r2):.4f}")
print("\nProject execution finished successfully!")
print("=" * 70)
