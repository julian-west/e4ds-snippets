from pyspark.sql import SparkSession

# create spark session
spark = SparkSession.builder.getOrCreate()

# create example dataframe
columns = ["county", "revenue"]
data = [("uk", 1000), ("us", 2000), ("germany", 3000), ("france", 4000)]

df = spark.createDataFrame(data, columns)


# 1. Naive Method (doesn't work)
summary_string = df.show()  # type: ignore
print(summary_string)
print(type(summary_string))


# 2. Using internal self.jdf.showString (does work)
summary_string = df._jdf.showString(20, 20, False)
print(summary_string)
print(type(summary_string))


# Notes: the following will throw errors
# df._jdf.showString()
# df._jdf.showString(n=20, truncate=20, vertical=False)


def get_df_string_repr(df, n=20, truncate=True, vertical=False):
    """Example wrapper function for interacting with self._jdf.showString"""
    if isinstance(truncate, bool) and truncate:
        return df._jdf.showString(n, 20, vertical)
    else:
        return df._jdf.showString(n, int(truncate), vertical)


print(get_df_string_repr(df))
