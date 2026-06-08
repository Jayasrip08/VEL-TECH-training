# Day 8 Tasks

## 1. Load best_model.pkl and record baseline score (Universal for everyone)
**What this means:** Before we try to improve our model, we need to know what score we are trying to beat! This is our "baseline" score.
**What to do:** 
- Load the `best_model.pkl` you saved yesterday.
- Re-test it on your `X_test` data from Day 6. 
- Print out the primary score. For classifiers use F1-weighted, and for regressors use RMSE. Write this number down!
- Also, run a "cross-validation" by using `cross_val_score(model, X_train, y_train, cv=5)`. This is like giving the model 5 mini-quizzes instead of one big one to see if it performs consistently. Print the mean (average) score and standard deviation (how much the scores varied).

## 2. Define a param_grid for your algorithm (Specific to your project)
**What this means:** Models have "settings" or "dials" (called hyperparameters) that we can adjust. A `param_grid` is a list of different dial positions we want the computer to try out.
**What to do:** 
- Write a `param_grid` (which is a dictionary in Python) with at least 2 parameters, testing 3 different values for each. This means testing at least 9 different combinations!
- **Specific Settings to Try:**
  - *Random Forest / Gradient Boosting:* Tune `n_estimators`, `max_depth`, `min_samples_split`.
  - *XGBoost:* Tune `learning_rate`, `n_estimators`, `max_depth`.
  - *SVM:* Tune `C`, `kernel`, `gamma`.
  - *Ridge:* Tune `alpha`.
  - *Naive Bayes:* Tune `var_smoothing`.
  - *Decision Tree:* Tune `max_depth`, `criterion`.

## 3. Run GridSearchCV with cv=5 (Universal for everyone)
**What this means:** We are going to make the computer test every single combination of settings in your `param_grid` to find the absolute best ones. This is called a Grid Search.
**What to do:** 
- Create a searcher by wrapping your model: `grid = GridSearchCV(model, param_grid, cv=5, scoring='f1_weighted', n_jobs=-1)`. *(Note: If you are doing regression, change scoring to `'neg_mean_squared_error'`)*.
- Start the search by running `.fit(X_train, y_train)`. 
- Print `grid.best_params_` (the winning settings) and `grid.best_score_` (the winning score).
- *Tip:* If the search takes longer than 15 minutes, stop it and switch to `RandomizedSearchCV(n_iter=20)` which is a faster version that only tests random combinations instead of all of them.

## 4. Print a before vs after comparison (Universal for everyone)
**What this means:** Let's see if all that tuning actually helped!
**What to do:** 
- Test your newly tuned model (`grid.best_estimator_`) on the `X_test` data.
- Create a small 2-row table (DataFrame) comparing the primary score of your "Default model" (from Step 1) against your "Tuned model". Print it out.
- *Note:* Even a tiny +0.5% improvement is great—document it! If your tuned model is somehow worse, don't panic. Be honest and write a 2-line explanation in your notebook about why it happened (e.g., maybe the dataset is too small, or it memorized the training data too much—"overfitting").

## 5. Plot a validation curve and save tuned model (Universal for everyone)
**What this means:** We want to visualize how changing a setting affected the model's performance. Then, we need to save our final, best-ever model.
**What to do:** 
- Use the data inside `grid.cv_results_` to plot a line graph showing how the cross-validation score changed as you adjusted one of your key settings. This helps show if the model is underfitting or overfitting.
- Save this ultimate, tuned model to your computer using `joblib.dump(grid.best_estimator_, 'tuned_model.pkl')`.
