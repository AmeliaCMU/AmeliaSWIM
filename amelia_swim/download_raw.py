import argparse
import os
import time
from minio import Minio
from minio.error import S3Error
from datetime import datetime
from tqdm import tqdm


class MinioFileDownloader:
    def __init__(self, endpoint="airlab-share-01.andrew.cmu.edu:9000", bucket_name="ameliaswim"):
        self.client = Minio(endpoint, secure=True)
        self.bucket_name = bucket_name

    def download_files(self, start_time, end_time, destination_folder, time_format="human"):
        # Create destination folder if it doesn't exist
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        if time_format == "human":
            start_timestamp = int(time.mktime(time.strptime(start_time, '%Y-%m-%d %H:%M:%S')))
            end_timestamp = int(time.mktime(time.strptime(end_time, '%Y-%m-%d %H:%M:%S')))
        elif time_format == "unix":
            start_timestamp = start_time
            end_timestamp = end_time
        else:
            print("Time format invalid..")
            raise ValueError("Invalid time format. Use 'human' or 'unix'.")

        pbar = tqdm(range(1, 9), desc="Downloading")
        for i in pbar:
            prefix = f'ALL{i}_'
            pbar.set_postfix({"iteration": i})
            print("For Prefix", prefix, "in 1 to 8")
            objects = self.client.list_objects(self.bucket_name, prefix=prefix)
            for obj in (objects):
                file_timestamp = int(obj.object_name.split('_')[1].split('.')[0])
                # print("Checking", file_timestamp)
                if start_timestamp <= file_timestamp <= end_timestamp:
                    self._download_file(obj.object_name, destination_folder)

    def _download_file(self, object_name, destination_folder):
        file_path = os.path.join(destination_folder, object_name)
        if not os.path.exists(file_path):
            try:
                response = self.client.get_object(self.bucket_name, object_name)
                with open(file_path, "wb") as file_data:
                    for d in response.stream(32 * 1024):
                        file_data.write(d)
                response.close()
                response.release_conn()
                # Get timestamp from the object name and convert it to human-readable format
                timestamp = int(object_name.split('_')[1].split('.')[0])
                human_readable_time = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                print(f"\nDownloaded {object_name} ({human_readable_time})")
            except S3Error as err:
                print(f"Failed to download {object_name}: {err}")
        else:
            print(f"File {object_name} already exists, skipping download.")


def main():
    parser = argparse.ArgumentParser(
        description='Download files from a MinIO bucket within a specified time range.')
    parser.add_argument('--endpoint', required=False,
                        default="airlab-share-01.andrew.cmu.edu:9000", help='MinIO server endpoint')
    parser.add_argument('--bucket', required=False, default="ameliaswim",
                        help='Name of the bucket to download files from')
    parser.add_argument('--start_time', default='2023-01-01 00:00:00',
                        help='Start time in the format YYYY-MM-DD HH:MM:SS (default: 2023-01-01 00:00:00)')
    parser.add_argument('--end_time', default='2023-01-02 00:00:00',
                        help='End time in the format YYYY-MM-DD HH:MM:SS (default: 2023-01-02 00:00:00)')
    parser.add_argument('--destination', required=False, default="out/raw",
                        help='Local directory to save the downloaded files')

    args = parser.parse_args()

    downloader = MinioFileDownloader(args.endpoint, args.bucket)
    downloader.download_files(args.start_time, args.end_time, args.destination)


if __name__ == '__main__':
    main()
