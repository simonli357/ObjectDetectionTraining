import os
import concurrent.futures

def process_file(file):
    with open(file, 'r') as f:
        lines = f.readlines()

    with open(file, 'w') as f:
        for line in lines:
            parts = line.strip().split(' ')

            # Convert negative numbers to positive numbers
            parts = [str(abs(float(part))) for part in parts]

            new_line = ' '.join(parts) + '\n'
            f.write(new_line)


def main():
    labels_folder = 'dataset/labels/val/'

    # Get all .txt files in the labels folder
    label_files = [os.path.join(labels_folder, f) for f in os.listdir(labels_folder) if f.endswith('.txt')]

    # Process files using multithreading
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(process_file, label_files)


if __name__ == '__main__':
    main()
