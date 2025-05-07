import yaml
import csv
import sys
import os
airport = 'kbwi'
# Input and output file names
input_file = f'conf/airports/{airport}.yaml'
output_file = f'conf/qgist/{airport}.csv'


def convert_fence_to_csv(input_file, output_file):
    try:

       # Read the YAML file
        with open(input_file, 'r') as file:
            data = yaml.safe_load(file)

        # Extract the fence coordinates
        fence_coordinates = data.get("fence", [])

        # Write to CSV file
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Lat", "Lon"])  # Header
            for polygon in fence_coordinates:
                for coordinate in polygon:
                    writer.writerow(coordinate)

        print(f"Successfully converted 'fence' to CSV: {output_file}")
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
    except yaml.YAMLError as e:
        print(f"Error: Failed to parse YAML file. {e}")
    except Exception as e:
        print(f"Error: An unexpected error occurred. {e}")


# Run the function
if __name__ == "__main__":
    # Get all YAML files in the "conf/airports/" directory
    input_dir = 'conf/airports/'
    output_dir = 'conf/qgist/'
    input_files = [f for f in os.listdir(input_dir) if f.endswith('.yaml')]

    # Filter files that are not already processed in "conf/qgist/"
    unprocessed_files = [
        f for f in input_files if not os.path.exists(os.path.join(output_dir, f.replace('.yaml', '.csv')))
    ]
    # breakpoint()
    # Process each unprocessed file
    for file_name in unprocessed_files:
        input_file = os.path.join(input_dir, file_name)
        output_file = os.path.join(output_dir, file_name.replace('.yaml', '.csv'))
        convert_fence_to_csv(input_file, output_file)

    # Convert the fence to CSV
# convert_fence_to_csv(input_file, output_file)
