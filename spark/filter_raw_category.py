from pyspark.sql import SparkSession, types
from pyspark.sql.functions import col
import subprocess

def check_hdfs_running():
    try:
        result = subprocess.run(['hdfs', 'dfsadmin', '-report'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            return True
    except Exception as e:
        print(f"Error checking HDFS status: {e}")
    return False

def path_exists(path):
    try:
        result = subprocess.run(['hdfs', 'dfs', '-test', '-e', path])
        return result.returncode == 0
    except Exception as e:
        print(f"Error checking path existence: {e}")
    return False

def filter_and_save_category_data(category_name):
    # Define schema explicitly to ensure data validation
    schema = types.StructType([
        types.StructField("asin", types.StringType(), True),
        types.StructField("title", types.StringType(), True),
        types.StructField("imgUrl", types.StringType(), True),
        types.StructField("productURL", types.StringType(), True),
        types.StructField("stars", types.FloatType(), True),
        types.StructField("reviews", types.IntegerType(), True),
        types.StructField("price", types.FloatType(), True),
        types.StructField("listPrice", types.FloatType(), True),
        types.StructField("categoryName", types.StringType(), True),
        types.StructField("isBestSeller", types.BooleanType(), True),
        types.StructField("boughtInLastMonth", types.IntegerType(), True)
    ])

    # Read the CSV file with explicit schema
    df = spark.read.csv(hdfs_base_path + file_path, header=True, schema=schema)

    # Filter for category and validate required fields
    filtered_df = df.filter(
        (col("categoryName") == category_name) &
        col("asin").isNotNull() & col("title").isNotNull() &
        (col("stars") > 0) & (col("reviews") > 0) &
        (col("price") > 0) &  # Exclude products with a price of 0.0
        (col("boughtInLastMonth") >= 0)
    )

    # Path for saving the data
    save_path = f"{hdfs_base_path}/user/hadoop/amazon/categories/{category_name.replace(' ', '_')}"

    # Save the filtered data with header
    filtered_df.write.option("header", "true").csv(save_path, mode="overwrite")
    print(f"Filtered data for {category_name} saved successfully with headers at:", save_path)

# Initialize Spark Session
spark = SparkSession.builder.appName("FilterCategories").getOrCreate()

# HDFS Base Path
hdfs_base_path = "hdfs://localhost:9000"

# CSV file path
file_path = "/user/hadoop/amazon/raw_products/amz_ca_total_products_data_processed.csv"

# Check if HDFS is running
if not check_hdfs_running():
    print("HDFS is not running. Please start HDFS and try again.")
    spark.stop()
    exit()

# Check if the file exists
if not path_exists(hdfs_base_path + file_path):
    print(f"File {file_path} does not exist in HDFS.")
    spark.stop()
    exit()

# Dynamically process categories based on the folders available
for category_name in ["Game Hardware", "Golf Equipment"]:
    filter_and_save_category_data(category_name)

# Stop Spark Session
spark.stop()
