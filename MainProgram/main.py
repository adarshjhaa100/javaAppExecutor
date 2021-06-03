import requests
from tqdm import tqdm
import os
import hashlib
import zipfile
import subprocess

# os.path.isfile()

BIN_JAVA="/bin/java"

# Create a base dir for JDKs. Run only once
BASE_PATH="./JDKs"
# os library is one way to run terminal commands like mkdir in pythoh w/o any error
if(~os.listdir().__contains__(BASE_PATH)):
    try:
        os.mkdir(BASE_PATH)
    except FileExistsError:
        pass    

# class to store properties of JDK
class JDK:
    def __init__(self,name, url, checksum,internalFolder):
        self.name:str=name
        self.url:str=url
        self.checksum:str=checksum
        self.path:str=BASE_PATH+"/"+self.name+".zip" #should i take a path or generate it?
        self.downloaded:bool=False
        self.internalFolder=internalFolder

    # try to create a different child process for this
    def download_jdk(self):
        if(os.path.isfile(self.path)):
            print("jdk file already exists skipping download")
            return True

        print("Establishing Connection")
        # Allow streaming for big files which will download it in chunks
        response=requests.get(self.url, stream=True)
        fileSize=int(response.headers.get('content-length',0))
        # chunk of 512kb
        chunk_size=1024*512
        print("downloading..")

        #twdm progress bar
        progressBar=tqdm(total=fileSize, unit='iB', unit_scale=True)
        with open(self.path,"wb") as f:
            # iterate in content for each block size
            for data in response.iter_content(chunk_size):
                progressBar.update(len(data))
                f.write(data)
            f.close()
        print("Download over")
        
        # Send file for integrity check
        file=open(self.path,"rb")

        # unzip if if file integrity check successful
        if(self.verify_integrity(file, self.checksum)):
            self.unzip()
            print(f"File {self.name} unzipped")
        
        # store that file is downloaded
        self.downloaded=True
        return False


    # integrity check for jdk
    def verify_integrity(self,file,hash):
        print("Checking for file integrity")
        hash_of_jdkzip=hashlib.sha256()
        
        # for checking bigger files
        for block in iter(lambda:file.read(4096),b""):
            hash_of_jdkzip.update(block)
    
        if(hash_of_jdkzip.hexdigest()==hash):
            return True
        else:
            return False
    
    # unzip the donwloaded file
    def unzip(self):
        with zipfile.ZipFile(self.path,"r") as zip:
            zip.extractall(BASE_PATH+"/"+self.name)
            # zip.extractall(BASE_PATH)

    # checks for java version
    def verify_java_command(self):
        try:
            # Run command and get output/error using subprocess.run
            # If just want to run commands w/o output, use subprocess.call([args]) 
            print(BASE_PATH+"/"+self.name+"/jdk11"+BIN_JAVA)
            command=subprocess.run([BASE_PATH+"/"+self.name+"/jdk-11"+BIN_JAVA,"-version"],capture_output=True)
            # why is the output inside stderr?
            output=command.stderr.decode('utf-8')
            print(output)
            if(output.find("openjdk version")):
                return True
        except FileNotFoundError:
            print("file not found")
            return False


# name, url, checksum, path
jdk={"name":"openjdk-11",
     "insidefoldername":"jdk-11",
    "url":"https://download.java.net/openjdk/jdk11/ri/openjdk-11+28_windows-x64_bin.zip",
    "checksum":"fde3b28ca31b86a889c37528f17411cd0b9651beb6fa76cac89a223417910f4b"}


# Main code
if __name__=="__main__":
    jdk1=JDK(jdk["name"], jdk["url"], jdk["checksum"],jdk["insidefoldername"])
    # the dict object of a python class can be obtained using
    # print(jdk1.__dict__)
    jdk1.download_jdk()
    jdk1.verify_java_command()
