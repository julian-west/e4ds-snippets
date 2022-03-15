# ML Design Pattern: Repeatable Splitting

> Blog post inspired by [ML Design Patterns book](https://www.oreilly.com/library/view/machine-learning-design/9781098115777/)

Sometimes `train_test_split()` does not guarantee reproducibility -- even if you set the random seed.

If you want to retrain your model on new data (i.e. add new data to your original dataset), your train test splits will be completely different to the original training regime. Datapoints which


This can be problematic for a few reasons:
- It hard to accurately compare model accuracy between training runs. If data-points used for training one model are in the test set for other (and visa-versa) it will not be a fair comparison.
- If model performance declines it can be hard to debug. Was the model degradation due to how the data was split originally? Or is it the new data?
- If you can't guarantee the order of your data will be the same between training runs, your train/test splits will be different.

Ultimately, you want your results to reproducible and robust. Using hashing techniques to decide your train/test split can improve the robustness of your training runs.
