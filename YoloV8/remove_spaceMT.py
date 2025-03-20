import os
import concurrent.futures

# Set the folder path containing the txt files
folder_path = "dataset/labels/train/"

def process_file(filename):
    # Check if the file is a txt file
    if filename.endswith(".txt"):
        # Open the file in read mode
        with open(os.path.join(folder_path, filename), "r") as f:
            # Read the contents of the file
            lines = f.readlines()
        # Open the file in write mode
        with open(os.path.join(folder_path, filename), "w") as f:
            # Loop through each line in the file
            for line in lines:
                # Remove the first space of the line
                line = line.strip()
                if line.startswith(" "):
                    line = line[1:]
                # elif line.startswith("nan"):
                #     line = line[3:]
                # Write the modified line to the file
                f.write(line + "\n")
        return 1
    return 0

# Use ThreadPoolExecutor to process files concurrently
with concurrent.futures.ThreadPoolExecutor() as executor:
    results = list(executor.map(process_file, os.listdir(folder_path)))

print("Processed files:", sum(results))
