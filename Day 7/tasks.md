# Day 7 Tasks

## 1. Compute full evaluation metrics for your Day 6 model (Specific to your project)
**What this means:** Yesterday you built a model and looked at a few predictions. Today, we need to calculate an overall "grade" or score for how well the model performed on the entire test dataset.
**What to do:** 
- **Classifiers (predicting categories):** Print the `classification_report(y_test, y_pred)`. This will give you grades on Accuracy, Precision, Recall, and F1-score for each category.
- **Regressors (predicting numbers - e.g., Akshara, Sai Sree Harsha):** Calculate your error scores: RMSE (Root Mean Squared Error), MAE (Mean Absolute Error), and R².
- **Anomaly Detection (e.g., Shalini):** Print the number of anomalies your model detected compared to the actual number of anomalies.
- **Similarity/Recommendation (e.g., Mithun):** Manually inspect the top-5 recommendations your model gives for 3 different movie inputs to see if they make sense.

## 2. Plot a confusion matrix or residual plot (Specific to your project)
**What this means:** Numbers are great, but pictures are better! We need to visualize the mistakes the model is making to better understand where it gets confused.
**What to do:** 
- **Classifiers:** Create a heatmap of your confusion matrix using `seaborn.heatmap(confusion_matrix(y_test, y_pred))` and make sure to label the axes. 
  - *Multi-class projects (Tarun, Naga Lakshmi, Paul, Shalini):* Add `normalize='true'` so you can see the percentages.
- **Regressors:** Plot a scatter plot of your actual values versus predicted values with a diagonal reference line. If the dots are close to the line, the model is doing well!
- **Finally:** Save this plot to your computer as `confusion_matrix.png` or `residual_plot.png`.

## 3. Train a second comparison algorithm (Specific to your project)
**What this means:** To know if our Day 6 model is actually good, we need to compare it to something else! We will train a second, different type of model to serve as a baseline.
**What to do:** 
- Train another algorithm using the exact same `X_train` and `X_test` data from yesterday. **CRITICAL RULE:** Do not split your data again or re-preprocess it. Use the exact same variables!
- **Specific Assignments:**
  - *Bhaskhar:* Logistic Regression vs Random Forest.
  - *Akshara:* Linear Regression vs Ridge.
  - *Tarun:* Naive Bayes vs Random Forest.
  - *Nihal, Koteswara, Reashma, Rithin, Sai Sree Harsha:* Add a Decision Tree as your baseline.
  - *Everyone else:* Add Logistic Regression or a Decision Tree as a simple baseline.

## 4. Build a side-by-side comparison DataFrame (Universal for everyone)
**What this means:** Now that you have two models, let's put their report cards side-by-side so we can clearly declare a winner.
**What to do:** 
- Create a pandas `DataFrame` (a table) where the rows are your model names and the columns are the scores you calculated in Step 1.
- **Classifiers:** Use Accuracy, Precision (weighted), Recall (weighted), and F1 (weighted).
- **Regressors:** Use RMSE, MAE, and R².
- Print this table clearly and save it as `comparison.csv`. 
- In your notebook, write a markdown cell where you clearly state which model is better and write one sentence explaining *why* based on the table.

## 5. Save the winning model as best_model.pkl (Universal for everyone)
**What this means:** You've found your best model! Now you need to save it safely so you can use it in your final application.
**What to do:** 
- Pick the better-performing model from your comparison table.
- Save it using `joblib.dump(model, 'best_model.pkl')`.
- Check your files to make sure any scaler or encoder `.pkl` files you created on Day 6 are still there (you will need them later!).
- Print out the final chosen model's name and its best score at the end of your notebook.



