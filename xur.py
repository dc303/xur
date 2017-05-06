# where is xur, what's he got, and where is trials?

import requests
import os,sys,traceback
import sendgrid
from sendgrid.helpers.mail import *
from time import sleep

bungo_apiKey=os.environ.get('BUNGIE_API_KEY')
bungo_authHeader = {'X-API-Key': bungo_apiKey}
sg_apiKey = os.environ.get('SENDGRID_API_KEY')
emailTarget = "ninja-chemists@googlegroups.com"
emailSender = "xur@ninjachemists.com"
emailSubject = "TGIF: Update from the Nine"


bungie_base_url = "https://www.bungie.net/Platform/Destiny/"
xur_url = bungie_base_url + "Advisors/Xur/"
hashType = "6"
whereIsXur_url = "https://tellmewhereisxur.com/api"
# ^^ is borked
whereIsTrials_url = "http://api.destinytrialsreport.com/currentMap/"

DEBUG = 1

def sendMail():
    try:
        sg = sendgrid.SendGridAPIClient(apikey=sg_apiKey)
        from_email = Email(emailSender)
        subject = emailSubject
        to_email = Email(emailTarget)
        content = Content("text/plain", "Hello, Guardian!\n\nTrials this week is on " + whereIsTrials() + "\n\nI'm hiding out " + whereIsXur() + "\n\n\nHere's what I've got for you this week:\n\n\n\n" + getXurInventory() + "\n\nSorry this email is so ugly. The Nine won't let me use HTMl and inline CSS\n\n")
        mail = Mail(from_email, subject, to_email, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        if DEBUG == 1:
            print content.value
            print(response.status_code)
            print(response.body)
            print(response.headers)
    except Exception:
        traceback.print_exc(file=sys.stdout)
        sys.exit(1)

def whereIsTrials():
    try:
        res = requests.get(whereIsTrials_url)
            # ex: [{"referenceId":"3292667877","start_date":"2016-11-25 17:00:00","week":"53","activityName":"Asylum",
            # "pgcrImage":"\/img\/theme\/destiny\/bgs\/pgcrs\/crucible_asylum.jpg"}]
        return res.json()[0]['activityName']

    except requests.exceptions.RequestException as e:
        print e
        sys.exit(1)

def whereIsXur():
    try:
        res = requests.get(whereIsXur_url)
        return(res.json()['location'])

    except requests.exceptions.RequestException as e:
        print e
        sys.exit(1)


def getXurInventory():
    try:
        # Send the request and store the result in res:
        res = requests.get(xur_url, headers=bungo_authHeader)
        #todo: return a list instead of a string when we're ready to send the email as HTML
        #xurStuff = []
        xurStuff = ""
        for saleItem in res.json()['Response']['data']['saleItemCategories']:
            mysaleItems = saleItem['saleItems']
            for myItem in mysaleItems:
                hashID = str(myItem['item']['itemHash'])
                hashReqString = bungie_base_url + "Manifest/" + hashType + "/" + hashID
                res = requests.get(hashReqString, headers=bungo_authHeader)
                item_name = res.json()['Response']['data']['inventoryItem']['itemName']
                #print "Item is: " + item_name
                #item_type = res.json()['Response']['data']['inventoryItem']['itemTypeName']
                #item_tier = res.json()['Response']['data']['inventoryItem']['tierTypeName']
                #print "Item type is: " + item_tier + " " + item_type + "\n"
                #xurStuff = xurStuff + "\n" + item_name + ": " + item_tier + " " + item_type + "\n"
                xurStuff = xurStuff + "\n" + item_name + "\n"
                #xurStuff.append(item_name + " " + item_tier + " "+ item_type)
                #print item_name + ": " + item_tier + " " + item_type
                sleep(0.5)
        return(xurStuff)

        # Print the error status:
        error_stat = res.json()['ErrorStatus']
        if error_stat != "Success":
            print "Error status: " + error_stat + "\n"
            sys.exit(1)

    except requests.exceptions.RequestException as e:
        print e
        sys.exit(1)

def main():
    try:
        sendMail()

    except KeyboardInterrupt:
        print "Shutdown requested...exiting"
    except Exception:
        traceback.print_exc(file=sys.stdout)
    sys.exit(0)


if __name__ == "__main__":
    main()


