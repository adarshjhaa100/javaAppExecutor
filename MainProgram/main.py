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
        self.binPath=""

    # try to create a different child process for this
    # download, verify integrity(sha256) and unzip
    def download_jdk(self):
        if(os.path.isfile(self.path)):
            self.binPath=""
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


    # integrity check for jdk(sha256)
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

    # checks for java version
    def verify_java_command(self, showOutput=True):
        try:
            # Run command and get output/error using subprocess.run
            # If just want to run commands w/o output, use subprocess.call([args]) 
            if(len(self.binPath)==0):
                self.binPath=BASE_PATH+"/"+self.name+"/jdk-11"+BIN_JAVA
            
            binPath=self.binPath
            command=subprocess.run([binPath,"-version"],capture_output=True)
            
            # why is the output inside stderr?
            output=command.stderr.decode('utf-8')
            if(showOutput):
                print(output)
            
            # will be done once per jdk
            if(output.find("openjdk version")>-1):
                self.binPath=BASE_PATH+"/"+self.name+"/jdk-11"+BIN_JAVA
                return True

        except FileNotFoundError:
            print("file not found")
            return False

    # please choose JAR files to run,.java is fine until you use builtin dependencies, 
    # I dont guarentee of adding external dependencies
    # Please for now add the absolute path of the java application
    def run_java(self,java_file_path,mode):
        command=""
        print("executing java file")
        # check if java runs
        if(self.verify_java_command()==False):
            return "Cannot Run the java command"    
        
        if(mode=="JAR"):
            command=subprocess.run([self.binPath,"-jar",java_file_path], capture_output=True)
        else:
            command=subprocess.run([self.binPath,java_file_path],capture_output=True)
        print(command.stdout.decode())
        return "successfully ran the java command"

# name, url, checksum, path
jdk={"name":"openjdk-11",
     "insidefoldername":"jdk-11",
    "url":"https://download.java.net/openjdk/jdk11/ri/openjdk-11+28_windows-x64_bin.zip",
    "checksum":"fde3b28ca31b86a889c37528f17411cd0b9651beb6fa76cac89a223417910f4b"}


# function to load jdk lists
def load_jdk_list():
    # only create jdk object if we can verify bin path
    pass




# Main code
if __name__=="__main__":
    jdk1=JDK(jdk["name"], jdk["url"], jdk["checksum"],jdk["insidefoldername"])
    # the dict object of a python class can be obtained using
    # print(jdk1.__dict__)
    jdk1.download_jdk()
    jdk1.verify_java_command()

    jdk1.run_java("D:/cs/PythonMaterial/HobbyProjects/javaAppExecutor/sampleJavaFiles/HelloWorld.java",mode="JAVA")
    # print(jdk1.__dict__)
