# Program to unzip jdk file
import zipfile

def unzip(jdkDir, jdkName):
    with zipfile.ZipFile(jdkDir+jdkName+".zip","r") as zip:
        zip.extractall(jdkDir)

unzip("./sampleDown/", "jdk11_2")