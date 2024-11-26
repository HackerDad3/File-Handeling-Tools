import os
import pandas as pd

def rename_files(csv_path, directory):
    """
    Rename files in the directory based on Bates/Control # and Document ID in the CSV.

    Args:
        csv_path (str): Path to the CSV file containing Bates/Control # and Document ID columns.
        directory (str): Path to the directory containing files to be renamed.
    """
    # Read the CSV file
    try:
        df = pd.read_csv(csv_path)
        if 'Bates/Control #' not in df.columns or 'Document ID' not in df.columns:
            raise ValueError("CSV must contain 'Bates/Control #' and 'Document ID' columns.")
    except Exception as e:
        print(f"Error reading CSV file: {e}")
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
                    print(f"Renamed: {filename} -> {new_name}")
                except Exception as e:
                    print(f"Failed to rename {filename}: {e}")
            else:
                print(f"No match found in CSV for file: {filename}")

# Example usage:
# csv_path = "path/to/your/csv_file.csv"
# directory = "path/to/your/files"
# rename_files(csv_path, directory)
