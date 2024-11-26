import os
import pandas as pd
from datetime import datetime, timezone, timedelta
import time

def get_utc_offset():
    """
    Get the UTC offset of the system as a string (e.g., 'UTC+8').
    """
    offset_sec = time.timezone if time.localtime().tm_isdst == 0 else time.altzone
    offset_hour = -offset_sec // 3600  # Convert seconds to hours
    return f"UTC{'+' if offset_hour >= 0 else ''}{offset_hour}"

def get_local_time_with_offset():
    """
    Get the current local time and UTC offset in the format:
    YYYYMMDDTHHMM_UTC+X
    """
    # Get the current local time
    local_time = datetime.now()
    utc_offset = get_utc_offset()
    return local_time.strftime(f"%Y%m%dT%H%M_{utc_offset}")

def rename_files(csv_path, directory):
    """
    Rename files in the directory based on Bates/Control # and Document ID in the CSV.
    Saves a report of the renaming process.

    Args:
        csv_path (str): Path to the CSV file containing Bates/Control # and Document ID columns.
        directory (str): Path to the directory containing files to be renamed.
    """
    # Prepare the report file
    base_csv_name = os.path.basename(csv_path)
    report_name = f"{get_local_time_with_offset()}_{base_csv_name}_RenameReport.txt"
    report_path = os.path.join(os.path.dirname(csv_path), report_name)
    
    # Open the report file for writing
    with open(report_path, "w") as report_file:
        def log(message):
            """Log a message to both the console and the report file."""
            print(message)
            report_file.write(message + "\n")

        # Read the CSV file
        try:
            df = pd.read_csv(csv_path)
            if 'Bates/Control #' not in df.columns or 'Document ID' not in df.columns:
                raise ValueError("CSV must contain 'Bates/Control #' and 'Document ID' columns.")
        except Exception as e:
            log(f"Error reading CSV file: {e}")
            return

        # Create a dictionary for mapping Bates/Control # to Document ID
        rename_map = dict(zip(df['Bates/Control #'], df['Document ID']))

        # Iterate through the files in the directory
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                # Extract the file's base name and extension
                base_name, extension = os.path.splitext(filename)

                # Rename the file if it matches a Bates/Control # in the CSV
                if base_name in rename_map:
                    new_name = f"{rename_map[base_name]}{extension}"
                    new_filepath = os.path.join(directory, new_name)

                    try:
                        os.rename(filepath, new_filepath)
                        log(f"Renamed: {filename} -> {new_name}")
                    except Exception as e:
                        log(f"Failed to rename {filename}: {e}")
                else:
                    log(f"No match found in CSV for file: {filename}")

        log(f"Report saved to: {report_path}")

if __name__ == "__main__":
    # Ask the user for the CSV file path and directory
    csv_path = input("Enter the full path to the CSV file: ").strip().strip('"')
    directory = input("Enter the full path to the directory: ").strip().strip('"')

    # Normalize paths to handle backslashes in Windows
    csv_path = os.path.normpath(csv_path)
    directory = os.path.normpath(directory)

    # Call the rename_files function
    rename_files(csv_path, directory)
