# Nalanda Lite (nalandalite)
#### Because being lazy is Being _BITSian_!

Update lecture slides with one click. Regular trips to Nalanda? Now Lite.
Are you a gen BITSian? Do you download lecture slides just before your Compre/MidSem? Then Nalanda Lite is what you need. You shouldn't be wasting time downloading each and every slide, should you? So take visiting Nalanda **Lite** and use Nalanda Lite.

## Basic Usage
1. Clone this Repository (or download a zipped version)
2. Create a credentials.txt file in this folder. The first line of this file must have your username enclosed whithin two ^ characters. i.e. the first line must be \^your_Nalanda_username\^ and similarly, the second line of this file must be \^your_Nalanda_password\^.
3. Do not worry! Your password is safe. It NEVER leaves your computer. It remains there.
4. Go to the terminal and navigate to this folder ('nalandalite'). run "sudo pip install -r requirements.txt"
5. Run "python nalanda.py"
6. That's All!! Everytime you run _nalanda.py_, your lecture slides will be updated.
7. A directory named COURSES will be created which will hold all your courses.

#### credentials.txt:
```
^f201xabc^
^password^
```
#### Terminal:
```sh
~ $ sudo pip install -r requirements.txt
nalandalite $ python nalanda.py
```

## Dependancies
  - PIP (Python's package manager)
  - requests
  - BeautifulSoup

#### You Could:
```sh
$ pip install requests
$ pip install beautifulsoup4
```
#### Or simply (as already mentioned above):
```sh
$ pip install -r requirements.txt
```

## Advanced Usage:
#### Arguements
You can give the script some arguements as per your need, for additional functionality.
Arguements are given in argv format (i.e. separated by spaces) when running the _nalanda.py_ script. Currently supported arguements:
 - "users" : This will show the online users on nalanda. Note that when this arguement is given alone, slides aren't updated.
 - "debug" : This will run nalanda.py in debug mode.
 - "getslides" : This arguement is assumend by default if no arguement is given to the script, or the only arguement given is "debug" or "r=_time_". This, as the name suggests, will fetch your slides for you.
 - "r=_time_" : this reloads the script every unit _time_. for example: "r=10s", "r=5m", "r=1h". s, m and h correspond to seconds, minutes and hours, repectively.
 - "all" : Combination of all arguements except "debug".

```sh
nalandalite $ python nalanda.py
/* Runs Nalanda Lite normally. Slides updated */

nalandalite $ python nalanda.py debug
/* Runs Nalanda Lite in debug mode. Slides Updated */

nalandalite $ python nalanda.py users
/* Online Nalanda Users are printed. Slides not updated. (debug arguement can also be given with this) */

nalandalite $ python nalanda.py users getslides r=1h debug
/* Users Printed. Slides Updated. Recursive calls per hour. Debug Mode */

nalandalite $ python nalanda.py all r=1h debug
/* somewhat same as above */
```

# License
You are free to use any part of this code, as long as you credit the Author

# Author
Chinmay Pandhare, BITS Pilani.
