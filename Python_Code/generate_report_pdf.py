import os
import pandas as pd
import numpy as np

from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

# Path configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
REPORTS_DIR = os.path.join(PROJECT_DIR, "Reports")
PDF_PATH = os.path.join(REPORTS_DIR, "Project_Report.pdf")

doc = SimpleDocTemplate(
    PDF_PATH,
    pagesize=A4,
    leftMargin=40,
    rightMargin=40,
    topMargin=40,
    bottomMargin=40
)

styles = getSampleStyleSheet()

# Custom styles
title_style = ParagraphStyle(
    "DocTitle",
    parent=styles["Heading1"],
    fontSize=24,
    leading=30,
    textColor=colors.HexColor("#1A365D"),
    alignment=1, # Center
    fontName="Helvetica-Bold",
    spaceAfter=15
)

subtitle_style = ParagraphStyle(
    "DocSubtitle",
    parent=styles["Normal"],
    fontSize=13,
    leading=18,
    textColor=colors.HexColor("#2B6CB0"),
    alignment=1,
    fontName="Helvetica",
    spaceAfter=25
)

h1_style = ParagraphStyle(
    "SectionH1",
    parent=styles["Heading1"],
    fontSize=16,
    leading=20,
    textColor=colors.HexColor("#1A365D"),
    fontName="Helvetica-Bold",
    spaceBefore=14,
    spaceAfter=8,
    keepWithNext=True
)

h2_style = ParagraphStyle(
    "SectionH2",
    parent=styles["Heading2"],
    fontSize=12,
    leading=16,
    textColor=colors.HexColor("#2C5282"),
    fontName="Helvetica-Bold",
    spaceBefore=10,
    spaceAfter=6,
    keepWithNext=True
)

body_style = ParagraphStyle(
    "DocBody",
    parent=styles["Normal"],
    fontSize=9.5,
    leading=14,
    textColor=colors.HexColor("#2D3748"),
    spaceAfter=6
)

bullet_style = ParagraphStyle(
    "DocBullet",
    parent=styles["Normal"],
    fontSize=9,
    leading=13,
    textColor=colors.HexColor("#2D3748"),
    leftIndent=15,
    spaceAfter=3
)

code_style = ParagraphStyle(
    "CodeSnippet",
    parent=styles["Code"],
    fontSize=8,
    leading=11,
    textColor=colors.HexColor("#1A202C"),
    backColor=colors.HexColor("#EDF2F7"),
    spaceAfter=6
)

story = []

# =============================================================================
# 1. COVER PAGE
# =============================================================================
story.append(Spacer(1, 40))
story.append(Paragraph("SYBCA-AI (Sem-III)", ParagraphStyle("CoverSem", parent=title_style, fontSize=18, leading=22, textColor=colors.HexColor("#4A5568"))))
story.append(Paragraph("303 Machine Learning", ParagraphStyle("CoverSub", parent=title_style, fontSize=16, leading=20, textColor=colors.HexColor("#2B6CB0"))))
story.append(Spacer(1, 25))
story.append(HRFlowable(width="80%", thickness=2, color=colors.HexColor("#2B6CB0"), spaceAfter=25))
story.append(Paragraph("PRACTICAL JOURNAL SUBMISSION<br/>(MINI PROJECT)", ParagraphStyle("CoverType", parent=title_style, fontSize=15, leading=19, textColor=colors.HexColor("#718096"))))
story.append(Spacer(1, 20))
story.append(Paragraph("PROJECT TITLE:<br/>HOUSE PRICE PREDICTION", title_style))
story.append(Paragraph("A Machine Learning Approach to Real Estate Price Estimation", subtitle_style))
story.append(Spacer(1, 40))

student_info = [
    [Paragraph("<b>Submitted By:</b>", body_style), Paragraph("Roll No. 524, 524", body_style)],
    [Paragraph("<b>Class:</b>", body_style), Paragraph("SYBCA-AI (Semester III)", body_style)],
    [Paragraph("<b>Course Code:</b>", body_style), Paragraph("303 Machine Learning", body_style)],
    [Paragraph("<b>Academic Term:</b>", body_style), Paragraph("2026-2027", body_style)],
    [Paragraph("<b>Target Domain:</b>", body_style), Paragraph("Real Estate & Finance (Topic #21)", body_style)]
]
t_info = Table(student_info, colWidths=[150, 250])
t_info.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F7FAFC")),
    ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E0")),
    ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ('LEFTPADDING', (0,0), (-1,-1), 12),
]))
story.append(t_info)
story.append(Spacer(1, 40))
story.append(HRFlowable(width="80%", thickness=1, color=colors.HexColor("#CBD5E0"), spaceAfter=20))
story.append(Paragraph("Department of Computer Applications & Artificial Intelligence", subtitle_style))
story.append(PageBreak())

# =============================================================================
# 2. CERTIFICATE
# =============================================================================
story.append(Paragraph("CERTIFICATE", title_style))
story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2B6CB0"), spaceAfter=25))
story.append(Spacer(1, 15))

cert_text = (
    "This is to certify that the project entitled <b>\"House Price Prediction\"</b> has been "
    "satisfactorily completed by the students with <b>Roll No. 524, 524</b> of <b>SYBCA-AI (Semester-III)</b> "
    "in partial fulfillment of the practical journal requirements for the course <b>303 Machine Learning</b> "
    "as prescribed by the syllabus during the academic year."
)
story.append(Paragraph(cert_text, ParagraphStyle("CertBody", parent=body_style, fontSize=11, leading=18, alignment=4))) # Justified
story.append(Spacer(1, 20))

cert_text_2 = (
    "The students have independently executed all practical stages of the Machine Learning lifecycle including "
    "dataset collection, exploratory data analysis, outlier & missing value preprocessing, automated EDA, "
    "feature engineering, Linear Regression model development, model evaluation, and model improvement via "
    "cross-validation and regularization."
)
story.append(Paragraph(cert_text_2, ParagraphStyle("CertBody2", parent=body_style, fontSize=11, leading=18, alignment=4)))
story.append(Spacer(1, 70))

sig_table_data = [
    [Paragraph("______________________", body_style), Paragraph("______________________", body_style), Paragraph("______________________", body_style)],
    [Paragraph("<b>Internal Faculty Guide</b>", body_style), Paragraph("<b>Head of Department</b>", body_style), Paragraph("<b>External Examiner</b>", body_style)],
    [Paragraph("Date: ______________", body_style), Paragraph("Date: ______________", body_style), Paragraph("Date: ______________", body_style)]
]
t_sig = Table(sig_table_data, colWidths=[160, 160, 160])
t_sig.setStyle(TableStyle([
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ('TOPPADDING', (0,0), (-1,-1), 4),
]))
story.append(t_sig)
story.append(PageBreak())

# =============================================================================
# 3. PROBLEM STATEMENT & 4. OBJECTIVES
# =============================================================================
story.append(Paragraph("3. Problem Statement", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E0"), spaceAfter=8))
story.append(Paragraph(
    "Determining the fair market price of residential properties is a complex challenge influenced by numerous "
    "interdependent factors including property size (square footage), locality/neighborhood, bedroom configurations (BHK), "
    "transaction type (New Property vs. Resale), and furnishing status. Traditional manual appraisals can be biased, "
    "time-consuming, and prone to inconsistency. Hence, there is a strong demand for an objective, automated machine learning "
    "solution that accurately models price dynamics based on real-world housing characteristics.",
    body_style
))
story.append(Spacer(1, 10))

story.append(Paragraph("4. Objectives", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E0"), spaceAfter=8))
objectives = [
    "To analyze a real-world residential dataset containing over 300 records and 7 distinct attributes.",
    "To perform rigorous data preprocessing including duplicate removal, missing value verification, and IQR-based outlier treatment.",
    "To carry out Exploratory Data Analysis (EDA) using 5 distinct graphical representations (Histogram, Box Plot, Pie Chart, Bar Chart, Correlation Matrix).",
    "To generate an automated, interactive HTML EDA profiling report using ydata-profiling.",
    "To build a supervised Machine Learning Linear Regression model predicting continuous property prices.",
    "To evaluate model performance using standard regression metrics: R² (R-squared), Mean Squared Error (MSE), and Root Mean Squared Error (RMSE).",
    "To improve and validate model reliability through 5-Fold Cross-Validation and Regularization (Ridge Regression L2 penalty)."
]
for obj in objectives:
    story.append(Paragraph(f"• {obj}", bullet_style))
story.append(Spacer(1, 12))

# =============================================================================
# 5. DATASET DESCRIPTION
# =============================================================================
story.append(Paragraph("5. Dataset Description", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E0"), spaceAfter=8))
story.append(Paragraph(
    "The dataset utilized for this project is a real-world residential housing dataset (`dataset.csv`) comprising <b>446 rows</b> "
    "and <b>7 features</b>, strictly fulfilling the course requirements (minimum 300 records and 5+ attributes).",
    body_style
))

ds_table_data = [
    [Paragraph("<b>Attribute Name</b>", body_style), Paragraph("<b>Data Type</b>", body_style), Paragraph("<b>Variable Type</b>", body_style), Paragraph("<b>Description</b>", body_style)],
    [Paragraph("square_feet", body_style), Paragraph("Integer", body_style), Paragraph("Feature (Independent)", body_style), Paragraph("Total carpet area in sq. ft.", body_style)],
    [Paragraph("transaction", body_style), Paragraph("Categorical", body_style), Paragraph("Feature (Independent)", body_style), Paragraph("Resale or New Property", body_style)],
    [Paragraph("furnishing", body_style), Paragraph("Categorical", body_style), Paragraph("Feature (Independent)", body_style), Paragraph("Furnished, Semi-Furnished, Unfurnished", body_style)],
    [Paragraph("price_per_sqft", body_style), Paragraph("Float", body_style), Paragraph("Feature (Independent)", body_style), Paragraph("Unit rate per square foot (INR)", body_style)],
    [Paragraph("bhk", body_style), Paragraph("Integer", body_style), Paragraph("Feature (Independent)", body_style), Paragraph("Number of Bedrooms/Hall/Kitchen (1-8)", body_style)],
    [Paragraph("location", body_style), Paragraph("Categorical", body_style), Paragraph("Feature (Independent)", body_style), Paragraph("Suburban location (Adajan, Vesu, etc.)", body_style)],
    [Paragraph("price", body_style), Paragraph("Integer", body_style), Paragraph("Target (Dependent)", body_style), Paragraph("Total property price in INR", body_style)]
]
t_ds = Table(ds_table_data, colWidths=[85, 70, 115, 200])
t_ds.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold')
]))
story.append(t_ds)
story.append(Spacer(1, 10))

# =============================================================================
# 6. DATA PREPROCESSING
# =============================================================================
story.append(Paragraph("6. Data Preprocessing (Unit-2)", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E0"), spaceAfter=8))
story.append(Paragraph(
    "Data preprocessing ensures dataset cleanliness and prevents distortions in model training. The key steps implemented include:",
    body_style
))
story.append(Paragraph("• <b>Missing Values:</b> Audited all 7 columns using <code>df.isnull().sum()</code>. Zero missing entries were found.", bullet_style))
story.append(Paragraph("• <b>Duplicate Records:</b> Detected and eliminated <b>13 duplicate rows</b> using <code>df.drop_duplicates()</code>.", bullet_style))
story.append(Paragraph("• <b>Outlier Detection & Removal (IQR Method):</b> Applied on target variable <code>price</code>:", bullet_style))

iqr_data = [
    [Paragraph("<b>Metric</b>", body_style), Paragraph("<b>Value</b>", body_style)],
    [Paragraph("Q1 (25th Percentile)", body_style), Paragraph("Rs. 4,600,000 (46 Lakhs)", body_style)],
    [Paragraph("Q3 (75th Percentile)", body_style), Paragraph("Rs. 16,300,000 (1.63 Crore)", body_style)],
    [Paragraph("Interquartile Range (IQR)", body_style), Paragraph("Rs. 11,700,000", body_style)],
    [Paragraph("Lower Limit (Q1 - 1.5 * IQR)", body_style), Paragraph("Rs. -12,950,000 (Effective floor 0)", body_style)],
    [Paragraph("Upper Limit (Q3 + 1.5 * IQR)", body_style), Paragraph("Rs. 33,850,000 (3.385 Crore)", body_style)],
    [Paragraph("Records Before Preprocessing", body_style), Paragraph("446 records", body_style)],
    [Paragraph("Records After Duplicate Removal", body_style), Paragraph("433 records", body_style)],
    [Paragraph("Outliers Removed (Above Upper Cutoff)", body_style), Paragraph("18 records", body_style)],
    [Paragraph("Final Cleaned Dataset", body_style), Paragraph("<b>415 records</b>", body_style)]
]
t_iqr = Table(iqr_data, colWidths=[220, 250])
t_iqr.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EDF2F7")),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
    ('TOPPADDING', (0,0), (-1,-1), 3),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
]))
story.append(t_iqr)
story.append(PageBreak())

# =============================================================================
# 7. EXPLORATORY DATA ANALYSIS (EDA)
# =============================================================================
story.append(Paragraph("7. Exploratory Data Analysis (Unit-1 & Unit-2)", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E0"), spaceAfter=8))
story.append(Paragraph(
    "Exploratory Data Analysis allows us to understand feature distributions, patterns, skewness, and relationships between "
    "independent attributes and house price. As required by the project specifications, the following 5 charts were generated:",
    body_style
))

# Chart 1 & Chart 2 side by side
hist_img = os.path.join(REPORTS_DIR, "eda_histogram.png")
box_before_img = os.path.join(REPORTS_DIR, "eda_boxplot_before.png")
box_after_img = os.path.join(REPORTS_DIR, "eda_boxplot_after.png")
pie_img = os.path.join(REPORTS_DIR, "eda_pie_chart.png")
bar_img = os.path.join(REPORTS_DIR, "eda_barchart.png")
corr_img = os.path.join(REPORTS_DIR, "eda_correlation_matrix.png")

eda_table_1 = [
    [
        Image(hist_img, width=2.8*inch, height=1.9*inch) if os.path.exists(hist_img) else Paragraph("Histogram", body_style),
        Image(box_before_img, width=2.8*inch, height=1.9*inch) if os.path.exists(box_before_img) else Paragraph("Boxplot Before", body_style)
    ],
    [
        Paragraph("<b>Figure 1:</b> Histogram of House Prices (Lakhs)", ParagraphStyle("Cap1", parent=body_style, fontSize=8, alignment=1)),
        Paragraph("<b>Figure 2:</b> Box Plot Before Outlier Removal", ParagraphStyle("Cap2", parent=body_style, fontSize=8, alignment=1))
    ]
]
t_eda1 = Table(eda_table_1, colWidths=[240, 240])
t_eda1.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'), ('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
story.append(t_eda1)
story.append(Spacer(1, 8))

eda_table_2 = [
    [
        Image(pie_img, width=2.6*inch, height=1.9*inch) if os.path.exists(pie_img) else Paragraph("Pie Chart", body_style),
        Image(bar_img, width=2.8*inch, height=1.9*inch) if os.path.exists(bar_img) else Paragraph("Bar Chart", body_style)
    ],
    [
        Paragraph("<b>Figure 3:</b> Furnishing Status Distribution", ParagraphStyle("Cap3", parent=body_style, fontSize=8, alignment=1)),
        Paragraph("<b>Figure 4:</b> Average Price by BHK Configuration", ParagraphStyle("Cap4", parent=body_style, fontSize=8, alignment=1))
    ]
]
t_eda2 = Table(eda_table_2, colWidths=[240, 240])
t_eda2.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'), ('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
story.append(t_eda2)
story.append(Spacer(1, 8))

eda_table_3 = [
    [
        Image(box_after_img, width=2.8*inch, height=1.9*inch) if os.path.exists(box_after_img) else Paragraph("Boxplot After", body_style),
        Image(corr_img, width=2.8*inch, height=1.9*inch) if os.path.exists(corr_img) else Paragraph("Correlation Matrix", body_style)
    ],
    [
        Paragraph("<b>Figure 5:</b> Box Plot After Outlier Removal", ParagraphStyle("Cap5", parent=body_style, fontSize=8, alignment=1)),
        Paragraph("<b>Figure 6:</b> Correlation Matrix Heatmap", ParagraphStyle("Cap6", parent=body_style, fontSize=8, alignment=1))
    ]
]
t_eda3 = Table(eda_table_3, colWidths=[240, 240])
t_eda3.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'), ('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
story.append(t_eda3)
story.append(Spacer(1, 8))

story.append(Paragraph(
    "<b>Automated EDA Report:</b> An extensive exploratory profiling HTML report has been generated using <code>ydata-profiling</code> "
    "and saved in <code>Reports/EDA_Report.html</code>, presenting interaction charts, missing cell correlations, and cardinality metrics.",
    body_style
))
story.append(PageBreak())

# =============================================================================
# 8. MODEL BUILDING (CODE)
# =============================================================================
story.append(Paragraph("8. Model Building (Code) (Unit-4)", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E0"), spaceAfter=8))
story.append(Paragraph(
    "Because the target variable (<code>price</code>) is continuous, a <b>Linear Regression</b> model was built as required by Unit-4. "
    "Categorical features (<code>transaction</code>, <code>furnishing</code>, <code>location</code>) were converted to numerical indicators "
    "using One-Hot Encoding (<code>pd.get_dummies</code> with <code>drop_first=True</code> to prevent multicollinearity).",
    body_style
))

code_text = (
    "# 1. Feature Matrix & Target Definition\n"
    "X = df_clean[['square_feet', 'transaction', 'furnishing', 'price_per_sqft', 'bhk', 'location']]\n"
    "y = df_clean['price']\n\n"
    "# 2. One-Hot Encoding\n"
    "X_encoded = pd.get_dummies(X, columns=['transaction', 'furnishing', 'location'], drop_first=True)\n\n"
    "# 3. Train-Test Split (80% Train, 20% Test)\n"
    "X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.20, random_state=42)\n\n"
    "# 4. Linear Regression Model Training\n"
    "linear_model = LinearRegression()\n"
    "linear_model.fit(X_train, y_train)\n\n"
    "# 5. Predictions on Test Set\n"
    "y_pred_linear = linear_model.predict(X_test)"
)
story.append(Paragraph(code_text.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))
story.append(Spacer(1, 10))

# =============================================================================
# 9. MODEL EVALUATION
# =============================================================================
story.append(Paragraph("9. Model Evaluation (Unit-3 & Unit-4)", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E0"), spaceAfter=8))
story.append(Paragraph(
    "The Linear Regression model was evaluated on the independent testing set (83 samples) using three core regression metrics:",
    body_style
))

eval_metrics = [
    [Paragraph("<b>Evaluation Metric</b>", body_style), Paragraph("<b>Formula / Definition</b>", body_style), Paragraph("<b>Obtained Value</b>", body_style)],
    [Paragraph("<b>R² (R-Squared)</b>", body_style), Paragraph("1 - (SS_res / SS_tot)", body_style), Paragraph("<b>0.8381 (83.81%)</b>", body_style)],
    [Paragraph("<b>Mean Squared Error (MSE)</b>", body_style), Paragraph("Average of squared differences between actual and predicted", body_style), Paragraph("11,192,419,167,903.97", body_style)],
    [Paragraph("<b>Root Mean Squared Error (RMSE)</b>", body_style), Paragraph("Square root of MSE (in INR units)", body_style), Paragraph("<b>Rs. 3,345,507.31</b>", body_style)]
]
t_eval = Table(eval_metrics, colWidths=[140, 200, 140])
t_eval.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
]))
story.append(t_eval)
story.append(Spacer(1, 8))

story.append(Paragraph("<b>Sample Predictions vs Actual Prices:</b>", h2_style))
sample_table_data = [
    [Paragraph("<b>Record #</b>", body_style), Paragraph("<b>Actual Price (INR)</b>", body_style), Paragraph("<b>Predicted Price (INR)</b>", body_style), Paragraph("<b>Absolute Error (INR)</b>", body_style)],
    [Paragraph("Sample 1", body_style), Paragraph("Rs. 3,500,000", body_style), Paragraph("Rs. 4,288,682", body_style), Paragraph("Rs. 788,682", body_style)],
    [Paragraph("Sample 2", body_style), Paragraph("Rs. 8,540,000", body_style), Paragraph("Rs. 9,265,976", body_style), Paragraph("Rs. 725,976", body_style)],
    [Paragraph("Sample 3", body_style), Paragraph("Rs. 8,200,000", body_style), Paragraph("Rs. 12,274,430", body_style), Paragraph("Rs. 4,074,430", body_style)],
    [Paragraph("Sample 4", body_style), Paragraph("Rs. 1,500,000", body_style), Paragraph("Rs. -3,449,655", body_style), Paragraph("Rs. 4,949,655", body_style)],
    [Paragraph("Sample 5", body_style), Paragraph("Rs. 16,600,000", body_style), Paragraph("Rs. 16,674,630", body_style), Paragraph("Rs. 74,630", body_style)]
]
t_sample = Table(sample_table_data, colWidths=[90, 130, 130, 130])
t_sample.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EDF2F7")),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
    ('TOPPADDING', (0,0), (-1,-1), 3),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
]))
story.append(t_sample)
story.append(Spacer(1, 10))

# =============================================================================
# 10. RESULTS & MODEL IMPROVEMENT
# =============================================================================
story.append(Paragraph("10. Results & Model Improvement (Unit-4)", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E0"), spaceAfter=8))
story.append(Paragraph(
    "To satisfy Unit-4 instructions regarding <b>Model Improvement</b>, two validation techniques were applied:",
    body_style
))
story.append(Paragraph("1. <b>5-Fold Cross Validation:</b> Verifies model stability across diverse folds (Fold scores: 0.8381, 0.8611, 0.4818, 0.7897, 0.7994; Mean R²: <b>0.7540</b>).", bullet_style))
story.append(Paragraph("2. <b>L2 Regularization (Ridge Regression):</b> Applied with α=1.0 to shrink coefficients and minimize overfitting.", bullet_style))
story.append(Spacer(1, 6))

comparison_table_data = [
    [Paragraph("<b>Model Name</b>", body_style), Paragraph("<b>Test R² Score</b>", body_style), Paragraph("<b>Test RMSE (INR)</b>", body_style), Paragraph("<b>Mean 5-Fold CV R²</b>", body_style), Paragraph("<b>Result</b>", body_style)],
    [Paragraph("Linear Regression (Baseline)", body_style), Paragraph("0.8381", body_style), Paragraph("Rs. 3,345,507.31", body_style), Paragraph("0.7540", body_style), Paragraph("Strong Baseline", body_style)],
    [Paragraph("Ridge Regression (Regularized)", body_style), Paragraph("<b>0.8439</b>", body_style), Paragraph("<b>Rs. 3,284,548.39</b>", body_style), Paragraph("<b>0.7548</b>", body_style), Paragraph("<b>Best Performing</b>", body_style)]
]
t_comp = Table(comparison_table_data, colWidths=[150, 75, 110, 85, 60])
t_comp.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#C6F6D5")),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
]))
story.append(t_comp)
story.append(Spacer(1, 10))

# =============================================================================
# 11. CONCLUSION & 12. FUTURE SCOPE
# =============================================================================
story.append(Paragraph("11. Conclusion", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E0"), spaceAfter=8))
story.append(Paragraph(
    "In this project, an end-to-end Machine Learning pipeline was successfully constructed to predict residential house prices. "
    "Through systematic preprocessing, 13 duplicate entries and 18 extreme outliers were handled using the IQR method. "
    "Linear Regression provided an R² score of 0.8381. Incorporating L2 Ridge regularization improved the R² score to <b>0.8439</b> "
    "and reduced RMSE to <b>Rs. 3,284,548.39</b>, confirming that penalizing large weights provides superior generalization. "
    "All syllabus and practical journal requirements for course 303 Machine Learning have been fully satisfied.",
    body_style
))
story.append(Spacer(1, 10))

story.append(Paragraph("12. Future Scope", h1_style))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E0"), spaceAfter=8))
scope_points = [
    "<b>Non-Linear Ensemble Models:</b> Evaluating ensemble algorithms such as Random Forest Regressor and XGBoost to capture complex non-linear price patterns.",
    "<b>Spatial & Geographic Features:</b> Integrating GIS coordinates (latitude and longitude) and proximity distances to civic infrastructure (schools, metros, hospitals).",
    "<b>Feature Scaling & Transformation:</b> Applying log transformation on prices and standard scaling on numerical inputs to manage skewed distributions.",
    "<b>Interactive Web Application:</b> Deploying the trained model with a Streamlit or Flask UI for instant property valuation by prospective buyers."
]
for pt in scope_points:
    story.append(Paragraph(f"• {pt}", bullet_style))

doc.build(story)
print(f"Project_Report.pdf generated successfully at: {PDF_PATH}")
