import sys, re, os, cgi
import sched, time, datetime
from bs4 import BeautifulSoup

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
    sys.exit("\n\tModule ERROR:\n\t\'Requests\' module not installed.\n\tEnter \'pip install requests\' on the command line and try again.\n")
if debug == True:
    print "\tModule exists.\n"

filetypes = {
"application/pdf": "pdf",
"application/vnd.openxmlformats-officedocument.presentationml.presentation": "ppt",
"application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "xlsx",
"application/vnd.openxmlformats-officedocument.spreadsheetml.template": "xltx",
"application/vnd.ms-excel.sheet.macroEnabled.12": "xlsm",
"application/vnd.ms-excel.template.macroEnabled.12": "xltm",
"application/vnd.ms-excel": "xls",
"application/msword": "doc",
"text/html; charset=utf-8": "html",
"image/gif": "gif",
"image/jpg": "jpg",
"image/png": "png",
"image/svg": "svg"
}

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
        sys.exit("\n\tAuthentication Error.\n\tPlease check the credentials.txt file.\n\tThe first line of the file must have your username within double quotes.\n\tThe second line must have your password within double quotes.\n")
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


    if "users" in arguements or "all" in arguements or len(arguements) == 0:
        print "\n\tOnline Users:"
        for user in users:
            print "\t\t"+user[0] + " " + user[1]

    if "courses" in arguements or "all" in arguements or len(arguements) == 0:
        print "\n\tCourses:"
        for course in courses:
            print "\t\t"+course[0] + " " + course[1] + " " + str(os.path.isdir("COURSES/"+course[2]))

    if "coursedirs" in arguements or "all" in arguements or "getslides" in arguements or len(arguements) == 0:
        print "\n\tCourse Directories:"
        if not os.path.isdir("COURSES"):
            debugger("\t\tmaking directory COURSES",0)
            try:
                os.makedirs("COURSES")
            except:
                sys.exit("Could not make directory COURSES. Please check permissions.")
            debugger("\t\tMade directory COURSES.\n",1)

        for course in courses:
            print "\t\t" + course[2] + " exists: " + str(os.path.isdir("COURSES/"+course[2]))
            if not os.path.isdir("COURSES/"+course[2]):
                debugger("\t\t\tmaking directory COURSES/"+course[2],0)
                try:
                    os.makedirs("COURSES/"+course[2])
                except:
                    print "Could not make directory COURSES/"+course[2]+". Please check permissions."
                debugger("\t\t\tMade directory COURSES/"+course[2],1)
    if "getslides" in arguements or "all" in arguements or len(arguements) == 0:
        print "\n\tGetting Slides:"
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
                                articletitle = str(a.text.replace(a.find("span", {"class": "accesshide"}).text,""))
                                articletype = str(a.find("span", {"class": "accesshide"}).text.replace(" ",""))
                            if str(li.find("span", {"class": "resourcelinkdetails"})) != "None":
                                articledetails = str(li.find("span", {"class": "resourcelinkdetails"}).text)
                            else:
                                articledetails = "None"
                            articles += [[str(heading),str(articletype),str(articletitle),str(articlelink),str(articledetails)]]
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
                    resourcename = "file.html"
                #resourcename = re.compile("id=(....)").findall(article[3])[0] + "-" + resourcename;
                #print "\t\t\t\t"+resourcename

                path_to_file = 'COURSES/'+course[2]+'/'+resourcename
                if not os.path.exists(path_to_file):
                    print "\t\t\t"+article[2]
                    print "\t\t\t"+article[4]
                    print "\t\t\t\t"+resourcename
                    r = session.get(resourcelink)
                    with open(path_to_file, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=1024):
                            if chunk: # filter out keep-alive new chunks
                                f.write(chunk)

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
