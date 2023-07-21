## Created by Jonirulah
## FiveM Artifacts Updater v1.0.0 for Linux.
## This will update your server artifacts within 10 seconds.
## Use at your own responsibility.

import requests
from bs4 import BeautifulSoup
import re
import os
import tarfile
from tabulate import tabulate
import time
import subprocess
import shutil

FIVEM_DIRECTORY = "/fivem/myserver"
CACHE_DIRECTORY = "/fivem/myserver/server-data/cache"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def download_and_extract(url, destination_dir):
    # Download the fx.tar.xz file
    print(bcolors.ENDC + "Downloading: ", url)
    response = requests.get(url, stream=True)
    response.raise_for_status()
    total_size = int(response.headers.get('Content-Length', 0))
    
    # Create the destination directory if it doesn't exist
    os.makedirs(destination_dir, exist_ok=True)

    # Save the downloaded file to the destination directory
    filepath = os.path.join(destination_dir, 'fx.tar.xz')
    with open(filepath, 'wb') as file:
        downloaded_size = 0
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
            downloaded_size += len(chunk)

            # Calculate and display the download progress
            progress = (downloaded_size / total_size) * 100
            print(bcolors.ENDC + f"Download progress: {progress:.2f}% - {downloaded_size / 1024 / 1024}/{total_size / 1024 / 1024} MB", end='\r')


    print(bcolors.BOLD + "# WARNING!")
    print(bcolors.WARNING + "This process will stop the FiveM service if your server is running a rollback and data loss will occur!")
    time.sleep(1)
    cont = str(input(bcolors.WARNING + "Do you want to continue? (y/n or CTRL+C to exit forcefully): ")).lower()
    if cont != "y":
        os._exit(0)

    # Stop FiveM Service
    try:
        subprocess.run(['sudo', 'systemctl', 'stop', 'fivem'], check=True)
        print(bcolors.OKGREEN + "FiveM has been stopped successfully!")
        delete_cache(select_cache, CACHE_DIRECTORY)
    except:
        print(bcolors.FAIL +"An error has occurred while trying to stop the FiveM service!")
        print("Please contact a system administrator or developer!")
        return
    
    # Extract the downloaded fx.tar.xz file
    print(bcolors.ENDC + "Extracting in: ", filepath)
    with tarfile.open(filepath, 'r:xz') as tar:
        tar.extractall(destination_dir)

    # Start FiveM Service
    try:
        subprocess.run(['sudo', 'systemctl', 'start', 'fivem'], check=True)
        print(bcolors.OKGREEN + "FiveM has been started successfully!")
    except:
        print(bcolors.FAIL + "An error has occurred while trying to start the FiveM service!")
        print("Please contact a system administrator or developer!")
        return
    
def delete_folder(folder):
    try:
        # Use shutil.rmtree to delete the folder and its contents
        shutil.rmtree(folder)
        print(bcolors.ENDC + f"Folder '{folder}' has been deleted successfully.")
    except OSError as e:
        print(bcolors.ENDC + f"Error while deleting folder '{folder}': {e}")

def delete_cache(cache, folder):
    # Delete Cache of the server
    if cache == "y":
        delete_folder(folder)
    else:
        return

req = requests.get("https://runtime.fivem.net/artifacts/fivem/build_proot_linux/master/", timeout=5)
soup = BeautifulSoup(req.text, 'lxml')


select_build = str(input("Do you wanna select a build? (y/n): ")).lower()
select_cache = str(input("Do you wanna delete the FiveM server cache? (y/n): ")).lower()

if (select_build) == "y":
    # Download Custom Build
    link = soup.find_all('a', class_='panel-block')
    builds = soup.find_all('div', class_='level-left')
    dates = soup.find_all('div', class_='level-item')
    print(bcolors.ENDC + "Last builds: (order by date) [INFO: You can choose any other not listed here.]")
    data = []

    time.sleep(1)

    # Just for pretty printing, show information to the administrator regarding last updates.
    for build in range(15): # You can change it to whatever you want.
        build_version = re.findall(r"[0-9].*", builds[build].text)[0]
        date = dates[build].text
        data.append([build_version, date, link[build+1]['href'][1:]])
    print(tabulate(data, headers=['Build', 'Release Date', 'URL'], tablefmt='fancy_grid', colalign=("center","center","center")))

    time.sleep(1)

    # Choose a build number, and look for it. (search method could be improved ikr)
    selected_build = int(input("\nEnter build number: "))
    found = False

    for build in range(len(builds)):
        build_version = re.findall(r"[0-9].*", builds[build].text)[0]
        if int(build_version) == int(selected_build):
            print(bcolors.OKGREEN + "Build has been found!", link[build+1]['href'][1:])
            build_url = "https://runtime.fivem.net/artifacts/fivem/build_proot_linux/master" + link[build+1]['href'][1:]
            found = True
            download_and_extract(build_url, FIVEM_DIRECTORY)
            break
    if not found:
        print(bcolors.FAIL + "Build has not been found!")
else:
    # Download Last Build
    last_build = soup.find('div', class_='level-left').text
    last_build_version = re.findall(r"[0-9].*", last_build)[0]
    url = soup.find('a', class_='is-active')['href'][1:]
    last_build_url = "https://runtime.fivem.net/artifacts/fivem/build_proot_linux/master" + url
    print(bcolors.OKGREEN + "Build has been found!", last_build_version)
    download_and_extract(last_build_url, FIVEM_DIRECTORY)