# Day 9 — Advanced Techniques
## M2 Model Development · Track 2 · InnoTrack 2025

---

## What Is Today About?

By Day 8 you have a trained and tuned model. It works. It gives predictions.
But right now it is a **black box** — you feed it numbers and it spits out an answer, and you have no idea *why* it made that decision.

Day 9 fixes that. You will:
- Find out **which features your model actually cares about**
- Fix any **data imbalance** problems that are silently hurting your model
- Make your model's decisions **explainable** (show *why* it predicted what it did)
- Make your output **human-readable** (not just "1" or "0.73" — real sentences)
- **Test it with real-world inputs** from scratch to prove it all works

Think of Day 9 as the day you go from *"my model runs"* to *"my model is ready to show someone"*.

---

## Task 1 — Feature Importance Analysis

### What does "feature importance" mean?

When your model was trained, it learned that some input columns matter a lot and some barely matter at all. Feature importance tells you **which columns the model relied on most** when making decisions.

For example, in a diabetes predictor:
- Glucose level might matter a lot → high importance
- Skin thickness might barely matter → low importance

This is useful because:
- It tells you if the model is making sensible decisions
- It helps you spot if something weird is happening (e.g. a patient ID column accidentally influencing predictions)
- It gives you something visual to show in your demo

### How to do it

Most tree-based models (Random Forest, Gradient Boosting, XGBoost, Decision Tree) give you feature importances directly:

```python
import pandas as pd
import matplotlib.pyplot as plt

# Get importances from your trained model
importances = model.feature_importances_

# Pair each importance score with its column name
feature_names = X_train.columns  # or whatever your column list is
importance_df = pd.DataFrame({
    'Feature': feature_names,
    'Importance': importances
})

# Sort from most important to least
importance_df = importance_df.sort_values('Importance', ascending=True)

# Plot as a horizontal bar chart
plt.figure(figsize=(8, 6))
plt.barh(importance_df['Feature'], importance_df['Importance'])
plt.xlabel('Importance Score')
plt.title('Top Features — What the Model Cares About')
plt.tight_layout()
plt.savefig('feature_importance.png')
plt.show()
```

### What if I use SVM or Ridge Regression?

SVM and Ridge do not have `feature_importances_` but they have coefficients:

```python
# For Ridge Regression (Akshara)
import numpy as np

coef_df = pd.DataFrame({
    'Feature': X_train.columns,
    'Coefficient': np.abs(model.coef_)  # abs() because negative = also important
})
coef_df = coef_df.sort_values('Coefficient', ascending=True)
```

### What if I use TF-IDF + Naive Bayes (Shaik)?

```python
# Get top words by their weight in the vectorizer
feature_names = vectorizer.get_feature_names_out()
top_indices = model.feature_log_prob_[1].argsort()[-15:]  # top 15 words
top_words = feature_names[top_indices]
print("Top words for positive sentiment:", top_words)
```

### What to save
Save the chart as `feature_importance.png`. You will use it in your M4 demo slides.

---

## Task 2 — Handle Class Imbalance

### What is class imbalance? Why does it matter?

Imagine you are building a **fraud detector**. In real data, maybe only 1 transaction in every 100 is fraud. So your dataset looks like this:

- 99,000 rows → Genuine
- 1,000 rows → Fraud

If you train a model on this, the model quickly learns a dirty trick: **always predict Genuine**. It will be 99% accurate and never catch a single fraud case. That is useless.

This is called **class imbalance** — one class has way more rows than the other — and it silently wrecks your model without you realising it.

### How to check if you have this problem

```python
print(y_train.value_counts())
print(y_train.value_counts(normalize=True))  # shows percentages
```

If one class is less than 10% of the total, you have a significant imbalance.

### The fix — SMOTE

SMOTE stands for **Synthetic Minority Over-sampling Technique**. It creates artificial new rows for the minority class by interpolating between existing minority rows. It does NOT just copy rows — it generates realistic synthetic samples.

**Install if needed:**
```
pip install imbalanced-learn
```

**Apply SMOTE:**
```python
from imblearn.over_sampling import SMOTE

smote = SMOTE(random_state=42)

# Apply only on training data — never on test data
X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)

print("Before SMOTE:", y_train.value_counts().to_dict())
print("After SMOTE: ", pd.Series(y_train_balanced).value_counts().to_dict())
```

After SMOTE, re-train your model using `X_train_balanced` and `y_train_balanced` instead of the originals. Then compare precision and recall before vs after.

### Who needs to do SMOTE today?

| Student | Why |
|---|---|
| S. Supradeel | Fraud dataset — ~0.17% fraud, massive imbalance |
| Rithin Sai | Outbreak dataset — Critical risk class is rare |

**Everyone else:** Just run `y_train.value_counts()` and print it. If your ratio is less than 10:1 you are fine and can move on.

### Alternative fix — class_weight

Some models accept `class_weight='balanced'` directly. This is simpler than SMOTE:

```python
model = GradientBoostingClassifier(random_state=42)
# For sklearn models that support it, pass sample_weight during fit
```

| Student | Action |
|---|---|
| T. Naga Lakshmi Priya | Pass `scale_pos_weight` to XGBClassifier |
| Reashma R | Gradient Boosting does not support class_weight directly — use SMOTE or oversample manually |

---

## Task 3 — Model Explainability

### Why does explainability matter?

Right now your model says "this person has high churn risk" or "this patient is diabetic". But *why*? Which inputs pushed it toward that decision?

Explainability gives your model a voice. Instead of just a prediction, it can say:
> "I predicted High Churn Risk because: contract type is Month-to-Month (most important), tenure is only 2 months (second), and no tech support (third)."

This is what your M3 Flask app will eventually show users — not just the answer, but the reasoning.

### Option A — SHAP (for Naga Lakshmi Priya — XGBoost + SHAP project)

SHAP is the gold standard for explainability. It assigns each feature a score for each individual prediction — positive score means it pushed toward the positive class, negative means it pushed away.

**Install:**
```
pip install shap
```

**Use:**
```python
import shap

# Create explainer using your trained XGBoost model
explainer = shap.TreeExplainer(model)

# Calculate SHAP values for test set
shap_values = explainer.shap_values(X_test)

# Summary plot — shows feature importances across all test samples
shap.summary_plot(shap_values, X_test, feature_names=X_test.columns)

# Force plot — explains one individual prediction
shap.initjs()
shap.force_plot(
    explainer.expected_value[0],
    shap_values[0][0],   # first test sample, class 0
    X_test.iloc[0],
    feature_names=X_test.columns
)
```

The summary plot shows you which features matter overall. The force plot shows you exactly why the model made a specific decision for one person.

### Option B — Top 3 features per prediction (everyone else)

For all other projects, write a simple function that takes one prediction and returns the 3 features that contributed most to it. This is a lightweight alternative to SHAP:

```python
def explain_prediction(sample_input, model, feature_names):
    """
    Takes one input sample and returns the top 3 most important features
    that influenced the prediction.

    sample_input : a single row as a numpy array or list
    model        : your trained model
    feature_names: list of column names
    """
    # Get feature importances from the model
    importances = model.feature_importances_

    # Pair each feature name with how much the model relies on it globally
    feature_scores = list(zip(feature_names, importances))

    # Sort by importance, highest first
    feature_scores.sort(key=lambda x: x[1], reverse=True)

    # Return the top 3
    top_3 = feature_scores[:3]

    print("Top 3 features influencing this prediction:")
    for i, (name, score) in enumerate(top_3, 1):
        print(f"  {i}. {name}  (importance score: {score:.4f})")

    return top_3

# Test it
explain_prediction(X_test.iloc[0], model, X_train.columns)
```

### Option C — Backtesting (Paul Surya — Stock Market Classifier)

For a stock trend predictor, explainability means: does the model actually make money if you follow its signals? This is called backtesting.

```python
# Predict on the held-out test period
y_pred = model.predict(X_test)

# Hit rate = % of predictions that were correct
correct = (y_pred == y_test).sum()
total = len(y_test)
hit_rate = correct / total * 100

print(f"Backtest hit rate: {hit_rate:.1f}%")
print(f"Correct Up/Down calls: {correct} out of {total}")

# Show month-by-month
results = pd.DataFrame({
    'Date': X_test.index,
    'Actual': y_test.values,
    'Predicted': y_pred,
    'Correct': (y_pred == y_test.values)
})
print(results.tail(20))
```

### Option D — Anomaly timeline chart (S. Shalini — Heart Rate Detector)

For anomaly detection, the most useful "explanation" is a visual timeline showing where the anomalies appeared in the signal:

```python
import matplotlib.pyplot as plt

# Assuming you have a time index and predictions (-1 = anomaly, 1 = normal)
anomaly_mask = (y_pred == -1)

plt.figure(figsize=(14, 4))
plt.plot(heart_rate_values, color='steelblue', label='Heart Rate', linewidth=0.8)
plt.scatter(
    x=anomaly_indices[anomaly_mask],
    y=heart_rate_values[anomaly_mask],
    color='red', s=20, label='Anomaly', zorder=5
)
plt.title('Heart Rate Signal with Detected Anomalies')
plt.xlabel('Time')
plt.ylabel('Heart Rate')
plt.legend()
plt.tight_layout()
plt.savefig('anomaly_timeline.png')
plt.show()
```

---

## Task 4 — Domain-Specific Output Enrichment

### What does "output enrichment" mean?

Right now your model outputs something like `1` or `0.73` or `"Class_2"`. That means nothing to a real user. Output enrichment means **translating the raw model output into something a human actually understands**.

This is the exact output your Flask app will display on screen in M3. Build it here in Python first, before any web development happens.

### Examples by project:

**V. Yuvaraju — AQI Predictor**
Your regressor outputs a number. Map it to a category and advice:

```python
def enrich_aqi(aqi_score):
    if aqi_score <= 50:
        return {'score': aqi_score, 'category': 'Good', 'colour': 'green',
                'advice': 'Air quality is satisfactory. Enjoy outdoor activities.'}
    elif aqi_score <= 100:
        return {'score': aqi_score, 'category': 'Moderate', 'colour': 'yellow',
                'advice': 'Sensitive groups should limit prolonged outdoor exertion.'}
    elif aqi_score <= 150:
        return {'score': aqi_score, 'category': 'Unhealthy for Sensitive Groups', 'colour': 'orange',
                'advice': 'People with heart or lung disease should reduce outdoor activity.'}
    elif aqi_score <= 200:
        return {'score': aqi_score, 'category': 'Unhealthy', 'colour': 'red',
                'advice': 'Everyone should limit outdoor exertion.'}
    else:
        return {'score': aqi_score, 'category': 'Hazardous', 'colour': 'maroon',
                'advice': 'Avoid all outdoor activity. Keep windows closed.'}
```

**R. Tarun — Crop Recommendation**
Your model outputs class probabilities. Return the top 3 crops with confidence:

```python
def enrich_crop(model, input_array, crop_labels):
    probabilities = model.predict_proba(input_array)[0]
    top_3_indices = probabilities.argsort()[-3:][::-1]
    results = []
    for idx in top_3_indices:
        results.append({
            'crop': crop_labels[idx],
            'confidence': f"{probabilities[idx] * 100:.1f}%"
        })
    return results
```

**Nareddy Shanmukha Nihal Reddy — Customer Churn**
Convert raw probability to percentage + risk label + retention tips:

```python
def enrich_churn(probability):
    churn_pct = probability * 100
    if churn_pct >= 75:
        risk = 'High Risk'
        tips = ['Offer a loyalty discount immediately',
                'Assign a dedicated account manager',
                'Provide a free service upgrade for 3 months']
    elif churn_pct >= 40:
        risk = 'Medium Risk'
        tips = ['Send a personalised re-engagement email',
                'Offer a one-time discount on renewal',
                'Check in with a customer satisfaction call']
    else:
        risk = 'Low Risk'
        tips = ['Continue regular engagement emails',
                'Invite to loyalty rewards programme',
                'Ask for a review or referral']
    return {'churn_probability': f"{churn_pct:.1f}%", 'risk_level': risk, 'tips': tips}
```

**S. Akshara — Student Grade Predictor**
Map predicted grade to improvement tips based on which input features were weakest:

```python
def enrich_grade(predicted_score, input_features):
    tips = []
    if input_features['study_time'] < 2:
        tips.append("Increase daily study time to at least 2 hours")
    if input_features['absences'] > 5:
        tips.append("Reduce absences — attendance strongly correlates with grades")
    if input_features['failures'] > 0:
        tips.append("Seek extra help from teachers for previously failed subjects")
    if not tips:
        tips.append("Keep up the good work and maintain current habits")

    grade_label = 'Distinction' if predicted_score >= 16 else \
                  'Merit' if predicted_score >= 12 else \
                  'Pass' if predicted_score >= 10 else 'Needs Improvement'

    return {'predicted_score': predicted_score, 'grade': grade_label, 'tips': tips[:3]}
```

**Everyone else:** Write a function that at minimum:
1. Converts a class index to a readable label (e.g. `0 → "Not Diabetic"`, `1 → "Diabetic"`)
2. Converts a raw probability to a percentage string (e.g. `0.847 → "84.7% confidence"`)
3. Returns a Python dict — not just a print statement

```python
# Minimum output enrichment for everyone
def format_prediction(y_pred, y_proba, class_labels):
    label = class_labels[y_pred]
    confidence = f"{max(y_proba) * 100:.1f}%"
    return {
        'prediction': label,
        'confidence': confidence
    }
```

---

## Task 5 — Run 5 Real-World Sample Inputs End-to-End

### What does "end-to-end" mean?

It means: start from a raw dictionary of values (exactly what a user would type into a form), run it through your entire pipeline — preprocessing, model, output enrichment — and print a clean result.

This is the most important test of the week. If this works, your M3 Flask integration will be smooth. If this breaks, you have a bug somewhere in your pipeline.

### How to construct a sample input

Do NOT use rows from your test set. Make up realistic values based on your domain. Think: what would a real user actually enter?

```python
# Example for Bhaskhar — Diabetes predictor
sample = {
    'Pregnancies': 2,
    'Glucose': 148,
    'BloodPressure': 72,
    'SkinThickness': 35,
    'Insulin': 0,
    'BMI': 33.6,
    'DiabetesPedigreeFunction': 0.627,
    'Age': 50
}
```

### Write the full pipeline test

```python
import joblib
import numpy as np
import pandas as pd

def run_full_prediction(raw_input: dict):
    """
    Takes a raw input dict (as if typed by a user),
    runs it through the full pipeline,
    and returns a human-readable result dict.
    """
    # Step 1 — Load model and any transformers
    model  = joblib.load('tuned_model.pkl')
    # scaler = joblib.load('scaler.pkl')  ← uncomment if you used scaling

    # Step 2 — Convert dict to a DataFrame (preserves column names)
    input_df = pd.DataFrame([raw_input])

    # Step 3 — Apply the same preprocessing as training
    # input_df = scaler.transform(input_df)  ← uncomment if you used scaling

    # Step 4 — Predict
    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0] if hasattr(model, 'predict_proba') else None

    # Step 5 — Enrich output (use your Task 4 function here)
    class_labels = {0: 'Not Diabetic', 1: 'Diabetic'}   # change to your labels
    result = {
        'prediction': class_labels[prediction],
        'confidence': f"{max(probability) * 100:.1f}%" if probability is not None else 'N/A'
    }

    return result
```

### Test it with 5 different samples

Create 5 sample dicts — make them varied and realistic:

```python
samples = [
    # Case 1 — Normal / low risk
    {'Pregnancies': 1, 'Glucose': 89, 'BloodPressure': 66, 'SkinThickness': 23,
     'Insulin': 94, 'BMI': 28.1, 'DiabetesPedigreeFunction': 0.167, 'Age': 21},

    # Case 2 — High risk
    {'Pregnancies': 8, 'Glucose': 183, 'BloodPressure': 64, 'SkinThickness': 0,
     'Insulin': 0, 'BMI': 23.3, 'DiabetesPedigreeFunction': 0.672, 'Age': 32},

    # Case 3 — Borderline
    {'Pregnancies': 2, 'Glucose': 120, 'BloodPressure': 70, 'SkinThickness': 30,
     'Insulin': 85, 'BMI': 30.0, 'DiabetesPedigreeFunction': 0.400, 'Age': 35},

    # Case 4 — Young, low glucose
    {'Pregnancies': 0, 'Glucose': 95, 'BloodPressure': 60, 'SkinThickness': 18,
     'Insulin': 58, 'BMI': 22.5, 'DiabetesPedigreeFunction': 0.112, 'Age': 24},

    # Case 5 — Extreme / boundary values
    {'Pregnancies': 15, 'Glucose': 199, 'BloodPressure': 90, 'SkinThickness': 50,
     'Insulin': 200, 'BMI': 45.0, 'DiabetesPedigreeFunction': 2.1, 'Age': 63},
]

# Run all 5
print(f"{'Sample':<10} {'Prediction':<20} {'Confidence'}")
print("-" * 45)
for i, sample in enumerate(samples, 1):
    result = run_full_prediction(sample)
    print(f"Sample {i:<4} {result['prediction']:<20} {result['confidence']}")
```

**Your output should look something like this:**
```
Sample     Prediction           Confidence
---------------------------------------------
Sample 1   Not Diabetic         91.3%
Sample 2   Diabetic             87.6%
Sample 3   Not Diabetic         54.2%
Sample 4   Not Diabetic         95.0%
Sample 5   Diabetic             98.1%
```

**Save your 5 sample inputs as a list** — you will use these same samples in your Day 10 final testing session.

---

## End-of-Day Checklist

Before you leave today, confirm every item:

- [ ] Feature importance chart saved as `feature_importance.png`
- [ ] Class distribution printed — SMOTE applied if imbalance > 10:1
- [ ] Before/after precision & recall comparison printed (SMOTE projects only)
- [ ] Explainability output working — SHAP summary plot, top-3 function, backtest, or anomaly chart depending on project
- [ ] `format_prediction()` or equivalent enrichment function returns a human-readable dict
- [ ] `run_full_prediction()` tested with 5 sample inputs — no crashes
- [ ] All 5 outputs print cleanly in a table
- [ ] Sample input list saved in the notebook for Day 10

---

## Common Mistakes to Avoid

**Applying SMOTE to the test set**
SMOTE must only be applied to `X_train` and `y_train`. Never touch the test set. Your test set must remain the original, unmodified data so your accuracy score is realistic.

**Using test set rows as "sample inputs" in Task 5**
Your 5 sample inputs must be made up by you, not copied from the dataset. The whole point is to simulate a real user typing values into a form.

**Returning a number instead of a label**
`prediction: 1` is meaningless to a non-technical user. `prediction: "Diabetic"` is clear. Always convert class indices to readable strings in your output enrichment function.

**Forgetting to load preprocessors in run_full_prediction()**
If your model was trained on scaled data, every prediction must also be scaled. If your training used a LabelEncoder, every new input must go through the same encoder. Missing this step is the single most common reason Flask apps crash in M3.

---

## Summary — What You Built Today

| Task | What you did | Output |
|---|---|---|
| Task 1 | Found which features your model relies on | `feature_importance.png` |
| Task 2 | Fixed class imbalance so model is fair | Balanced training data, improved recall |
| Task 3 | Made predictions explainable | SHAP plots / top-3 function / backtest |
| Task 4 | Translated raw output to human language | Enriched result dict per project |
| Task 5 | Tested full pipeline with real inputs | 5 clean predictions printed in a table |

Tomorrow on Day 10 you bring everything together — final model, clean `predict()` function, GitHub push, and full M3 handoff.

---

*InnoTrack 2025 · Track 2 Advanced ML · M2 Model Development*