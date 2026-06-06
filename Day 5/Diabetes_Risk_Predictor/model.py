import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data/diabetes.csv')

# Chart 1
plt.figure(figsize=(6,4))
df['Outcome'].value_counts().plot(kind='bar')
plt.title('Diabetes Distribution')
plt.xlabel('Outcome')
plt.ylabel('Count')
plt.savefig('chart1.png')
plt.close()

# Chart 2
plt.figure(figsize=(6,4))
plt.hist(df['Glucose'], bins=20)
plt.title('Glucose Distribution')
plt.xlabel('Glucose')
plt.ylabel('Frequency')
plt.savefig('chart2.png')
plt.close()

# Chart 3
plt.figure(figsize=(6,4))
plt.scatter(df['Age'], df['BMI'])
plt.title('Age vs BMI')
plt.xlabel('Age')
plt.ylabel('BMI')
plt.savefig('chart3.png')
plt.close()

print("Charts saved successfully.")