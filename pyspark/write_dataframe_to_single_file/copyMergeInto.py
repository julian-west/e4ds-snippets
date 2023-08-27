from typing import List

from py4j.java_gateway import JavaObject
from pyspark.sql import SparkSession


def configure_hadoop(spark: SparkSession):
    hadoop = spark.sparkContext._jvm.org.apache.hadoop  # type: ignore
    conf = hadoop.conf.Configuration()
    fs = hadoop.fs.FileSystem.get(conf)
    return hadoop, conf, fs


def ensure_exists(spark: SparkSession, file: str):
    hadoop, _, fs = configure_hadoop(spark)
    if not fs.exists(hadoop.fs.Path(file)):
        out_stream = fs.create(hadoop.fs.Path(file, False))
        out_stream.close()


def delete_location(spark: SparkSession, location: str):
    hadoop, _, fs = configure_hadoop(spark)
    if fs.exists(hadoop.fs.Path(location)):
        fs.delete(hadoop.fs.Path(location), True)


def get_files(spark: SparkSession, src_dir: str) -> List[JavaObject]:
    """Get list of files in HDFS directory"""
    hadoop, _, fs = configure_hadoop(spark)
    ensure_exists(spark, src_dir)
    files = []
    for f in fs.listStatus(hadoop.fs.Path(src_dir)):
        if f.isFile():
            files.append(f.getPath())
    if not files:
        raise ValueError("Source directory {} is empty".format(src_dir))

    return files


def copy_merge_into(
    spark: SparkSession, src_dir: str, dst_file: str, delete_source: bool = True
):
    """Merge files from HDFS source directory into single destination file

    Args:
        spark: SparkSession
        src_dir: path to the directory where dataframe was saved in multiple parts
        dst_file: path to single file to merge the src_dir contents into
        delete_source: flag for deleting src_dir and contents after merging

    """
    hadoop, conf, fs = configure_hadoop(spark)

    # 1. Get list of files in the source directory
    files = get_files(spark, src_dir)

    # 2. Set up the 'output stream' for the final merged output file
    # if destination file already exists, add contents of that file to the output stream
    if fs.exists(hadoop.fs.Path(dst_file)):
        tmp_dst_file = dst_file + ".tmp"
        tmp_in_stream = fs.open(hadoop.fs.Path(dst_file))
        tmp_out_stream = fs.create(hadoop.fs.Path(tmp_dst_file), True)
        try:
            hadoop.io.IOUtils.copyBytes(
                tmp_in_stream, tmp_out_stream, conf, False
            )  # False means don't close out_stream
        finally:
            tmp_in_stream.close()
            tmp_out_stream.close()

        tmp_in_stream = fs.open(hadoop.fs.Path(tmp_dst_file))
        out_stream = fs.create(hadoop.fs.Path(dst_file), True)
        try:
            hadoop.io.IOUtils.copyBytes(tmp_in_stream, out_stream, conf, False)
        finally:
            tmp_in_stream.close()
            fs.delete(hadoop.fs.Path(tmp_dst_file), False)
    # if file doesn't already exist, create a new empty file
    else:
        out_stream = fs.create(hadoop.fs.Path(dst_file), False)

    # 3. Merge files from source directory into the merged file 'output stream'
    try:
        for file in files:
            in_stream = fs.open(file)
            try:
                hadoop.io.IOUtils.copyBytes(
                    in_stream, out_stream, conf, False
                )  # False means don't close out_stream
            finally:
                in_stream.close()
    finally:
        out_stream.close()

    # 4. Tidy up - delete the original source directory
    if delete_source:
        delete_location(spark, src_dir)
