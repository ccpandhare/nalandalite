import requests
#import sys #not needed
import re

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
    print "Online Users:"
    for user in userfilter.findall(text):
        print user
    print "Courses:"
    for link in coursefilter.findall(text):
        print link
if __name__ == '__main__':
    main()
