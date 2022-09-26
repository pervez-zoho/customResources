import os,shutil,sys

if(len(sys.argv)>1):
    if(sys.argv[1]=="old"):
        os.chdir("/home/local/ZOHOCORP/sayad-pt5854/ZohoWorkspace/apigrepo/apigateway/build")
        os.remove("./build.xml")
        shutil.copyfile("/home/local/ZOHOCORP/sayad-pt5854/Documents/build.xml","/home/local/ZOHOCORP/sayad-pt5854/ZohoWorkspace/apigrepo/apigateway/build/build.xml")
    else:
        os.chdir("/home/local/ZOHOCORP/sayad-pt5854/ZohoWorkspace/apigrepo/apigateway/build")
        os.remove("./build.xml")
        shutil.copyfile("/home/local/ZOHOCORP/sayad-pt5854/Documents/build.xml_new","/home/local/ZOHOCORP/sayad-pt5854/ZohoWorkspace/apigrepo/apigateway/build/build.xml")
else:
    print("No Cmd Line Arguements Provided")