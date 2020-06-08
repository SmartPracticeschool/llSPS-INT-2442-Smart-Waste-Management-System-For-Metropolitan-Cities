import time
import sys
import random

import ibmiotf.application
import ibmiotf.device


#Provide your IBM Watson Device Credentials
organization = "q2va6d" # repalce it with organization ID
deviceType = "rsip" #replace it with device type
deviceId = "108" #repalce with device id
authMethod = "token"
authToken = "9110705023"#repalce with token


def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data)        
        if cmd.data['command']=='cover':
                print("the bin lid is closed")
        elif cmd.data['command'] == 'uncover':
            print("the bin lid is open")
                
try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
	#..............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

deviceCli.connect()



while True:
        
        L = random.randint(0, 100);
        F = random.randint(0, 100);
        Q = random.randint(0, 100);
        W = random.randint(0, 100);
        E = random.randint(0, 100);
        R = random.randint(0, 100);
        T = random.randint(0, 100);
        Y = random.randint(0, 100);
        lat=17.3984
        lon=78.5583
      
       
        data = {'d':{ 'garbagelevel' : L, 'garbageweight': F,'lat': lat,'lon': lon,'a' : Q, 'b' : W, 'c' : E, 'd' : R,'e' : T, 'f' : Y, 'g' : Y}}
        u=time.asctime(time.localtime(time.time()))
        print(u)
        
        

        #print data
        def myOnPublishCallback():
            print ("Published Your Garbage Level = %s %%" % L, "Garbage Weight = %s %%" % F, "to IBM Watson")
            print ("Published Your Garbage Level of bin2 = %s %%" % Q, "Garbage Weight of bin2 = %s %%" % W, "to IBM Watson")
            print ("Published Your Garbage Level of bin3 = %s %%" % E, "Garbage Weight of bin3 = %s %%" % R, "to IBM Watson")
            print ("Published Your Garbage Level of bin4 = %s %%" % T, "Garbage Weight of bin4 = %s %%" % Y, "to IBM Watson")

        success = deviceCli.publishEvent("event", "json", data, qos=0, on_publish=myOnPublishCallback)
        if not success:
            print("Not connected to IoTF")
            
        time.sleep(5)
        deviceCli.commandCallback = myCommandCallback
        from cloudant.client import Cloudant
        from cloudant.error import CloudantException
        from cloudant.result import Result, ResultByKey
        client = Cloudant("fa3c80de-84b9-4280-be10-e9ee55d6726b-bluemix", "cd3fd31f55919b590bdd100e21c3278805fab74817ca0ca86c68309a46585792",
                  url="https://fa3c80de-84b9-4280-be10-e9ee55d6726b-bluemix:cd3fd31f55919b590bdd100e21c3278805fab74817ca0ca86c68309a46585792@fa3c80de-84b9-4280-be10-e9ee55d6726b-bluemix.cloudantnosqldb.appdomain.cloud")
        client.connect()
        database_name = "dustmanagement"
        my_database = client.create_database(database_name)
        if my_database.exists():
            print(f"'{database_name}' successfully created.")
            json_document = {'d':{ 'Garbage Level' : L, 'Garbage Weight': F }}
            json_document = {'d':{ 'Garbage Level' : Q, 'Garbage Weight': W }}
            json_document = {'d':{ 'Garbage Level' : E, 'Garbage Weight': R }}
            json_document = {'d':{ 'Garbage Level' : T, 'Garbage Weight': Y }}
            new_document = my_database.create_document(json_document)
            if new_document.exists():
                print(f"Document '{new_document}' successfully created.")
        ''' if L>=100:
                print("your garbage is full")
                import requests

                url = "https://www.fast2sms.com/dev/bulk"

                querystring = {"authorization":"G3k8jc6SOWqei20PQZJV4otdarXImlCYAygM9RuUxKnb1BvDhEWbJPYeFM1tLASXNKQzj5xp0Gm3Uw6B","sender_id":"FSTSMS","message":"This is test message","language":"english","route":"p","numbers":"9999999999,8919275560,7777777777"}

                headers = {
                    'cache-control': "no-cache"
                }

                response = requests.request("GET", url, headers=headers, params=querystring)

                print(response.text)'''






# Disconnect the device and application from the cloud
deviceCli.disconnect()
