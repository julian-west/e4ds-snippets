import pyspark.sql.functions as F
import pyspark.sql.types as T
from copyMergeInto import copy_merge_into
from pyspark.sql import DataFrame, SparkSession


def init_spark() -> SparkSession:
    return SparkSession.builder.getOrCreate()


def create_example_dataframe(nrows: int, ncols: int, seed: int = 1) -> DataFrame:
    """Create dataframe (nrows x ncols) with random data"""
    df = spark.range(nrows).select(F.col("id"))
    df = df.select(
        "*", *(F.rand(seed).alias("col_" + str(target)) for target in range(ncols))
    )
    return df


if __name__ == "__main__":
    TMP_OUTPUT_DIR = "test"
    OUTPUT_FILE = "test.csv"

    spark = init_spark()

    df = create_example_dataframe(nrows=50, ncols=3)

    df = df.repartition(5)

    # Write headers (required for csv only)
    headers = spark.createDataFrame(
        data=[[f.name for f in df.schema.fields]],
        schema=T.StructType(
            [T.StructField(f.name, T.StringType(), False) for f in df.schema.fields]
        ),
    )

    headers.write.csv(TMP_OUTPUT_DIR)

    # write csv headers to output file first
    copy_merge_into(
        spark,
        TMP_OUTPUT_DIR,
        OUTPUT_FILE,
    )

    # Write main outputs
    # dataframe written to TMP_OUTPUT_DIR folder in 5 separate csv files
    df.write.csv(TMP_OUTPUT_DIR)

    # merge main csv files in folder into single file
    copy_merge_into(
        spark,
        TMP_OUTPUT_DIR,
        OUTPUT_FILE,
    )
