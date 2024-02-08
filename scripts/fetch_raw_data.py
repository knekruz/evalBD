import os
import subprocess
import shutil
from kaggle.api.kaggle_api_extended import KaggleApi

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

def download_and_extract_dataset(local_path):
    # Configure Kaggle API and authenticate
    api = KaggleApi()
    api.authenticate()
    print("Downloading dataset...")
    api.dataset_download_files('asaniczka/amazon-canada-products-2023-2-1m-products', path=local_path, unzip=True)
    print("Dataset downloaded and extracted.")

def upload_to_hdfs(local_path, hdfs_path):
    run_cmd(['hdfs', 'dfs', '-rm', '-r', hdfs_path])
    print("Uploading to HDFS...")
    csv_file = os.path.join(local_path, 'amz_ca_total_products_data_processed.csv')
    run_cmd(['hdfs', 'dfs', '-put', csv_file, hdfs_path])
    print("Upload completed.")

if __name__ == "__main__":
    local_path = "/home/hadoop/Bureau/raw"
    hdfs_path = "/user/hadoop/amazon/raw_products/amz_ca_total_products_data_processed.csv"
    
    if check_hdfs_running():
        if os.path.exists(local_path):
            shutil.rmtree(local_path)
        os.makedirs(local_path, exist_ok=True)
        download_and_extract_dataset(local_path)
        upload_to_hdfs(local_path, hdfs_path)
    else:
        print("Please ensure HDFS is running and try again.")
