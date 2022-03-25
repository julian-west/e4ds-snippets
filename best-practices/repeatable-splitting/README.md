# ML Design Pattern: Repeatable Splitting

https://engineeringfordatascience.com/posts/ml_repeatable_splitting_using_hashing/

> Blog post inspired by the [ML Design Patterns book](https://www.oreilly.com/library/view/machine-learning-design/9781098115777/)

## Reproducible ML: Maybe you shouldn't be using train_test_split¶

Reproducibility is critical for robust data science -- after all, it is a science.

But reproducibility in ML can be surprisingly difficult.

**The behaviour of your model doesn't only depend on your code, but also the underlying dataset that was used to train it**

Therefore, you need to keep tight control on which data points were used to train and test your model to ensure reproducibility.

A fundamental tenet of the ML workflow is splitting your data into training and testing sets. This involves deliberately withholding some data points from the model training in order to evaluate the performance of your model on 'unseen' data.

It is vitally important to be able to reproducibly split your data across different training runs. For a few main reasons:

- So you can use the same test data points to effectively compare the performance of different model candidates
- To control as many variables as possible to help troubleshoot performance issues
- To ensure that you, or your colleagues, can reproduce your model exactly
How you split your data can have a big effect on the perceived model performance

It is important to control and understand the training and test splits when comparing different model candidates and across multiple training runs.

**Sklearn train_test_split**

Probably, the most common way to split your dataset is to use Sklearn's train_test_split function.

Out of the box, the train_test_split function will randomly split your data into a training set and a test set. Each time you run the function you will get a different split for your data. Not ideal for reproducibility.

"Ah!" you say. "I set the random seed so it is reproducible!".

Fair point. Setting random seeds is certainly an excellent idea and goes a long way to improve reproducibility. I would highly recommend setting random seeds for any functions which have non-deterministic outputs.

However, random seeds might not be enough to ensure reproducibility

In this post I will demonstrate that the train_test_split function is more sensitive than you might think, and explain why using a random seed does not always guarantee reproducibility, particularly if you need to retrain your model in the future.

Sometimes `train_test_split()` does not guarantee reproducibility -- even if you set the random seed.


## The Solution: Hashing

See the notebook in this folder for a demonstration and commentary on using the Farmhash algorithm to split your data in a robust manner.

## Resources

**Hashing**
- [ML Design Pattern: Repeatable sampling](https://towardsdatascience.com/ml-design-pattern-5-repeatable-sampling-c0ccb2889f39) (inspiration for this post)
- [Hash your data before you create the train-test split](https://www.bi-kring.nl/192-data-science/1340-reusing-data-for-ml-hash-your-data-before-you-create-the-train-test-split)
- [Farmhash Algorithm Description](https://github.com/google/farmhash/blob/master/Understanding_Hash_Functions)
- [Python Farmhash library](https://pypi.org/project/pyfarmhash/)
- [Different hashing implementation from Hands-on Machine Learning with Scikit-Learn, Keras and TensorFlow](https://www.danli.org/2021/06/06/hands-on-machine-learning/) also [see notebook](https://github.com/ageron/handson-ml2/blob/master/02_end_to_end_machine_learning_project.ipynb)
- [Google documentation: Considerations for Hashing](https://developers.google.com/machine-learning/data-prep/construct/sampling-splitting/randomization)

**Differences between Python and BigQuery**
- [Farmhash vs BigQuery implementation, GitHub issue](https://github.com/lovell/farmhash/issues/26)
- [StackOverflow question: difference in results between BigQuery and Python](https://stackoverflow.com/questions/63341637/python-vs-bigquery-farmhash-sometimes-do-not-equal)
- [BigQuery returns signed integers from FARM_FINGERPRINT function](https://stackoverflow.com/questions/51892989/how-does-bigquerys-farm-fingerprint-represent-a-64-bit-unsigned-int)
- [Be careful about operation order in BigQuery](https://mentin.medium.com/be-careful-with-abs-function-8e91c78715d5)
- [Reproducibly sampling in BigQuery](https://towardsdatascience.com/advanced-random-sampling-in-bigquery-sql-7d4483b580bb)
