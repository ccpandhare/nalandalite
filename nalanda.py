import sys, re
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
    sys.exit("\n\tModule ERROR:\n\t\'Requests\' module not installed.\n\tEnter \'pip install requests\' on the command line and try again.\n")
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

    #filter definitions
    coursefilter = re.compile('<a[^"]*href="[^"]*course\/view.php\?id=([^"]*)[^"]*"', re.I)
    #<a href="http://nalanda.bits-pilani.ac.in/user/view.php?id=8294&amp;course=1" title="1 sec"><img src="http://nalanda.bits-pilani.ac.in/theme/image.php/formfactor/core/1470067502/u/f2" alt="" title="" class="userpicture defaultuserpic" width="16" height="16" />Chinmay Pandhare . .</a>
    userfilter = re.compile('<a[^"]*href="[^"]*user\/view.php[^"]*"[^<>]*><img[^<>]*/>([^<>]*) \. \.</a>', re.I)
    #<div id="inst44796" class="block_course_overview  block"
    overviewfilter = re.compile('<h2[^<>]*>Course overview</h2></div></div><div class="content">([^<>]*)</div>', re.I)

    if "users" in arguements or "all" in arguements or len(arguements) == 0:
        print "\n\tOnline Users:"
        for user in userfilter.findall(text):
            print "\t\t"+user

    if "courses" in arguements or "all" in arguements or len(arguements) == 0:
        print "\n\tCourses:"
        for link in coursefilter.findall(text):
            print "\t\t"+link

    if "overview" in arguements or "all" in arguements or len(arguements) == 0:
        print "\n\tCourse overview:"
        for content in overviewfilter.findall(text):
            print "\t\t"+content

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
