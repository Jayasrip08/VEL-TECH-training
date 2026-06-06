import pickle

# Load model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

print("Enter Patient Details")

glucose = float(input("Glucose: "))
blood_pressure = float(input("Blood Pressure: "))
bmi = float(input("BMI: "))
age = float(input("Age: "))

prediction = model.predict(
    [[glucose, blood_pressure, bmi, age]]
)

if prediction[0] == 1:
    print("\nPrediction: Diabetic")
else:
    print("\nPrediction: Not Diabetic")