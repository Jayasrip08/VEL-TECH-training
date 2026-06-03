# Numerical python demo
import numpy as np

# Static data
scores = np.array([78, 82, 91, 65, 88, 74])
print(scores)
print("Mean:", scores.mean())
print("Max:", scores.max())
print("Min:", scores.min())
print("Std Dev:", scores.std())

passed = scores[scores >= 75]
print("Passed:", passed)
print("Count:", len(passed))


