import joblib

model = joblib.load("models/diabetes_model.pkl")

print(model.n_features_in_)

if hasattr(model, "feature_names_in_"):
    print(model.feature_names_in_)