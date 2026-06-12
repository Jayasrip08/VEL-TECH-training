import joblib

model = joblib.load("model/model.pkl")

print("Model Type:", type(model))
print("Features Expected:", model.n_features_in_)

if hasattr(model, "feature_names_in_"):
    print("Feature Names:")
    print(model.feature_names_in_)