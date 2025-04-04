import os
import zipfile
import urllib.request
import shutil

# Sequence ID to KITTI drive mapping
files = {
    '00': '2011_10_03_drive_0027',
    '01': '2011_10_03_drive_0042',
    #'02': '2011_10_03_drive_0034',
    #'03': '2011_09_26_drive_0067',
    #'04': '2011_09_30_drive_0016',
    #'05': '2011_09_30_drive_0018',
    #'06': '2011_09_30_drive_0020',
    #'07': '2011_09_30_drive_0027',
    #'08': '2011_09_30_drive_0028',
    #'09': '2011_09_30_drive_0033',
    #'10': '2011_09_30_drive_0034'
}

BASE_URLS = [
    "https://s3.eu-central-1.amazonaws.com/avg-kitti/raw_data/",
    "http://kitti.is.tue.mpg.de/kitti/raw_data/"
]

output_dir = "images"
os.makedirs(output_dir, exist_ok=True)

def download_file(url, filename):
    try:
        print(f"Downloading: {url}")
        urllib.request.urlretrieve(url, filename)
        print("Download complete.")
        return True
    except Exception as e:
        print(f"Download failed from {url} with error: {e}")
        return False

def process_sequence(seq_id, drive_name):
    zip_filename = f"{drive_name}_sync.zip"
    drive_folder = f"{drive_name}/{drive_name}_sync"

    # Try downloading from URLs
    downloaded = False
    for base_url in BASE_URLS:
        url = base_url + drive_name + '/' + zip_filename
        if download_file(url, zip_filename):
            downloaded = True
            break

    if not downloaded:
        print(f"Failed to download sequence {seq_id}")
        return

    # Extract the zip
    print(f"Extracting {zip_filename}...")
    with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
        zip_ref.extractall()

    # Path to image_03
    src_dir = os.path.join(drive_folder, 'image_03', 'data')
    dst_dir = os.path.join(output_dir, seq_id)
    os.makedirs(dst_dir, exist_ok=True)

    if os.path.exists(src_dir):
        for f in sorted(os.listdir(src_dir)):
            shutil.move(os.path.join(src_dir, f), os.path.join(dst_dir, f))
        print(f"Moved images to {dst_dir}")
    else:
        print(f"image_03 not found in {drive_folder}")

    # Cleanup
    shutil.rmtree(drive_name[:10], ignore_errors=True)
    os.remove(zip_filename)

# Main loop
for seq_id, drive_name in files.items():
    process_sequence(seq_id, drive_name)

print("All done!")
