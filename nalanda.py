import requests
#import sys #not needed
import re
import sched, time, datetime
s = sched.scheduler(time.time, time.sleep)

credentials = open('credentials.txt','r').read().split('\n')

URL = 'http://nalanda.bits-pilani.ac.in/login/index.php'

def main():
    # Start a session so we can have persistant cookies
    session = requests.session()

    # This is the form data that the page sends when logging in
    login_data = {
        'username': credentials[0],
        'password': credentials[1],
        'submit': 'Login',
    }

    # Authenticate
    r = session.post(URL, data=login_data)

    # Try accessing a page that requires you to be logged in
    r = session.get('http://nalanda.bits-pilani.ac.in/')

    text = r.text
    coursefilter = re.compile('<a[^"]*href="[^"]*course\/view.php\?id=([^"]*)[^"]*"', re.I)

    #<a href="http://nalanda.bits-pilani.ac.in/user/view.php?id=8294&amp;course=1" title="1 sec"><img src="http://nalanda.bits-pilani.ac.in/theme/image.php/formfactor/core/1470067502/u/f2" alt="" title="" class="userpicture defaultuserpic" width="16" height="16" />Chinmay Pandhare . .</a>
    userfilter = re.compile('<a[^"]*href="[^"]*user\/view.php[^"]*"[^<>]*><img[^<>]*/>([^<>]*) \. \.</a>', re.I)

    #<div id="inst44796" class="block_course_overview  block"
    overviewfilter = re.compile('<h2 id="instance-44796-header">Course overview</h2></div></div><div class="content">([^<>]*)</div>', re.I)

    users = open('users.txt','r').read().split('\n')
    log = open('userlog.txt','a')

    print "Online Users:"
    i = 0
    for user in userfilter.findall(text):
        if not user in users:
            users.extend([user])
            i = i+1
        stamp = datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p ")
        if user != "Chinmay Pandhare":
            log.write(stamp+user+"\n")
        print user
    print "Courses:"
    for link in coursefilter.findall(text):
        print link
    print "Course overview:"
    for content in overviewfilter.findall(text):
        print content

    usersupdated = "\n".join(users)
    open('users.txt','w').write(usersupdated)
    print i," users added"

def do_something(sc):
    print "Updating..."
    main()
    s.enter(270, 1, do_something, (sc,))

if __name__ == '__main__':
    main()
    s.enter(270, 1, do_something, (s,))
    s.run()
