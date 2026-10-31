import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split,cross_val_score,KFold
from sklearn.linear_model import LinearRegression,Ridge
from sklearn.metrics import r2_score, mean_squared_error

#Load House Price Dataset
df = pd.read_csv("D:\House_Price_Prediction_524_524\Dataset\dataset.csv")

#Check Missing Values
print("\nMissing Values Before Handling:")
print(df.isnull().sum())

#Check Duplicate Values
print("\nDuplicate Rows Before Handling:")
print(df.duplicated().sum())

#Remove Duplicate Rows
df = df.drop_duplicates()
print("\nDuplicate Rows After Handling:")
print(df.duplicated().sum())

#Check Outliers Before Handling
plt.figure(figsize=(8, 5))
plt.boxplot(df["price"])
plt.title("Price Before Outlier Handling")
plt.ylabel("House Price")
plt.show()

#Handle Outliers using IQR
Q1 = df["price"].quantile(0.25)
Q3 = df["price"].quantile(0.75)
IQR = Q3 - Q1
lower_limit = Q1 - 1.5 * IQR
upper_limit = Q3 + 1.5 * IQR

print("\nLower Limit:", lower_limit)
print("Upper Limit:", upper_limit)

#Remove price outliers
df_clean = df[
    (df["price"] >= lower_limit) &
    (df["price"] <= upper_limit)
].copy()

#Before vs After Comparison
print("\nRecords Before Outlier Handling:", len(df))
print("Records After Outlier Handling:", len(df_clean))

#Box Plot After Outlier Handling
plt.figure(figsize=(8, 5))
plt.boxplot(df_clean["price"])
plt.title("Price After Outlier Handling")
plt.ylabel("House Price")
plt.show()

#Final Missing Value Check
print("\nMissing Values After Handling:")
print(df_clean.isnull().sum())

#AUTOMATED EDA
from ydata_profiling import ProfileReport

#Create Automated EDA Report
profile = ProfileReport(df,title="House Price Prediction - Automated EDA Report",explorative=True)

#Save HTML Report
profile.to_file("D:\House_Price_Prediction_524_524\Reports\EDA_Report.html")
print("\nAutomated EDA Report Generated Successfully!")
print("File: EDA_Report.html")

#Dependent Variable
y = df["price"]

#Independent Variables
X = df[["square_feet","transaction","furnishing","price_per_sqft","bhk","location"]]
print("\nIndependent Variables:")
print(X.columns.tolist())

#Convert Categorical Variables
X = pd.get_dummies(X,columns=["transaction", "furnishing", "location"],drop_first=True)

print("\nFeatures After Encoding:")
print(X.columns.tolist())

#Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.20,random_state=425)

# Display Results
print("\nTrain-Test Split Completed")

print("Training Records:", len(X_train))
print("Testing Records:", len(X_test))
print("Training Features:", X_train.shape)
print("Testing Features:", X_test.shape)

#Linear Regression Model
model = LinearRegression()

#Train Model
model.fit(X_train, y_train)

print("\nLinear Regression Model Trained Successfully!")


#Make Predictions
y_pred = model.predict(X_test)

print("\nFirst 10 Predicted Prices:")
print(y_pred[:10])

comparison = pd.DataFrame({
    "Actual Price": y_test.values[:10],
    "Predicted Price": y_pred[:10]
})
print("\nActual vs Predicted:")

comparison["Actual Price"] = comparison["Actual Price"].map(
    lambda x: f"{x:,.2f}"
)

comparison["Predicted Price"] = comparison["Predicted Price"].map(
    lambda x: f"{x:,.2f}"
)

print(comparison)

#Calculate R²
r2 = r2_score(y_test, y_pred)

#Calculate MSE
mse = mean_squared_error(y_test, y_pred)

#Calculate RMSE
rmse = np.sqrt(mse)

#Display Results
print("\n========== MODEL EVALUATION ==========")
print(f"R² Score : {r2:.4f}")
print(f"MSE : {mse:.2f}")
print(f"RMSE : {rmse:.2f}")
print("=======================================")

#Interpretation
print("\nModel Evaluation Completed Successfully!")

#Original Linear Regression
linear_model = LinearRegression()

linear_model.fit(X_train, y_train)

linear_pred = linear_model.predict(X_test)

linear_r2 = r2_score(y_test, linear_pred)

linear_mse = mean_squared_error(y_test, linear_pred)

linear_rmse = np.sqrt(linear_mse)

#Cross Validation
cv_scores = cross_val_score(
    LinearRegression(),
    X,
    y,
    cv=5,
    scoring="r2"
)

print("\n========== CROSS VALIDATION ==========")

print("5-Fold R² Scores:")
print(cv_scores)

print(f"Average Cross-Validation R²: {cv_scores.mean():.4f}")

#Ridge Regression - Regularization
ridge_model = Ridge(alpha=1.0)

ridge_model.fit(X_train, y_train)

ridge_pred = ridge_model.predict(X_test)

ridge_r2 = r2_score(y_test, ridge_pred)

ridge_mse = mean_squared_error(y_test, ridge_pred)

ridge_rmse = np.sqrt(ridge_mse)

#5-Fold Cross Validation
kf = KFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

linear_cv_scores = cross_val_score(
    LinearRegression(),
    X,
    y,
    cv=kf,
    scoring="r2"
)

print("\n========== LINEAR REGRESSION CROSS VALIDATION ==========")
print("5-Fold R² Scores:")
print(linear_cv_scores)
print(f"Average Cross-Validation R²: {linear_cv_scores.mean():.4f}")

#Ridge Cross Validation
ridge_cv_scores = cross_val_score(
    Ridge(alpha=1.0),
    X,
    y,
    cv=kf,
    scoring="r2"
)

print("\n========== RIDGE CROSS VALIDATION ==========")
print("5-Fold R² Scores:")
print(ridge_cv_scores)
print(f"Average Ridge Cross-Validation R²: {ridge_cv_scores.mean():.4f}")

comparison = pd.DataFrame({
    "Model": [
        "Linear Regression",
        "Ridge Regression"
    ],
    "Test R2": [
        linear_r2,
        ridge_r2
    ],
    "Test MSE": [
        linear_mse,
        ridge_mse
    ],
    "Test RMSE": [
        linear_rmse,
        ridge_rmse
    ],
    "CV Mean R2": [
        linear_cv_scores.mean(),
        ridge_cv_scores.mean()
    ]
})

print("\n========== MODEL COMPARISON ==========")
pd.set_option('display.float_format', '{:,.2f}'.format)
print(comparison.to_string(index=False))

#Final Result
if ridge_r2 > linear_r2:
    print("\nRidge Regression performed better based on R².")
else:
    print("\nLinear Regression performed better based on R².")

 #Best Model
if ridge_r2 > linear_r2:
    print("\nBest Test Model: Ridge Regression")
else:
    print("\nBest Test Model: Linear Regression")
