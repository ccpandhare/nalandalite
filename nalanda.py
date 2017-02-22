import sys, re, os, cgi
import sched, time, datetime

#options
arguements = sys.argv
del arguements[0]
s = sched.scheduler(time.time, time.sleep)

if "debug" in arguements:
    debug = True
    print "\n\tReceived argv:"
    print "\t" , sys.argv
    arguements.remove("debug")
else:
    debug = False

global debugger
def debugger(data,pos):
    if debug == True:
        print data
try:
    rT = [m.group(1) for arg in arguements for m in [re.compile('^r=([0-9]*).*$').search(arg)] if m][-1]
    rM = [m.group(1) for arg in arguements for m in [re.compile('^r=[0-9]*(.*)$').search(arg)] if m][-1]
    rW = [m.group(1) for arg in arguements for m in [re.compile('^r=(.*)$').search(arg)] if m][-1]
    arguements.remove("r="+rT+rM)
    rT = int(rT)
except:
    rT = False
if not rT == False:
    if rM == 'm':
        rT *= 60
    elif rM == 'h':
        rT *= 60*60
    else:
        rT *= 1
if debug == True:
    print "\n\trecursive = " , rT

#check for and import requests module
if debug == True:
    print "\n\tChecking requests module"
try:
    import requests
except:
    sys.exit("\n\tModule ERROR:\n\t\'Requests\' module not installed.\n\tEnter \'sudo pip install requests\' on the command line and try again.\n")
if debug == True:
    print "\tModule exists.\n"

#check for and import beautifulsoup4 module
if debug == True:
    print "\n\tChecking beautifulsoup4 module"
try:
    from bs4 import BeautifulSoup
except:
    sys.exit("\n\tModule ERROR:\n\t\'BeautifulSoup\' module not installed.\n\tEnter \'sudo pip install beautifulsoup4\' on the command line and try again.\n")
if debug == True:
    print "\tModule exists.\n"


def main():
    #definitions
    loginurl = 'http://nalanda.bits-pilani.ac.in/login/index.php'

    #try and open credentials.txt file
    debugger("\n\tOpening credentials.txt",0)
    try:
        credentials = open('credentials.txt','r').read().split('\n')
    except IOError:
        sys.exit("\n\tFile ERROR:\n\tProblem reading the credentials.txt file.\n\tCheck if file exists.\n\tIf the file exists, and you are still getting this error,\n\t\tEnter \'chmod u+r credentials.txt\' in the command line and try again.\n")
    debugger("\tOpened Successfully.\n",1)

    debugger("\n\tChecking credentials.txt",0)
    if len(credentials) < 2:
        sys.exit("Problem with credentials.txt file.\nMake sure that you have entered both the username and password.")
    debugger("\tFile is OK.\n",1)

    # Start a session
    debugger("\n\tStarting Session.",0)
    try:
        session = requests.session()
    except:
        sys.exit("Could not initiate session")
    debugger("\tSession initiated.\n",1)
    fetchfilter = re.compile('\^(.*)\^')
    login_data = {
        'username': fetchfilter.findall(credentials[0])[0],
        'password': fetchfilter.findall(credentials[1])[0],
        'submit': 'Login',
    }
    debugger("\n\tSupplied username: " + fetchfilter.findall(credentials[0])[0],0)
    debugger("\tSupplied password: " + "*"*len(fetchfilter.findall(credentials[1])[0]) + "\n",1)

    #login
    debugger("\n\tLogging in.",0)
    r = session.post(loginurl, data=login_data)
    if re.compile('<div class="logininfo">[^<>]*<a[^<>]*>([^<>]*)</a>', re.I).findall(r.text) == []:
        sys.exit("\n\tAuthentication Error.\n\tPlease check the credentials.txt file.\n\tThe first line of the file must have your username within two ^ characters.\n\tThe second line must have your password within two ^ characters.\n")
    debugger("\tLogged in Successfully.\n",1)

    #try and get homepage data
    debugger("\n\topen homepage; method:GET",0)
    try:
        r = session.get('http://nalanda.bits-pilani.ac.in/')
    except:
        sys.exit("\n\tGET ERROR:\n\tCould not fetch Nalanda homepage");
    debugger("\tHomepage loaded\n",1)
    text = r.text

    soup = BeautifulSoup(text,"html.parser")
    #filter definitions
    divs = soup.find_all("div", {"class": "course_title"})
    courses = []
    for div in divs:
        namearray = []
        array = re.compile("[A-Z]*",re.I).findall(re.compile(" \(.*\)$").sub("",div.find("a").string))
        for a in array:
            if a != "":
                namearray += [a]
        foldername = "_".join(namearray)

        courses += [[re.compile('....$').findall(div.find("a")['href'])[0] , div.find("a").string , foldername]]

    divs = soup.find_all("div", {"class": "user"})
    users = []
    for div in divs:
        try:
            users += [[re.compile('id=(....)').findall(div.find("a")['href'])[0] , re.compile('([^<>]*) \. \.$').findall(div.find("a").text)[0]]]
        except IndexError:
            indexError = True


    if "users" in arguements or "all" in arguements:
        print "\n\tOnline Users:"
        for user in users:
            print "\t\t"+user[0] + " " + user[1]

    if "courses" in arguements or "all" in arguements or len(arguements) == 0:
        print "\n\tCourses:"
        for course in courses:
            print "\t\t"+course[1]

    if "coursedirs" in arguements or "all" in arguements or "getslides" in arguements or len(arguements) == 0:
        dirs_made = 0
        print "\n\tCourse Directories:"
        if not os.path.isdir("COURSES"):
            debugger("\t\tmaking directory COURSES",0)
            try:
                os.makedirs("COURSES")
            except:
                sys.exit("Could not make directory COURSES. Please check permissions.")
            dirs_made += 1
            debugger("\t\tMade directory COURSES.\n",1)

        for course in courses:
            debugger("\t\t" + course[2] + " exists: " + str(os.path.isdir("COURSES/"+course[2])),0)
            if not os.path.isdir("COURSES/"+course[2]):
                debugger("\t\t\tmaking directory COURSES/"+course[2],0)
                try:
                    os.makedirs("COURSES/"+course[2])
                except:
                    print "Could not make directory COURSES/"+course[2]+". Please check permissions."
                dirs_made += 1
                debugger("\t\t\tMade directory COURSES/"+course[2],1)
        print "\t\t"+str(dirs_made)+" directories made"

    if "getslides" in arguements or "all" in arguements or len(arguements) == 0:
        print "\n\tGetting Slides: (Please Be Patient. This may take some time)"
        for course in courses:
            articles = []
            link = "http://nalanda.bits-pilani.ac.in/course/view.php?id="+course[0]
            print "\t\t"+course[1]
            coursesoup = BeautifulSoup(session.get(link).text,"html.parser")
            liss = coursesoup.find("ul",{"class": "topics"}).find_all("li", class_= "section main clearfix")
            for lis in liss:
                for li in lis.find_all("li"):
                    if str(lis.find("h3")) != "None":
                        if str(li.find("a")) != "None":
                            #print "\n\t\t\t"+li['id']
                            heading = str(lis.find("h3").text)+"\n"
                            for a in li.find_all("a"):
                                articlelink = str(a['href'])
                                if not str(a.find("span", {"class": "accesshide"})) == "None":
                                    articletitle = str(a.text.replace(a.find("span", {"class": "accesshide"}).text,""))
                                else:
                                    articletitle = ""
                                if not str(a.find("span", {"class": "accesshide"})) == "None":
                                    articletype = str(a.find("span", {"class": "accesshide"}).text.replace(" ",""))
                                else:
                                    articletype = "None"
                            if str(li.find("span", {"class": "resourcelinkdetails"})) != "None":
                                articledetails = str(li.find("span", {"class": "resourcelinkdetails"}).text)
                            else:
                                articledetails = "None"
                            articles += [[str(heading),str(articletype),str(articletitle),str(articlelink),str(articledetails)]]
            num_downloaded = 0
            for article in articles:
                head = session.head(article[3])
                if re.compile("PDF").findall(article[4]) == ['PDF']:
                    res = session.get(article[3])
                    resourceobject = BeautifulSoup(res.text,"html.parser").find("object",{"id": "resourceobject"})
                    resourcelink = resourceobject['data']
                else:
                    resourcelink = article[3]
                    if article[1] == "File":
                        resourcelink = session.head(resourcelink).headers['Location']

                file_to_download = session.head(resourcelink)
                try:
                    val, resourcename = cgi.parse_header(file_to_download.headers['Content-Disposition'])
                    resourcename = resourcename['filename']
                except:
                    resourcename = re.compile("id=(....)").findall(article[3])[0] + "-" + "file.html"
                #resourcename = re.compile("id=(....)").findall(article[3])[0] + "-" + resourcename;

                path_to_file = 'COURSES/'+course[2]+'/'+resourcename
                if not os.path.exists(path_to_file):
                    debugger("\t\t\t"+article[2],0)
                    debugger("\t\t\t"+article[4],0)
                    debugger("\t\t\t\t"+resourcename,1)
                    r = session.get(resourcelink)
                    with open(path_to_file, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=1024):
                            if chunk: # filter out keep-alive new chunks
                                f.write(chunk)
                    num_downloaded += 1
            print "\t\t\t"+str(num_downloaded)+" new file(s) downloaded."

    if not (rT == False):
        print "\n\tUpdating in " , rW

def do_something(sc):
    main()
    s.enter(sc, 1, do_something, (sc,))

if __name__ == '__main__':
    main()
    if not (rT == False or rT == 0):
        s.enter(rT, 1, do_something, (rT,))
    s.run()
