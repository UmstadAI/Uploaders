import zipfile
import requests
import shutil
import os

def download_github_folder(username, repository, branch, folder_path, target_directory):
    url = f"https://github.com/{username}/{repository}/archive/{branch}.zip"
    response = requests.get(url, stream=True)

    os.makedirs('examples')
    if response.status_code == 200:
        zip_file_path = os.path.join(target_directory, f"{repository}-{branch}.zip")
        with open(zip_file_path, 'wb') as zip_file:
            for chunk in response.iter_content(chunk_size=128):
                zip_file.write(chunk)

        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(target_directory)
            extracted_folder_path = os.path.join(target_directory, f"{repository}-{branch}", folder_path)
            shutil.move(extracted_folder_path, os.path.join(target_directory, folder_path))

        os.remove(zip_file_path)
        shutil.rmtree(os.path.join(target_directory, f"{repository}-{branch}"))

        print(f"Downloaded {folder_path} successfully.")
    else:
        print(f"Failed to download {folder_path}. Status code: {response.status_code}")

download_github_folder('o1-labs', 'o1js', 'main', 'src/examples', 'examples')
