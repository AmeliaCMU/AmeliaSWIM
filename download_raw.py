import argparse
import os
import time
import requests
from datetime import datetime
from tqdm import tqdm
from urllib.parse import urljoin


class SwiftFileDownloader:
    def __init__(self, base_url):
        """
        base_url example:
        https://airlab-cloud.andrew.cmu.edu:8080/swift/v1/AUTH_xxx/amelia_swim/
        """
        if not base_url.endswith("/"):
            base_url += "/"
        self.base_url = base_url

    def download_files(self, start_time, end_time, destination_folder, time_format="human"):
        # Ensure output directory exists
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

        # loop over prefixes ALL1_ to ALL8_
        for i in range(1, 9):
            prefix = f"ALL{i}_"
            print(f"\n🔍 Checking prefix: {prefix}")

            # List files under this prefix
            file_list = self._list_objects(prefix)

            for fname in file_list:
                try:
                    file_timestamp = int(fname.split("_")[1].split(".")[0])
                except Exception:
                    continue

                if start_timestamp <= file_timestamp <= end_timestamp:
                    self._download_file(fname, destination_folder)

    def _list_objects(self, prefix):
        """Fetch file list by scraping the Swift directory index."""
        list_url = urljoin(self.base_url, f"?prefix={prefix}")
        resp = requests.get(list_url)

        if resp.status_code != 200:
            print(f"Failed to list prefix: {prefix}")
            return []

        # Swift returns plain text, one file per line
        files = resp.text.strip().split("\n")
        files = [f for f in files if f.startswith(prefix)]

        print(f"Found {len(files)} files for {prefix}")
        return files

    def _download_file(self, filename, destination_folder):
        local_path = os.path.join(destination_folder, filename)

        if os.path.exists(local_path):
            print(f"✔ {filename} already exists, skipping.")
            return

        url = urljoin(self.base_url, filename)
        print(f"⬇ Downloading {filename}")

        with requests.get(url, stream=True) as r:
            if r.status_code != 200:
                print(f"❌ Failed: {filename} ({r.status_code})")
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
        print(f"✔ Downloaded {filename} ({human})")


def main():
    parser = argparse.ArgumentParser(description="Download files from OpenStack Swift time range.")
    parser.add_argument(
        "--base_url",
        required=False,
        default="https://airlab-cloud.andrew.cmu.edu:8080/swift/v1/AUTH_ac8533a83cff4d48bc8c608ad222d330/amelia_swim/",
    )
    parser.add_argument("--start_time", default="2023-01-01 00:00:00")
    parser.add_argument("--end_time", default="2023-01-02 00:00:00")
    parser.add_argument("--destination", default="swim_data/")
    args = parser.parse_args()

    downloader = SwiftFileDownloader(args.base_url)
    downloader.download_files(args.start_time, args.end_time, args.destination)


if __name__ == "__main__":
    main()
