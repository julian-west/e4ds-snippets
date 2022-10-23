"""Bad practice example PySpark code

- Difficult to read: Lots of complex logic in one place
- Difficult to test: Single function responsible for multiple actions
- Difficult to reuse: Can't reuse classification function across other processed
"""
import pyspark.sql.functions as F
from pyspark.sql import DataFrame


def classify_debit_credit_transactions(
    transactionsDf: DataFrame, accountDf: DataFrame
) -> DataFrame:
    """Join transactions with account information and classify as debit/credit"""

    # normalise strings
    transactionsDf = transactionsDf.withColumn(
        "transaction_information_cleaned",
        F.regexp_replace(F.col("transaction_information"), r"[^A-Z0-9]+", ""),
    )

    # join on customer account using first 9 characters
    transactions_accountsDf = transactionsDf.join(
        accountDf,
        on=F.substring(F.col("transaction_information_cleaned"), 1, 9)
        == F.col("account_number"),
        how="inner",
    )

    # classify transactions as from debit or credit account customers
    credit_account_ids = ["123", "124", "125"]
    debit_account_ids = ["212", "223", "258"]
    transactions_accountsDf = transactions_accountsDf.withColumn(
        "business_line",
        F.when(F.col("business_line_id").isin(credit_account_ids), F.lit("credit"))
        .when(F.col("business_line_id").isin(debit_account_ids), F.lit("debit"))
        .otherwise(F.lit("other")),
    )

    return transactions_accountsDf
