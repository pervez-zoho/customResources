import os,sys
import getpass

if(input("Do you want to clean the existing databases ?\n(Y/n) >>> ").lower()=="y"):
    os.system("python3 /home/local/ZOHOCORP/sayad-pt5854/ZohoWorkspace/customResources/refreshMysql.py")

httpsconfig = '''Connector port="7448"
 maxThreads="150"
 minSpareThreads="25"
 maxSpareThreads="75"
 enableLookups="false"
 disableUploadTimeout="true"
 useBodyEncodingForURI="true"
 acceptCount="100"
 connectionTimeout="20000"
 debug="4"
 scheme="https"
 secure="true"
 clientAuth="false"
 sslProtocol="TLS"
 SSLEnabled="true"
 keystoreFile="conf/sas.keystore"
 keystoreType="JKS"
 keystorePass="Awqg+@fa9XQjX3"
  />
'''

privateKey = '''<?xml version="1.0" encoding="UTF-8"?>
<!-- Generated Time : 2020-03-16 19:28:09.744 & Service Name : APIGateway -->
    <security xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="security.xsd">
        <properties>
            <property name="internalrequest.privatekey" value="30820153020100300d06092a864886f70d01010105000482013d30820139020100024100dba9ad4161df6c1ed6dd3c7e5a94227e9fe001d779aaf28aae4707bce2dceeb87c4e925fac31440ace85eef41001c4006877552af4b6df81fb2eac62f7b71bf5020301000102401d875fbd0c552689b6c4a2df3179fc711d38d5c68b9a89644f2d49430114461ad2f3838cc489493bcb6a2fa45d13abfc1e80a7493072069aedea968f4a006fb9022100f9bf46796ddae5119bc836e8ec8ab4ee5747216ca3aedeede17c23368e386e0b022100e129944dafe4e0a80cbbe2f99ff2b2c9ee69a06cabf278096bc559fcaec6ddff0220054d0102ecc8fb99af13c5ce95ceafde6b2dd050ccfc9630b85b7927dc46e857022016f6c2a559b722228189f810357bef382114acc3e89586208fd944e03c8313c90220664d23591886a3dc57f8ee2be9e50f4b5cabd8d9ecb0593859957aa8e30a547b"/>
        </properties>
    </security>
'''

if(len(sys.argv)<=1):

    try:
        zipfilename = [_ for _ in os.listdir() if _.endswith(".zip")][0]
        zipfilename = "./"+zipfilename if input(f"Is {zipfilename} your output ZIP file ? (y/n)\n>>> ").lower()=="y" else input("Enter filepath :\n>>> ")
        zipfilename = zipfilename+".zip" if(not zipfilename.endswith(".zip")) else zipfilename
    except Exception as e:
        zipfilename = input("Enter filepath :\n>>> ")

else:
    zipfilename = sys.argv[1]

try:
    os.system(f'''unzip {zipfilename} -d ./{zipfilename.replace(".zip","")}''')
except Exception as e:
    print("Initial unzip failed\n")
    print(e)

try:
    myDbName = input("Enter your database name :")
    myDbPasswd = getpass.getpass("Enter your database password :")
    myDbName = myDbName if myDbName!="" else "jbossdbpvz"
    myDbPasswd = myDbPasswd if myDbPasswd!="" else "sas"
except Exception as e:
    print("Database getpass failed\n")
    print(e)  

os.chdir(f'{zipfilename.replace(".zip","")}/AdventNet/Sas/tomcat/conf/')

try:
    os.remove("sas.keystore")
    os.system(f'cp /home/local/ZOHOCORP/sayad-pt5854/ZohoWorkspace/Java/Resources/sas.keystore ./sas.keystore')
except Exception as e:
    print("Error in copying sas.keystore\n")
    print(e)

try:
    with open("./server.xml.orig","r") as f:
        overallcontent = f.read().replace("8080","7085")
        li = overallcontent.split("<")
        for index,_ in enumerate(li):
            if(("Connector" in _) and ("port" in _) and ("8443" in _) and ("secure" in _)):
                li[index] = httpsconfig
        contents = "<".join(li)
    with open("./server.xml.orig","w") as f1:
        f1.write(contents)
    with open("./server.xml","w") as f2:
        f2.write(contents)
except Exception as e:
    print("Error in writing to server.xml & server.xml.orig file\n")
    print(e)

try:
    os.chdir("../")
    os.mkdir("logs")
    tomcatpath = os.getcwd()
except Exception as e:
    print("Error in creating logs file under tomcat\n")
    print(e)

try:
    os.chdir("webapps/")
    os.remove("grid.war")
    zipfilename = "ROOT.war"
    os.system(f'''unzip {zipfilename} -d ./{zipfilename.replace(".war","")}''')
except Exception as e:
    print("Error in deleting grid.war and extracting root.war\n")
    print(e) 

try:
    os.chdir("ROOT/")
    rootpath = os.getcwd()
    os.chdir("WEB-INF/")
    webinfpath = os.getcwd()
    os.chdir("conf/")
    webinfconfpath = os.getcwd()
    with open("security-privatekey.xml","w+") as f3:
        f3.write(privateKey)
except Exception as e:
    print("Error in creating security-privatekey.xml\n")
    print(e) 

try:
    with open("configuration.properties","r") as f4:
        rawdata = f4.readlines()
        for index,_ in enumerate(rawdata):
            if("app.home" in _):
                rawdata[index] = f'''app.home={webinfpath}'''
            elif("app.context" in _):
                rawdata[index] = f'''app.context={rootpath}'''
            elif("production=true" in _):
                rawdata[index] = "production=false"
            elif("db.password" in _):
                rawdata[index] = f'''db.password={myDbPasswd}'''
            elif("db.schemaname" in _):
                rawdata[index] = f'''db.schemaname={myDbName}'''

        with open("configuration.properties","w") as f5:
            f5.write("\n".join(rawdata))

except Exception as e:
    print("Error in editing configuration.properties\n")
    print(e) 

try:
    os.chdir("SAS/")
    with open("./provisioning-configuration.xml","r") as f6:
        x = f6.read().replace('''<GridConfiguration propname="mysql-root-password" propval=""/>''',f'''<GridConfiguration propname="mysql-root-password" propval="{myDbPasswd}"/>''')
    with open("./provisioning-configuration.xml","w") as f7:
        f7.write(x)
except Exception as e:
    print("Error in editing provisioning-configuration.xml\n")
    print(e) 
