from pyspark.sql import SparkSession, types
from pyspark.sql.functions import col, lit, dense_rank, round
from pyspark.sql.window import Window
import subprocess
import re

def run_cmd(args_list):
    """Run linux commands and return output"""
    print('Running system command: {0}'.format(' '.join(args_list)))
    proc = subprocess.Popen(args_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    return out, err, proc.returncode

def check_hdfs_running():
    _, _, status = run_cmd(['hdfs', 'dfsadmin', '-report'])
    if status == 0:
        print("HDFS is running.")
        return True
    else:
        print("HDFS is not running.")
        return False

def ensure_path_exists(path):
    out, err, status = run_cmd(['hdfs', 'dfs', '-test', '-e', path])
    if status == 0:
        print(f"Directory already exists: {path}")
    else:
        _, _, mkdir_status = run_cmd(['hdfs', 'dfs', '-mkdir', '-p', path])
        if mkdir_status == 0:
            print(f"Created directory: {path}")
        else:
            print(f"Failed to create directory: {path}, Error: {err.decode('utf-8')}")


def get_category_folders():
    """List category folders within /user/hadoop/amazon/categories/"""
    path = f"{hdfs_base_path}/user/hadoop/amazon/categories/"
    out, err, status = run_cmd(['hdfs', 'dfs', '-ls', path])
    if status == 0:
        folders = re.findall(r'\S+/(\S+)', out.decode('utf-8'))
        return folders
    else:
        print("Error listing category folders:", err.decode('utf-8'))
        return []

def process_category(category_name):
    category_folders = get_category_folders()
    matched_folders = [folder for folder in category_folders if category_name.replace(' ', '_') in folder]
    
    if not matched_folders:
        print(f"No matching folder found for category: {category_name}")
        return

    category_path = f"/user/hadoop/amazon/categories/{matched_folders[0]}"
    file_path = f"{hdfs_base_path}{category_path}"

    enriched_base_path = f"{hdfs_base_path}/user/hadoop/amazon/enriched_categories/{matched_folders[0]}"
    ensure_path_exists(enriched_base_path)

    
    df = spark.read.option("header", "true").csv(file_path, inferSchema=True)
    
    value_score_expr = round(col("stars") / (col("price") + lit(0.01)), 2)
    df = df.withColumn("value_score", value_score_expr)
    
    windowSpec = Window.orderBy(col("reviews").desc())
    df = df.withColumn("reviews_rank", dense_rank().over(windowSpec))
    
    top_sellers_save_path = f"{enriched_base_path}/Top100_seller"
    top_reviews_save_path = f"{enriched_base_path}/Top100_reviews"
    best_investments_save_path = f"{enriched_base_path}/Best_investments"
    
    top_sellers_last_month = df.filter(col("boughtInLastMonth") > 0).orderBy(col("boughtInLastMonth").desc()).limit(100)
    ensure_path_exists(top_sellers_save_path)
    top_sellers_last_month.write.option("header", "true").csv(top_sellers_save_path, mode="overwrite")
    
    top_by_reviews = df.orderBy(col("reviews").desc()).limit(100)
    ensure_path_exists(top_reviews_save_path)
    top_by_reviews.write.option("header", "true").csv(top_reviews_save_path, mode="overwrite")
    
    best_investments = df.filter(col("reviews") >= 100).withColumn("value_score", value_score_expr).orderBy(col("value_score").desc()).limit(100)
    ensure_path_exists(best_investments_save_path)
    best_investments.write.option("header", "true").csv(best_investments_save_path, mode="overwrite")
    
    print(f"Enriched data saved successfully for {category_name}.")

# Initialize Spark Session
spark = SparkSession.builder.appName("EnrichData").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

# HDFS Base Path
hdfs_base_path = "hdfs://localhost:9000"

if not check_hdfs_running():
    spark.stop()
    raise Exception("HDFS is not running. Please start HDFS and try again.")

# Dynamically process categories based on the folders available
for category_name in ["Game Hardware", "Golf Equipment"]:
    process_category(category_name)

# Stop Spark Session
spark.stop()