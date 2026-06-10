# Day 10 — Final Model, Testing & Handoff
## M2 Model Development · Track 2 · InnoTrack 2025

---

## What Is Today About?

This is the last day of M2. Your model is trained, tuned, and tested. Today you
bring everything together into one clean, organised package that another developer
can pick up and plug straight into a Flask web app — without needing to ask you
a single question.

By end of day you will have:
- All your `.pkl` files named consistently and verified
- One clean `predict()` function that works on any input
- 10 test cases logged and passing
- A model summary card written in plain English
- Everything pushed to GitHub and submitted on InnoTrack

Think of today as the day you go from *"my model works on my laptop"* to
*"my model is ready for someone else to use"*.

---

## Task 1 — Consolidate and Name All Final `.pkl` Files

### What is a `.pkl` file and why does naming matter?

A `.pkl` file is a saved version of a Python object — your trained model, your
scaler, your encoder. When your Flask app runs, it loads these files and uses
them to make predictions. If the files have inconsistent names like
`model_v3_final_FINAL.pkl` or `enc2.pkl`, the Flask developer will have no idea
what each file does.

Today you give every file a clear, consistent name so anyone can understand
what it contains just by reading the filename.

### Standard naming convention

| File | What it contains |
|---|---|
| `final_model.pkl` | Your trained, tuned model |
| `label_encoder.pkl` | LabelEncoder fitted on your training data |
| `scaler.pkl` | StandardScaler fitted on your training data |
| `tfidf_vectorizer.pkl` | TF-IDF vectorizer (Shaik only) |
| `similarity_matrix.pkl` | Cosine similarity matrix (Mithun only) |
| `movies_list.pkl` | Movies DataFrame (Mithun only) |

### How to save with the correct name

```python
import joblib

# Save your final tuned model
joblib.dump(grid.best_estimator_, 'final_model.pkl')

# Save your scaler (if you used one)
joblib.dump(scaler, 'scaler.pkl')

# Save your encoder (if you used one)
joblib.dump(label_encoder, 'label_encoder.pkl')

print("All files saved.")
```

### Verify every file loads correctly

Open a brand new notebook cell — do not reuse variables from earlier cells.
Load every file from scratch and confirm it works:

```python
import joblib

# Load each file fresh — as if you are the Flask developer
model   = joblib.load('final_model.pkl')
scaler  = joblib.load('scaler.pkl')       # remove this line if you did not use a scaler
encoder = joblib.load('label_encoder.pkl') # remove this line if you did not use an encoder

# Quick sanity check — make one prediction to confirm the model loaded correctly
import numpy as np
test_input = np.array([[120, 33.6, 50, 1]])  # replace with valid values for your project
print("Load test passed. Sample prediction:", model.predict(test_input))
```

If this cell runs without errors, your files are ready.

### Write a handoff checklist in a markdown cell

In your notebook, add a markdown cell that lists every file the Flask developer
will need. This is the most important thing you will write today — it tells
the M3 team exactly what to load and in what order.

**Example for Bhaskhar — Diabetes Predictor:**

```
## Files required for prediction

| File | Purpose |
|---|---|
| final_model.pkl | Trained Random Forest classifier |
| scaler.pkl | StandardScaler fitted on training features |

## Input columns (in this exact order)
Pregnancies, Glucose, BloodPressure, SkinThickness,
Insulin, BMI, DiabetesPedigreeFunction, Age

## Output
{ "prediction": "Diabetic" or "Not Diabetic", "confidence": "84.7%" }
```

---

## Task 2 — Write and Test a Single `predict(inputs)` Function

### What is this function and why does it matter?

This is the single most important piece of code you write in M2. The Flask
developer will copy this function directly into their app. When a user fills
in your web form and clicks Submit, Flask will call this function, and whatever
it returns will be shown on screen.

If this function is messy, crashes on unexpected inputs, or requires the Flask
developer to guess what order to preprocess things in — your M3 integration
will fail. Write it cleanly.

### The structure every student must follow

```python
import joblib
import pandas as pd

def predict(inputs: dict) -> dict:
    """
    Takes a raw input dictionary (exactly what the Flask form will send)
    and returns a dictionary with the prediction and confidence.

    Parameters
    ----------
    inputs : dict
        Raw values from the user, e.g.
        {'Glucose': 148, 'BMI': 33.6, 'Age': 50, ...}

    Returns
    -------
    dict
        e.g. {'prediction': 'Diabetic', 'confidence': '84.7%'}
    """

    # Step 1 — Load all required .pkl files
    model  = joblib.load('final_model.pkl')
    scaler = joblib.load('scaler.pkl')   # remove if not used

    # Step 2 — Convert the input dict into a DataFrame
    # This preserves column names so the model knows which value is which
    input_df = pd.DataFrame([inputs])

    # Step 3 — Apply preprocessing in the EXACT same order as training
    input_df = scaler.transform(input_df)   # remove if not used

    # Step 4 — Make the prediction
    prediction   = model.predict(input_df)[0]
    probabilities = model.predict_proba(input_df)[0]

    # Step 5 — Return a clean, human-readable dict
    class_labels = {0: 'Not Diabetic', 1: 'Diabetic'}  # change to your labels
    return {
        'prediction': class_labels[prediction],
        'confidence': f"{max(probabilities) * 100:.1f}%"
    }
```

### Things to include based on your project

Add any extra outputs from Day 9 into the return dict:

```python
# If you built a top-3 feature explanation on Day 9, add it here
return {
    'prediction':  class_labels[prediction],
    'confidence':  f"{max(probabilities) * 100:.1f}%",
    'top_features': ['Glucose', 'BMI', 'Age'],   # from your Day 9 explain function
    'risk_level':  'High'                         # if your project has risk categories
}
```

### Test the function with one quick call

```python
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

result = predict(sample)
print(result)
# Expected: {'prediction': 'Diabetic', 'confidence': '84.7%'}
```

---

## Task 3 — Run 10 Test Cases Through `predict()` and Log Results

### Why 10 test cases?

One test proves your function works once. Ten tests prove it works reliably
across different kinds of inputs — normal, extreme, borderline, and even broken.
This is especially important because Flask will pass whatever the user types into
your form, and users will type unexpected things.

### The 10 cases you must run

| # | Type | What to test | What you expect |
|---|---|---|---|
| 1 | Normal case | Typical healthy values | Low risk / negative prediction |
| 2 | Normal case | Another typical healthy set | Low risk / negative prediction |
| 3 | Normal case | Average values across all features | Medium or low prediction |
| 4 | High-risk | All danger values pushed to extremes | High risk / positive prediction |
| 5 | High-risk | Another extreme combination | High risk / positive prediction |
| 6 | Edge case | All values at their minimum valid value | Should not crash |
| 7 | Edge case | All values at their maximum valid value | Should not crash |
| 8 | Known test row | Copy one row from X_test where y_test = 0 | Must return the correct label |
| 9 | Known test row | Copy one row from X_test where y_test = 1 | Must return the correct label |
| 10 | Invalid input | A negative age, or a missing field | Must return a readable error message |

### How to run and log all 10 in a table

```python
import pandas as pd

# Define your 10 test cases as a list of dicts
test_cases = [
    # Case 1 — Normal / low risk
    {'Pregnancies': 1, 'Glucose': 89,  'BloodPressure': 66,
     'SkinThickness': 23, 'Insulin': 94,  'BMI': 28.1,
     'DiabetesPedigreeFunction': 0.167, 'Age': 21},

    # Case 2 — Normal
    {'Pregnancies': 0, 'Glucose': 95,  'BloodPressure': 60,
     'SkinThickness': 18, 'Insulin': 58,  'BMI': 22.5,
     'DiabetesPedigreeFunction': 0.112, 'Age': 24},

    # Case 3 — Normal / average
    {'Pregnancies': 3, 'Glucose': 110, 'BloodPressure': 70,
     'SkinThickness': 25, 'Insulin': 80,  'BMI': 27.0,
     'DiabetesPedigreeFunction': 0.300, 'Age': 30},

    # Case 4 — High risk
    {'Pregnancies': 8, 'Glucose': 183, 'BloodPressure': 64,
     'SkinThickness': 0,  'Insulin': 0,   'BMI': 23.3,
     'DiabetesPedigreeFunction': 0.672, 'Age': 32},

    # Case 5 — High risk
    {'Pregnancies': 10,'Glucose': 199, 'BloodPressure': 90,
     'SkinThickness': 50, 'Insulin': 200, 'BMI': 45.0,
     'DiabetesPedigreeFunction': 2.1,   'Age': 63},

    # Case 6 — Edge: minimum values
    {'Pregnancies': 0, 'Glucose': 44,  'BloodPressure': 24,
     'SkinThickness': 7,  'Insulin': 14,  'BMI': 18.2,
     'DiabetesPedigreeFunction': 0.078, 'Age': 21},

    # Case 7 — Edge: maximum values
    {'Pregnancies': 17,'Glucose': 199, 'BloodPressure': 122,
     'SkinThickness': 99, 'Insulin': 846, 'BMI': 67.1,
     'DiabetesPedigreeFunction': 2.42,  'Age': 81},

    # Case 8 — Known test row (y_test = 0, not diabetic)
    # Replace these with actual values from your X_test where y_test = 0
    {'Pregnancies': 1, 'Glucose': 103, 'BloodPressure': 30,
     'SkinThickness': 38, 'Insulin': 83,  'BMI': 43.3,
     'DiabetesPedigreeFunction': 0.183, 'Age': 33},

    # Case 9 — Known test row (y_test = 1, diabetic)
    # Replace these with actual values from your X_test where y_test = 1
    {'Pregnancies': 2, 'Glucose': 155, 'BloodPressure': 52,
     'SkinThickness': 27, 'Insulin': 540, 'BMI': 38.7,
     'DiabetesPedigreeFunction': 0.240, 'Age': 25},

    # Case 10 — Invalid input (should NOT crash — must return error message)
    {'Pregnancies': -1, 'Glucose': -999, 'BloodPressure': 70,
     'SkinThickness': 25, 'Insulin': 80,  'BMI': 27.0,
     'DiabetesPedigreeFunction': 0.3,   'Age': -5},
]

# Add try/except to your predict() function before running this
def predict_safe(inputs):
    try:
        return predict(inputs)
    except Exception as e:
        return {'prediction': 'Error', 'confidence': 'N/A', 'error': str(e)}

# Run all 10 and log results
results = []
for i, case in enumerate(test_cases, 1):
    result = predict_safe(case)
    results.append({
        'Case': i,
        'Prediction': result.get('prediction', 'Error'),
        'Confidence': result.get('confidence', 'N/A'),
        'Status': 'PASS' if result.get('prediction') != 'Error' else 'ERROR'
    })

log_df = pd.DataFrame(results)
print(log_df.to_string(index=False))
```

**Your output should look like this:**

```
 Case   Prediction  Confidence  Status
    1 Not Diabetic       91.3%    PASS
    2 Not Diabetic       95.0%    PASS
    3 Not Diabetic       74.2%    PASS
    4     Diabetic       87.6%    PASS
    5     Diabetic       98.1%    PASS
    6 Not Diabetic       88.5%    PASS
    7     Diabetic       79.3%    PASS
    8 Not Diabetic       82.1%    PASS
    9     Diabetic       91.7%    PASS
   10        Error         N/A   ERROR
```

Case 10 showing ERROR is correct — that means your `try/except` caught the bad
input and returned a readable message instead of crashing Python.

---

## Task 4 — Write the Model Summary Card

### What is a model summary card?

It is a single markdown cell at the bottom of your notebook that documents
everything about your final model in plain English. The Flask integration team
reads this before touching any of your code. It tells them exactly what inputs
the model expects, what files to load, and what the output looks like.

Think of it as the instruction manual for your model.

### The template — copy this into a markdown cell in your notebook

````
## Model Summary Card

### Project
<!-- Your project name and domain -->
Diabetes Risk Predictor · Healthcare

### Algorithm
Random Forest Classifier (tuned with GridSearchCV)

### Dataset
PIMA Indians Diabetes Dataset · 768 rows · 8 features

### Final Performance
| Metric | Score |
|---|---|
| Accuracy | 79.2% |
| F1-Score (weighted) | 0.787 |
| Cross-validation mean | 0.774 ± 0.031 |

### Input Features (in this exact order)
| Column | Type | Example value |
|---|---|---|
| Pregnancies | int | 2 |
| Glucose | float | 148.0 |
| BloodPressure | float | 72.0 |
| SkinThickness | float | 35.0 |
| Insulin | float | 0.0 |
| BMI | float | 33.6 |
| DiabetesPedigreeFunction | float | 0.627 |
| Age | int | 50 |

### Required .pkl Files
| File | Contents |
|---|---|
| final_model.pkl | Trained Random Forest (n_estimators=200, max_depth=10) |
| scaler.pkl | StandardScaler fitted on X_train |

### Sample Input
```python
{
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

### Sample Output
```python
{
    'prediction': 'Diabetic',
    'confidence': '84.7%',
    'top_features': ['Glucose', 'BMI', 'Age']
}
```

### How to use
```python
import joblib
result = predict(your_input_dict)
```
````

Fill in every section with your own project's real values. Do not leave any
section blank — every field in this card is something the Flask developer
will need.

---

## Task 5 — Push All Files to GitHub and Submit InnoTrack Report

### Folder structure to push

Your GitHub repository must have this structure by end of day:

```
your-repo/
│
├── M2_model_development.ipynb   ← your full Day 6-10 notebook
│
├── models/
│   ├── final_model.pkl
│   ├── scaler.pkl               ← if used
│   ├── label_encoder.pkl        ← if used
│   └── tfidf_vectorizer.pkl     ← if used (Shaik only)
│
├── charts/
│   ├── feature_importance.png
│   ├── confusion_matrix.png     ← or residual_plot.png for regressors
│   └── validation_curve.png
│
└── comparison.csv               ← your Day 7 model comparison table
```

### Git commands to push everything

```bash
# Navigate to your project folder
cd your-project-folder

# Stage all new and changed files
git add .

# Commit with a clear message
git commit -m "M2 complete: final model, predict function, test cases, summary card"

# Push to GitHub
git push origin main
```

### Verify your repo on GitHub

After pushing, open your GitHub repo in a browser and confirm:

- `M2_model_development.ipynb` is present and visible
- `models/` folder exists and contains all `.pkl` files
- `charts/` folder contains all PNG charts
- `comparison.csv` is present

If any file is missing, add it and push again before submitting.

### Submit on InnoTrack

Your InnoTrack submission must include:

1. Your GitHub repository link
2. A screenshot of your final model's metric score (from the notebook output)
3. A screenshot of your comparison table (from `comparison.csv` or the notebook)

---

## End-of-Day Checklist

This is the final checklist for the entire M2 track. Every item must be
complete before you leave today.

- [ ] All `.pkl` files renamed consistently and saved in `models/` folder
- [ ] Every `.pkl` file loads without errors in a fresh notebook cell
- [ ] Handoff checklist markdown cell written in notebook
- [ ] `predict(inputs: dict) -> dict` function written and tested
- [ ] Function returns a human-readable dict with label + confidence
- [ ] All 10 test cases run — 9 pass, case 10 returns error message (not crash)
- [ ] Results logged in a printed table
- [ ] Model summary card markdown cell complete with all 7 sections filled in
- [ ] GitHub repo pushed with correct folder structure
- [ ] InnoTrack report submitted with GitHub link + screenshots

---

## The Final Mentor Test

Your mentor will do the following to verify you are M3-ready:

```python
# Mentor opens a fresh Python session and runs:
import joblib
import pandas as pd

# Loads your predict function from your notebook
# Calls it with a made-up input

result = predict({
    'Pregnancies': 3,
    'Glucose': 130,
    'BloodPressure': 70,
    'SkinThickness': 28,
    'Insulin': 100,
    'BMI': 31.5,
    'DiabetesPedigreeFunction': 0.45,
    'Age': 38
})

print(result)
```

**If this prints a clean dict with a readable prediction in under 3 seconds,
you pass. You are M3-ready.**

If it crashes, raises a FileNotFoundError, or returns a raw class index — go
back and fix your `predict()` function before submitting.

---

## Common Mistakes to Avoid

**Using different variable names across cells**
Your `predict()` function must be self-contained. It must load its own `.pkl`
files internally — do not rely on variables that were defined in earlier cells.

**Forgetting to include preprocessing inside predict()**
If your model was trained on scaled data, every call to `predict()` must also
scale the input. Forgetting this gives wrong predictions silently — the
function will not crash, it will just return garbage.

**Pushing notebooks with errors in cells**
Before pushing to GitHub, go to Kernel → Restart & Run All in Jupyter and
confirm every cell runs clean from top to bottom. A notebook with red error
cells will confuse the Flask developer.

**Not testing the invalid input case**
Flask users will type anything — negative numbers, blank fields, letters where
numbers are expected. If your `predict()` has no `try/except`, the Flask app
will crash with a 500 error every time someone enters bad data.

---

## What Happens After Today

| Track | What they take from you | What they build |
|---|---|---|
| M3 Flask | Your `predict()` function + all `.pkl` files + model summary card | The web form and result page |
| M4 Deploy | M3's finished Flask app | Live URL on Render |

Your M2 output is the foundation everything else is built on. A clean handoff
today means a smooth M3 and M4 for your project.

---

*InnoTrack 2025 · Track 2 Advanced ML · M2 Model Development · Day 10*