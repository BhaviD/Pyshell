import utilities as utils
from pathlib import Path
from datetime import date

import os
import pwd
import time
import stat
import re

# bash commands
EXIT="exit"
CD="cd"
LS="ls"
PWD="pwd"
TOUCH="touch"
GREP="grep"


def PromptPrint():
    dt = date.today()
    user = pwd.getpwuid(os.getuid()).pw_name
    cwd_path = os.getcwd()

    if cwd_path == str(Path.home()):
        cwd = "~"
    elif cwd_path == "/":
        cwd = "/"
    else:
        parent_path, cwd = os.path.split(cwd_path)

    utils.ColorTextPrint(utils.BLUE, "[{0} {1}] ".format(dt.strftime("%a %b %d"), user), True)
    print ("@ ", end="")
    utils.ColorTextPrint(utils.GREEN, "[{0}] ".format(cwd), True)
    print ("$ ", end="")


def RemoveTrailingFwdSlashes(s):
    n = len(s)
    while (s != "" and s[n - 1] == '/'):
        s = s[:n-1]
        n -= 1
    return s


def RemovePrecedingFwdSlashes(s):
    while (s != "" and s[0] == '/'):
        s = s[1:]
    return s


def TildeToHomeConvert(s):
    s = s[1:]
    s = RemovePrecedingFwdSlashes(s)
    s = str(Path.home()) + '/' + s
    s = RemoveTrailingFwdSlashes(s)
    return s


def cd_run(args, prev_dir, curr_dir):
    if (args == ""):         # handling empty argument to "cd" command
        args = str(Path.home())

    elif (args[0] == '~'):   # handling "~/"
        args = TildeToHomeConvert(args)
        print(args)

    if (args[0] == '-'):     # handling '-'
        if prev_dir != "":
            print (prev_dir)
            os.chdir(prev_dir)
    else:
        try:
            os.chdir(args)
        except FileNotFoundError:
            utils.ErrorPrint("No such directory... please try again!!\n")


def ls_run(args):
    if (args == ""):
        args = os.getcwd()
    elif (args[0] == '~'):
        args = TildeToHomeConvert(args)

    dir_content = os.listdir(args)
    for c in sorted(dir_content):
        if c[0] != '.':
            print (c)

def touch_run(args):
    if (args == ""):
        utils.ErrorPrint("touch: missing file operand\n")
        return

    # check whether the parent directories exist or not
    p = (str)(Path(args).absolute())
    basedir, f = os.path.split(p)
    if not Path(basedir).exists():
        utils.ErrorPrint("touch: cannot touch {0}: no such file or directory!!\n".format(args))
        return

    # check whether the file/directory exists or not
    if Path(args).exists():
        os.utime(args, None)
    else:
        with open(args, 'a'):        # new file is created
            os.utime(args, None)


def grep_file(pattern, filepath, flag_n, print_path = False):
    with open(filepath, 'r') as search_file:
        i = 0
        for line in search_file:
            i += 1
            match = re.findall(r"{0}".format(pattern), line)
            if match:
                if print_path:
                    if flag_n:
                        print ("{0}:{1}:{2}".format(filepath, i, line), end="")
                    else:
                        print ("{0}:{1}".format(filepath, i), end="")
                else:
                    if flag_n:
                        print ("{0}:{1}".format(i, line), end="")
                    else:
                        print ("{0}".format(line), end="")


def grep_run(args):
    args_list = args.split()
    n = len(args_list)
    flag_n = False
    flag_r = False
    pattern_found = False
    pattern = ""

    for a in args_list:
        if flag_n and flag_r:
            break

        if (a[0] == '-'):
            for i in range(1, len(a)):
                if (a[i] == 'n'):
                    flag_n = True
                elif (a[i] == 'r'):
                    flag_r = True

        elif (pattern_found == False):
            pattern = a
            pattern_found = True


    search_content = args_list[n-1]
    if (search_content == "*"):
        if flag_r:
            grep_dir_recursive(pattern, os.getcwd(), flag_n)
        else:
            grep_dir_iterative(pattern, os.getcwd(), flag_n)

    elif (os.path.isdir(search_content)):
        if not flag_r:
            utils.ErrorPrint("grep: {0}: Is a directory\n".format(search_content))
            return
        else:
            grep_dir_recursive(pattern, search_content, flag_n)

    elif (os.path.isfile(search_content)):
        grep_file(pattern, search_content, flag_n)



if __name__ == "__main__":
    utils.screen_clear()
    utils.BoldPrint("Pyshell Started...\n\n")

    curr_dir = os.getcwd()
    prev_dir = ""
    while(True):
        PromptPrint()
        ip_cmd = input()

        cmd_list = ip_cmd.split()
        if (len(cmd_list) == 0):
            continue

        if (cmd_list[0] == EXIT):
            break

        cmd = cmd_list[0]
        del cmd_list[0]
        args = ' '.join([str(a) for a in cmd_list])

        if (cmd == CD):
            cd_run(args, prev_dir, curr_dir)
            prev_dir = curr_dir
            curr_dir = os.getcwd()

        elif (cmd == LS):
            ls_run(args)

        elif (cmd == PWD):
            print (curr_dir)

        elif (cmd == TOUCH):
            touch_run(args)

        elif (cmd == GREP):
            grep_run(args)

        else:
            utils.ErrorPrint ("{0}: command not found\n".format(cmd))

    utils.screen_clear()
    utils.BoldPrint("Pyshell Exited...\n\n")
