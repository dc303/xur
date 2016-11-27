# where is xur, what's he got, and where is trials?

#from lxml import html
#import json

import requests
import os,sys,traceback
import sendgrid
from sendgrid.helpers.mail import *

# Uncomment this line to print JSON output to a file:
# f = open('output.txt', 'w')

apiKey=os.environ['BUNGIE_API_KEY']
BUNGO_AUTHHEADER = {'X-API-Key': apiKey}

base_url = "https://www.bungie.net/platform/Destiny/"
#xur_url = "https://www.bungie.net/Platform/Destiny/Advisors/Xur/"

bungie_base_url = "https://www.bungie.net/Platform/Destiny/"
xur_url = bungie_base_url + "Advisors/Xur/"

whereIsXur_url = "https://tellmewhereisxur.com/api"
whereIsTrials_url = "http://api.destinytrialsreport.com/currentMap/"
hashType = "6"


def sendMail():
    try:
        sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
        from_email = Email("guardian@ninjachemists.com")
        subject = "TGIF: Xur and Trials update"
        to_email = Email("ninja-chemists@googlegroups.com")
        content = Content("text/plain", "Hello, Guardian!\n\nTrials this week is on " + whereIsTrials() + "\n\nXur is " + whereIsXur() + "\n\n\nHere's what Xur has this week:\n\n\n\n" + getXurInventory())
        mail = Mail(from_email, subject, to_email, content)
        response = sg.client.mail.send.post(request_body=mail.get())
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
        #print "finding xur by hitting" + whereIsXur_url
        #print "Xur is " + res.json()['location']
        return(res.json()['location'])

    except requests.exceptions.RequestException as e:
        print e
        sys.exit(1)


def getXurInventory():
    try:
        # Send the request and store the result in res:
        res = requests.get(xur_url, headers=BUNGO_AUTHHEADER)
        #xurStuff = []
        xurStuff = ""
        for saleItem in res.json()['Response']['data']['saleItemCategories']:
            mysaleItems = saleItem['saleItems']
            for myItem in mysaleItems:
                hashID = str(myItem['item']['itemHash'])
                hashReqString = bungie_base_url + "Manifest/" + hashType + "/" + hashID
                res = requests.get(hashReqString, headers=BUNGO_AUTHHEADER)
                item_name = res.json()['Response']['data']['inventoryItem']['itemName']
                #print "Item is: " + item_name
                item_type = res.json()['Response']['data']['inventoryItem']['itemTypeName']
                item_tier = res.json()['Response']['data']['inventoryItem']['tierTypeName']
                #print "Item type is: " + item_tier + " " + item_type + "\n"
                xurStuff = xurStuff + "\n" + item_name + ": " + item_tier + " " + item_type + "\n"
                #xurStuff.append(item_name + " " + item_tier + " "+ item_type)
                #print item_name + ": " + item_tier + " " + item_type
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
        sys.exit(0)
        #mailContent = ""
        #print "Trials this week is on " + whereIsTrials()
        #print "Xur is " + whereIsXur()
        #print "\nHere's what Xur has this week:\n"
        #for element in getXurInventory():
        #    print '<td>%s</td>' % element
        #print getXurInventory().items()

    except KeyboardInterrupt:
        print "Shutdown requested...exiting"
    except Exception:
        traceback.print_exc(file=sys.stdout)
    sys.exit(0)



if __name__ == "__main__":
    main()


