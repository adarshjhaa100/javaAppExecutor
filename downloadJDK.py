# Program to download JDK(or any other file) from a given link 
import requests
from tqdm import tqdm
import hashlib

# SHA256: 5AEBB80215094F8FE81CA5E0937FEC8A4E2618B7B3D17A2B83DAA0E79F9890CB
realHash= "fde3b28ca31b86a889c37528f17411cd0b9651beb6fa76cac89a223417910f4b"

def verify_integrity(fileObj,real_hash):
    print("Checking for file integrity")
    hash_of_jdkzip=hashlib.sha256()
    
    # for checking bigger files
    for block in iter(lambda:fileObj.read(4096),b""):
        hash_of_jdkzip.update(block)
    print(hash_of_jdkzip.hexdigest())
    print(realHash)

    if(hash_of_jdkzip.hexdigest()==realHash):
        print("file integrity check successful")
    else:
        print("file integrity check failed")
    

filePath="./sampleDown/jdk11_2.zip"
# Method downlaods file from a given link and shows progress bar
def download_file(path,justCheck=False): 
    print("Establishing connection")

    # In streaming mode, file is downloaded in chunks
    res=requests.get(path,stream=True)          # Establish connection
    totalSize=int(res.headers.get('content-length',0))      # size in bytes
    block_size=512*1024 # 512KB block size

    # skip downloading if just checking for files
    if(justCheck==False):
        # elegant progress bar using tqdm, unit is the type of progress(here bytes) 
        progressBar=tqdm(total=totalSize, unit='iB', unit_scale=True)
        with open(filePath,"wb") as f:
            # iterate in content for each block size
            for data in res.iter_content(block_size):
                #set precision up inside fstring
                progressBar.update(len(data))
                # print(f"downloaded {(downloaded*100/totalSize):0.1f}% ")
                f.write(data)
            f.close()
        print("Download over")
        
        # Send file for integrity check
        f=open(filePath,"rb")
        real_hash=""
        verify_integrity(f, real_hash)
    
    else:
        print(res.headers)
        print("\nwas just checking for file info")


        
url="https://download.java.net/openjdk/jdk11/ri/openjdk-11+28_windows-x64_bin.zip"
# url="http://download.nust.na/pub2/FreeStuff/Software/Audio/Audacity/audacity-win-1.2.6.exe"
download_file(url,False)
