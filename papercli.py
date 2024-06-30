import requests
import json
import os

ascii_art = open("ascii.txt", "r").read()
print(ascii_art)

projects_response = requests.get("https://api.papermc.io/v2/projects")
global projects

if projects_response.status_code == 200:
    json_data = projects_response.text
    data = json.loads(json_data)
    projects = data['projects']

    for p in projects:
        print(p)
else:
    print(f"Failed to connect to Paper API. Status code: {projects_response.status_code}")

while True:
    software_to_download = input("\nSelect the server software you want to download: ").lower()
    if software_to_download not in projects:
        print("The server software you specified doesn't exist!")
        exit()
    data = json.loads(requests.get(f"https://api.papermc.io/v2/projects/{software_to_download}").text)
    versions = data['versions']

    for v in versions:
        print(v)
    
    while True:
        version_to_download = input("\nSelect the version you want to download: ").lower()
        if version_to_download not in versions:
            print("The version you specified doesn't exist!")
        else: 
            data = json.loads(requests.get(f"https://api.papermc.io/v2/projects/{software_to_download}/versions/{version_to_download}").text)
            builds = data['builds']

            for b in builds:
                print(b)
            
            while True:
                build_to_download = input("\nSelect the build you want to download (Leave empty to download the latest build): ")
                if build_to_download == '':
                    build_to_download = max(builds)
                file_name = json.loads(requests.get(f"https://api.papermc.io/v2/projects/{software_to_download}/versions/{version_to_download}/builds/{build_to_download}").text)['downloads']['application']['name']
                downloaded_file = requests.get(f"https://api.papermc.io/v2/projects/{software_to_download}/versions/{version_to_download}/builds/{build_to_download}/downloads/{file_name}", stream=True)
                if downloaded_file.status_code == 200:
                    file_path = f"./downloads/"
                    if not os.path.exists(file_path):
                        os.makedirs(file_path)

                        with open(file_path + file_name, "wb") as file:
                            for chunk in downloaded_file.iter_content(chunk_size=8192):
                                if chunk:
                                    file.write(chunk)
                        print(f"Downloaded {file_name} successfully!")
                        exit()
                print(f"Failed to download the file. Status code: {downloaded_file.status_code}")
                exit()