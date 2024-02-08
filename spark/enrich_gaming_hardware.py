from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, dense_rank, round
from pyspark.sql.window import Window
import subprocess

# Initialize Spark Session
spark = SparkSession.builder.appName("EnrichGameHardwareData").getOrCreate()

# Adjust log level to suppress warnings
spark.sparkContext.setLogLevel("ERROR")

def run_cmd(args_list):
    """Run linux commands"""
    print('Running system command: {0}'.format(' '.join(args_list)))
    proc = subprocess.Popen(args_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.communicate()
    return proc.returncode

def check_hdfs_running():
    status = run_cmd(['hdfs', 'dfsadmin', '-report'])
    if status == 0:
        print("HDFS is running.")
        return True
    else:
        print("HDFS is not running.")
        return False

def ensure_path_exists(path):
    if run_cmd(['hdfs', 'dfs', '-test', '-e', path]) != 0:
        run_cmd(['hdfs', 'dfs', '-mkdir', '-p', path])
        print(f"Created directory: {path}")

# HDFS Base Path and file path correction
hdfs_base_path = "hdfs://localhost:9000"
category_path = "/user/hadoop/amazon/categories/Game_Hardware"
file_path = f"{hdfs_base_path}{category_path}"

# Adjusted enriched data save paths
enriched_base_path = f"{hdfs_base_path}/user/hadoop/amazon/enriched_categories/Game_Hardware"

# Check if HDFS is running
if not check_hdfs_running():
    spark.stop()
    raise Exception("HDFS is not running. Please start HDFS and try again.")

# Ensure the base path for enriched data exists
ensure_path_exists(enriched_base_path)

# Read the CSV file
df = spark.read.option("header", "true").csv(file_path, inferSchema=True)

# Calculate Value Score = stars / price (handling division by zero)
value_score_expr = round(col("stars") / (col("price") + lit(0.01)), 2)  # Now rounding to 2 decimal places
df = df.withColumn("value_score", value_score_expr)

# Window specification for dense ranking
windowSpec = Window.orderBy(col("reviews").desc())
df = df.withColumn("reviews_rank", dense_rank().over(windowSpec))

# Save paths adjusted as requested
top_sellers_save_path = f"{enriched_base_path}/Top100_seller"
top_reviews_save_path = f"{enriched_base_path}/Top100_reviews"
best_investments_save_path = f"{enriched_base_path}/Best_investments"

# Top 100 sellers last month
top_sellers_last_month = df.filter(col("boughtInLastMonth") > 0).orderBy(col("boughtInLastMonth").desc()).limit(100)
ensure_path_exists(top_sellers_save_path)
top_sellers_last_month.write.option("header", "true").csv(top_sellers_save_path, mode="overwrite")

# Top 100 by reviews
top_by_reviews = df.orderBy(col("reviews").desc()).limit(100)
ensure_path_exists(top_reviews_save_path)
top_by_reviews.write.option("header", "true").csv(top_reviews_save_path, mode="overwrite")

# Best investments (Quality/Price Ratio) with at least 100 reviews
best_investments = df.filter(col("reviews") >= 100).withColumn("value_score", value_score_expr).orderBy(col("value_score").desc()).limit(100)
ensure_path_exists(best_investments_save_path)
best_investments.write.option("header", "true").csv(best_investments_save_path, mode="overwrite")

print("Enriched data saved successfully.")

# Stop Spark Session
spark.stop()
