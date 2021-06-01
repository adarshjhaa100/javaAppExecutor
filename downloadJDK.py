# Program to download JDK(or any other file) from a given link 
import requests
from tqdm import tqdm


# Method downlaods file from a given link and shows progress bar
def download_file(path): 
    print("Establishing connection")
    res=requests.get(path,stream=True)          # Establish connection
    
    totalSize=int(res.headers.get('content-length',0))      # size in bytes
    block_size=512*1024 # 512KB block size

    # elegant progress bar using tqdm, unit is the type of progress(here bytes) 
    progressBar=tqdm(total=totalSize, unit='iB', unit_scale=True)

    with open("./sampleDown/jdk11_2.zip","wb") as f:
        # iterate in content for each block size
        for data in res.iter_content(block_size):
            #set precision up inside fstring
            progressBar.update(len(data))
            # print(f"downloaded {(downloaded*100/totalSize):0.1f}% ")
            f.write(data)
        
        f.close()

        

download_file("https://download.java.net/openjdk/jdk11/ri/openjdk-11+28_windows-x64_bin.zip")
