import pyspark.sql.functions as F
from pyspark.sql import DataFrame


def classify_debit_credit_transactions(
    transactionsDf: DataFrame, accountsDf: DataFrame
) -> DataFrame:
    """Join transactions with account information and classify as debit/credit"""

    transactionsDf = normalise_transaction_information(transactionsDf)

    transactions_accountsDf = join_transactionsDf_to_accountsDf(
        transactionsDf, accountsDf
    )

    transactions_accountsDf = apply_debit_credit_business_classification(
        transactions_accountsDf
    )

    return transactions_accountsDf


def normalise_transaction_information(transactionsDf: DataFrame) -> DataFrame:
    """Remove special characters from transaction information"""
    return transactionsDf.withColumn(
        "transaction_information_cleaned",
        F.regexp_replace(F.col("transaction_information"), r"[^A-Z0-9]+", ""),
    )


def join_transactionsDf_to_accountsDf(
    transactionsDf: DataFrame, accountsDf: DataFrame
) -> DataFrame:
    """Join transactions to accounts information"""
    return transactionsDf.join(
        accountsDf,
        on=F.substring(F.col("transaction_information_cleaned"), 1, 9)
        == F.col("account_number"),
        how="inner",
    )


def apply_debit_credit_business_classification(
    transactions_accountsDf: DataFrame,
) -> DataFrame:
    """Classify transactions as coming from debit or credit account customers"""
    # TODO: move to config file
    CREDIT_ACCOUNT_IDS = ["123", "124", "125"]
    DEBIT_ACCOUNT_IDS = ["212", "223", "258"]

    return transactions_accountsDf.withColumn(
        "business_line",
        F.when(F.col("business_line_id").isin(CREDIT_ACCOUNT_IDS), F.lit("credit"))
        .when(F.col("business_line_id").isin(DEBIT_ACCOUNT_IDS), F.lit("debit"))
        .otherwise(F.lit("other")),
    )
