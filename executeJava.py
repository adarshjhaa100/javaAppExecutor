# program to verify whether java command is working and then java files using it
import subprocess

bin_java="/bin/java"

# checks for java version
def verify_java_command(path):
    try:
        # Run command and get output/error using subprocess.run
        # If just want to run commands w/o output, use subprocess.call([args]) 
        command=subprocess.run([path+bin_java,"-version"],capture_output=True)
        # why is the output inside stderr?
        output=command.stderr.decode('utf-8')

        if(output.find("openjdk version")):
            return True
        # print(output.find("openjdk version"))
    except FileNotFoundError:
        print("file not found")
        return False

# javatype=JAR, java etc
def run_java(jdkPath, javaFilePath,javaType):
    if(verify_java_command(jdkPath)):
        # do we need output? 
        command=subprocess.run([jdkPath+bin_java,javaFilePath],capture_output=True)
        # here the output is inside stdout!! Ha Ha
        javaOutput=command.stdout.decode('utf-8')
        print(javaOutput)
    else:
        print("Cannot run java command")


run_java("./sampleDown/jdk-11","./sampleJavaFiles/HelloWorld.java","java")

