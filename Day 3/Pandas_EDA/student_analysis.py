# First Pandas Program
from pathlib import Path
import pandas as pd

script_dir = Path(__file__).resolve().parent
csv_path = script_dir / 'student-mat.csv'

df = pd.read_csv(csv_path, sep=';')
print(df.head())

# Check Dataset Shape
print("Shape:", df.shape)

# Display Column Names
print("Columns:", list(df.columns))

# Check Missing Values
print("Null values:\n", df.isnull().sum())

# Select One Column
ages = df['age']
print(ages.mean())
df['age']

# Select Multiple Columns
subset = df[['age', 'studytime', 'G3']]
print(subset.head())

# Filter Rows
hardworkers = df[df['studytime'] > 2]
print("Hard workers:", len(hardworkers))
print("Their avg grade:", hardworkers['G3'].mean())

# EDA Begins
print(df.describe())

# Category Counts
print(df['sex'].value_counts())
print(df['internet'].value_counts())

# GroupBy Analysis
study_vs_grade = df.groupby('studytime')['G3'].mean()
print("Study Time vs Grade:")
print(study_vs_grade)

# Internet vs Grade
internet_vs_grade = df.groupby('internet')['G3'].mean()
print("Internet vs Grade:")
print(internet_vs_grade)

# Absence Analysis
absence_low = df[df['absences'] <= 3]['G3'].mean()
absence_high = df[df['absences'] > 10]['G3'].mean()
print(f"Low absences avg grade: {absence_low:.1f}")
print(f"High absences avg grade: {absence_high:.1f}")

