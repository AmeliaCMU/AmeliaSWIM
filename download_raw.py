import argparse
import os
import time
import requests
from datetime import datetime
from tqdm import tqdm
from urllib.parse import urljoin


class SwiftFileDownloader:
    def __init__(self, base_url):
        self.base_url = base_url

    def download_files(self, start_time, end_time, destination_folder, time_format="human"):
        # Ensure output directory exists
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder, exist_ok=True)

        # Convert human → unix timestamps
        if time_format == "human":
            start_timestamp = int(time.mktime(time.strptime(start_time, "%Y-%m-%d %H:%M:%S")))
            end_timestamp = int(time.mktime(time.strptime(end_time, "%Y-%m-%d %H:%M:%S")))
        elif time_format == "unix":
            start_timestamp = start_time
            end_timestamp = end_time
        else:
            raise ValueError("Invalid time_format")

        print(f"Start TS: {start_timestamp}   End TS: {end_timestamp}")

        file_list = self._list_all_objects()

        for fname in file_list:
            if not fname.startswith("ALL"):
                continue
            try:
                file_timestamp = int(fname.split("_")[1].split(".")[0])
            except Exception:
                continue

            if start_timestamp <= file_timestamp <= end_timestamp:
                self._download_file(fname, destination_folder)
    
    def _list_all_objects(self):
        """List ALL objects in Swift with pagination."""
        files = []
        marker = None

        while True:
            params = {"format": "plain"}
            if marker:
                params["marker"] = marker

            resp = requests.get(self.base_url, params=params)
            
            if resp.status_code == 204:
                # No more objects
                break
            if resp.status_code != 200:
                print(f"Failed listing (HTTP {resp.status_code})")
                break

            page = resp.text.splitlines()

            if not page:
                # No more objects
                break

            files.extend(page)

            # Prepare next page
            marker = page[-1]

            print(f"Retrieved {len(page)} more objects... total so far: {len(files)}")

        print(f"Total objects in bucket: {len(files)}")
        return files

    def _download_file(self, filename, destination_folder):
        local_path = os.path.join(destination_folder, filename)

        if os.path.exists(local_path):
            print(f"File {filename} already exists, skipping.")
            return

        url = urljoin(self.base_url, filename)
        print(f"Downloading {filename}")

        with requests.get(url, stream=True) as r:
            if r.status_code != 200:
                print(f"Failed: {filename} ({r.status_code})")
                return

            total_size = int(r.headers.get("Content-Length", 0))

            with open(local_path, "wb") as f, tqdm(
                total=total_size,
                unit="B",
                unit_scale=True,
                desc=filename,
                leave=True
            ) as pbar:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))

        ts = int(filename.split("_")[1].split(".")[0])
        human = datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
        print(f"Downloaded {filename} ({human})")

def main():
    parser = argparse.ArgumentParser(description="Download files from OpenStack Swift within a specified time range.")
    parser.add_argument(
        "--base_url",
        required=False,
        default="https://airlab-cloud.andrew.cmu.edu:8080/swift/v1/AUTH_ac8533a83cff4d48bc8c608ad222d330/amelia_swim/",
    )
    parser.add_argument("--start_time", default="2023-01-01 00:00:00", help='Start time in the format YYYY-MM-DD HH:MM:SS (default: 2023-01-01 00:00:00)')
    parser.add_argument("--end_time", default="2023-01-02 00:00:00", help='End time in the format YYYY-MM-DD HH:MM:SS (default: 2023-01-02 00:00:00)')
    parser.add_argument("--destination", required=False, default="swim_data/", help='Local directory to save the downloaded files')
    args = parser.parse_args()

    downloader = SwiftFileDownloader(args.base_url)
    downloader.download_files(args.start_time, args.end_time, args.destination)


if __name__ == "__main__":
    main()
