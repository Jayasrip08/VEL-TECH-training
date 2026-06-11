import joblib

model = joblib.load(
    "models/model.pkl"
)

sample = [[
    180,
    95,
    34,
    55
]]

prediction = model.predict(sample)

probability = model.predict_proba(sample)

print("Prediction:", prediction)

print("Probability:", probability)