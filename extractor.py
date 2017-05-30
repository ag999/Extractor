import re, requests, json
from socket import timeout
TIMEOUT = 5 #The wait time in seconds before timing out for requesting the page

def main(url):
    """Prints in json format the found twitter handle, facebook page id, iOS App
    Store Id and Google Play Store Id."""
    regexFb = r"facebook\.com\/([a-zA-Z0-9_]+)"
    regexTwitter = r"twitter\.com\/([a-zA-Z0-9_]+)"
    regexApple = r"apple\.com\/(?:[a-zA-Z_-]+\/)?app\/[a-zA-Z0-9_-]+\/id([0-9]+)"
    regexGoogle = r"google\.com\/[a-zA-Z0-9_]+\/apps\/details\?id=((?:com|org)?.[a-zA-Z0-9_-]+)"
    web = url[url.find("/")+2:url.find(".com")].lower()
    if("www." in web):
        web = web[4:] #Gets the domain name 
    text = readPage(url)
    if(text == "00"): #00 would not be returned for anything else so same to use it for error code
        return;
    twit = None
    if("twitter" != web):#Already on the Twitter page
        twit = extract(url, regexTwitter, web, text)
    fb = None
    if("facebook" != web):#Already on the Facebook page
        fb = extract(url, regexFb, web, text)
        if (fb != None and fb.isdigit()): #For some reason there are times when the year of something is written in the same format as the page id for Facebook
            fb=None
    appleId = None
    if("itunes.apple" != web):#Itunes page of the app has ids for other apps not but the one we are at
        appleId = extract(url, regexApple, web, text)
    googleId = extract(url, regexGoogle, web, text)
    if(googleId == None):
        regexGoogle = r'content="((?:com|org)?.[a-zA-Z0-9_-]+).android"' #I found some websites used a different format for having the link for their Google Play Store App
        googleId = extract(url, regexGoogle, web, text)
    unordered = {}
    if(twit != None):
        unordered["twitter"] = twit
    if(fb != None):
        unordered["facebook"] = fb
    if(appleId != None):
        unordered["ios"] = appleId
    if(googleId != None):
        unordered["google"] = googleId
    if (len(unordered) == 0):
        print("Nothing found")
        return;
    print(json.dumps(unordered, indent = 2))
    
def extract(url, regex, web, text):
    """Returns the correct handle following a set rule of hierarchy."""
    matches = re.finditer(regex, text)
    Ids = list(set(listUsers(matches))) #List of all the handle matches
    if(len(Ids) == 0):
        return None
    redundant = {"plugins", "likes", "like", "html", "sharer", "dialog", "intent", "follow", "widgets"} #Often show up using the same format as handles but are not the handles
    if(len(Ids) == 1): #Only one then probably is that
        if Ids[0] not in redundant:
            return Ids[0]
        else:
            return None
        
    for x in Ids:
        if web == x.lower(): #Exact match with the domain name
            if x not in redundant:
                return x
            else:
                return None
    
    for x in Ids:
        if web in x.lower(): #Handle contains the domain name
            if x not in redundant:
                return x
            else:
                return None
   
    firstHalf = web[:int(len(web)/2)+1]
    for x in Ids:
        if firstHalf in x.lower(): #Handle contains first half of the domain name
            if x not in redundant:
                return x
            else:
                return None
    
    lastHalf = web[int(len(web)/2)+1:]
    for x in Ids:
        if lastHalf in x.lower(): #Handle contains last half of the domain name
            if x not in redundant:
                return x
            else:
                return None
    
    if Ids[0] not in redundant: #None of the above rules met but if there is a handle then it should be of the page. 
        return Ids[0]           #Ususally handles are in the first or the last link. More in the former case
    elif Ids[-1] not in redundant:
        return Ids[-1]
    else:
        return None

def readPage(url):
    """Reads the page associated with the given URL and returns it as string.
    # Print out the errors in case of bad URLs, request Timeout, Redirect requests and returns string 00"""
    
    text=""
    try:
        r = requests.get(url, timeout = TIMEOUT)
        text = r.text
    except requests.exceptions.Timeout:
    # Maybe set up for a retry, or continue in a retry loop
        print ("Your request to "+str(url)+" timeout out. The current timeout limit is " +str(TIMEOUT) +" seconds." + "\n" + "Trying again with a greater limit.")
        try:
            r = requests.get(url, timeout = TIMEOUT * 1.5)
            text = r.text
        except requests.exceptions.Timeout: #Make a second request in case of timeout with 1.5* times the timeout limit
            print("The request to " + str(url) + " timed out again. Please try again later or try a different URL.")
            return ("00")
        except requests.exceptions.RequestException as e:
            print(e)
            return ("00")
    except requests.exceptions.TooManyRedirects as error:
    # Tell the user their URL was bad and try a different one
        print(error)
        print("The given URL ("+str(url)+") was bad, pleaase try a different one")
        return ("00")
    except requests.exceptions.ConnectionError:
        print("The connection request to " + str(url) + " could not be completed")
        return ("00")
    except requests.exceptions.RequestException as e:
    # catastrophic error. bail.
        print(e)
        return ("00")
    return (text)

def listUsers(matches):
    """Returns a list of matches found in the capturing group of the regex."""
    returnList = []
    for num, match in enumerate(matches):
        num = num + 1
        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1
            returnList.append(match.group(groupNum))
    return returnList
