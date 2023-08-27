## Writing PySpark dataframe to a single output file

When using other Python packages like Pandas, saving the output to a single output file
(e.g. csv) is as simple as running 'pd.to_csv'.

However, when calling PySpark's 'df.write.csv' function, the dataframe is written to a
folder and split into multiple files (one for each partition).

You can use the code in the 'copy_merge_into' function in this folder to merge these
multiple files into a single output file on HDFS.

There is an example script in `main.py` that shows how to use the `copy_merge_into`
function to write a spark dataframe to a single output csv file.

```bash
# install requirements (pyspark 3.3.1)
pip install -r requirements.txt

# run script
python main.py
```
