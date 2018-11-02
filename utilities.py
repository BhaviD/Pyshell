import getpass

BLACK=30
RED=31
GREEN=32
BLUE=34
PURPLE=35

def cursor_move(x, y):
    print ("\033[{0};{1}H".format(x, y))

def screen_clear():
    print (chr(27) + "[2J")
    cursor_move(0, 0)

def ErrorPrint(msg):
    print ("\033[0;{0}m{1}\033[0m".format(RED, msg), end='', flush=True)

def SuccessPrint(msg):
    print ("\033[0;{0}m{1}\033[0m".format(GREEN, msg), end='')

def ColorTextPrint(color, msg, bold = False):
    if bold == False:
        print ("\033[0;{0}m{1}\033[0m".format(color, msg), end='')
    else:
        print ("\033[1;{0}m{1}\033[0m".format(color, msg), end='')

def BoldPrint(msg):
    print ("\033[1;{0}m{1}\033[0m".format(BLACK, msg), end='')

def YesNoGet(question):
    r = input("{0} (y/n) ? ".format(question))
    while(r != "y" and r != "n"):
        ErrorPrint("Invalid Input!!\n")
        r = input("{0} (y/n) ? ".format(question))
    return r

def FloatingPointInputGet(msg):
    f=0.0
    while True:
        try:
            ff = input(msg)
            if ff == "":
                break
            f = float(ff)
            break
        except ValueError:
            ErrorPrint("Only Floating Point values accepted... please try again!!\n")
    return f


def IntegerInputGet(msg):
    i=0
    while True:
        try:
            ii = input(msg)
            if ii == "":
                break
            i = int(ii)
            break
        except ValueError:
            ErrorPrint("Only Integer values accepted... please try again!!\n")
    return i

   

def MobileNumberGet(msg):
    n=""
    while True:
        try:
            nn = input(msg)
            if nn == "":
                break
            if (len(nn) < 10 or len(nn) > 10):
                ErrorPrint("Mobile number should contain 10 digits!!\n")
                continue
            (int)(nn)
            n = nn
            break
        except ValueError:
            ErrorPrint("Only numeric input allowed... please try again!!\n")
    return n


def DictPrintAndInputGet(_dict):
    l = len(_dict)
    for a in sorted(_dict):
        BoldPrint (a)
        print (" : {0}".format(_dict[a]))

    BoldPrint("-1")
    print (": Go Back")
    print ("==============================================")

    str_x = input(">> ")
    x = 0
    if(str_x == "-1" or str_x.isdigit()):
        x = (int)(str_x)

    while(x != -1 and (1 > x or x > l)):
        ErrorPrint("Invalid Input... Please try again!!\n\n")
        for a in sorted(_dict):
            BoldPrint (a)
            print (" : {0}".format(_dict[a]))

        BoldPrint("-1")
        print (": Go Back")
        print ("==============================================")

        str_x = input(">> ")
        if(str_x == "-1" or str_x.isdigit()):
            x = (int)(str_x)

    return x


def NewPasswdGet(msg):
    pswd = getpass.getpass(msg)
    while (pswd != "" and len(pswd) < 8):
        ErrorPrint("Minimum length of password should be 8... please try again!!\n")
        pswd = getpass.getpass(msg)

    return pswd

def PasswdInputMatch(msg, correct_passwd):
    try_count = 1
    max_try_count = 3
    pswd = ""
    pswd = getpass.getpass(msg)
    while (pswd != correct_passwd):
        try_count += 1
        if (try_count > max_try_count):
            ErrorPrint ("Max number of tries reached!!\n")
            return False

        ErrorPrint("Incorrect Password... please try again!!\n")
        pswd = getpass.getpass(msg)

    return True


