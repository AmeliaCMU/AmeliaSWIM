import csv

# Input and output file names
airport = 'kden'
input_file = f'/Users/alonso.cano/Desktop/{airport}.txt'
output_file = f'conf/qgist/{airport}_v1.csv'


def txt_to_csv(input_file, output_file):
    try:
        with open(input_file, 'r') as file:
            # Read the single line of coordinates
            line = file.readline().strip()

            # Split by comma to get each coordinate pair
            pairs = [pair.strip() for pair in line.split(',') if pair.strip()]

            # Extract Longitude and Latitude (reversed order)
            coordinates = []
            for pair in pairs:
                lon, lat = map(float, pair.split())
                coordinates.append([lat, lon])

            # Write to CSV with reversed columns
            with open(output_file, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Lat', 'Lon'])  # Add header
                writer.writerows(coordinates)

            print(f"Successfully converted to CSV: {output_file}")
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
    except Exception as e:
        print(f"Error: An unexpected error occurred. {e}")


# Run the function
txt_to_csv(input_file, output_file)
