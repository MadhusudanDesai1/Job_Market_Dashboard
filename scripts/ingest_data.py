import kagglehub
import shutil
import os
import glob

# 1. Download latest version
print("Downloading dataset...")
path = kagglehub.dataset_download("murilozangari/jobs-and-salaries-in-data-field-2024")

print(f"Dataset downloaded to cache at: {path}")

# 2. Define your project data path (The 'data' folder we created)
destination_folder = "data"
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# 3. Find the CSV file in the download path and move it
csv_files = glob.glob(os.path.join(path, "*.csv"))

if csv_files:
    source_file = csv_files[0] # Take the first CSV found
    file_name = os.path.basename(source_file)
    destination_path = os.path.join(destination_folder, "jobs_data.csv") # Renaming it for simplicity
    
    shutil.copy(source_file, destination_path)
    print(f"✔ Success! File saved to: {destination_path}")
else:
    print("❌ Error: No CSV file found in the downloaded folder.")