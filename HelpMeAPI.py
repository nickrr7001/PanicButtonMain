from flask import Flask, jsonify, request
from twilio.rest import Client
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)
@app.route('/')
def TestConnect():
    return "Conencted!"
@app.route("/sendLocation",methods=["POST"])
def LocationSend():
    print ("Location send called!")
    data = request.get_json()
    print (data)
    userID = data["userid"]
    print(userID)
    location = data["location"]
    print ("user data collected")
    dataFile = open("dataHolder.txt","r").read().split('\n')
    print ("file opened")
    emergencyPhone = ""
    for line in dataFile:
        datasec = line.split("|")
        if (datasec[0] == userID):
            datasec[2] = location
            emergencyPhone = datasec[4]
            line = "|".join(datasec)
            break
    print("for loop complete!")
    open("dataHolder.txt","w").write("\n".join(dataFile))
    print ("file written")
    notifyPolice = data["notify police"]
    
    msg = "ALERT! {} IS IN TROUBLE! LOCATION: {}".format(userID,location)
    if (emergencyPhone != ""):
        sendTextMSG(msg,emergencyPhone)
    if (notifyPolice):
        sendTextMSG(msg,"+13173191985")
    print ("notifed!")
    return "Complete"
@app.route("/endHelp",methods=["POST"])
def endHelp():
    data = request.get_json()
    userID = data["userid"]
    dataFile = open("dataHolder.txt","r").read().split('\n')
    found = False
    for line in dataFile:
        datasec = line.split("|")
        if (datasec[0] == userID and datasec[1] == data["password"]):
            datasec[2] =  "NO_LOCATION"
            line = "|".join(datasec)
            found = True
            break
    if (found == False):
        return "Incorrect Password!"
    else:
        sendTextMSG(userID + " is safe!","+13173191985")
    open("dataHolder.txt","w").write("\n".join(dataFile))
    return "Ended!"
@app.route("/register",methods=["POST"])
def RegisterUser():
    try:
        print ("Registering User!")
        data = request.get_json()
        print (data)
        userID = data["userid"]
        password = data["password"]
        print ("e contacts")
        emergencyContactname = data["contact name"]
        emergencyContactphone = data["contact phone"]
        emergencyContactname = data["contact email"]
        print ("open file")
        dataFile = open("dataHolder.txt","a")
        dataFile.write(userID + "|" + password + "|" + "NO_LOCATION" + "|" + emergencyContactname+ "|" + emergencyContactphone + "|" + emergencyContactname +'\n')
        return "Registered!"
    except:
        return "Registration Error!"
def sendTextMSG(message,phone):
    account_sid = 'AC757ad136e22280293939be6c13fba6bd'
    auth_token = 'ce2ee24ae81bb49a7f7ae2539d33ed75'
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body=message,
                        from_='+12056289978',
                        to=phone
                    )
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)