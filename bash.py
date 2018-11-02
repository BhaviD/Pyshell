import utilities as utils
from pathlib import Path
from datetime import date

import os
import pwd
import time
import stat

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


# def RemovePrecedingSpaces(s):
#     while (s != "" and s[0] == ' '):
#         s = s[1:]
#     return s
#
#
# # Returns the command and args strings
# def CommandExtract(s):
#     s = RemovePrecedingSpaces(s)
#
#     i = 0
#     while (i < len(s) and s[i] != ' '):
#         i += 1
#     if i == len(s):
#         return s, ""
#
#     cmd = s[:i]
#     args = s[i+1:]
#
#     args = RemovePrecedingSpaces(args)
#
#     return cmd, args


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
        args = home_dir

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
   

if __name__ == "__main__":
    utils.screen_clear()
    utils.BoldPrint("Pyshell Started...\n\n")

    cmd=[""]
    curr_dir = os.getcwd()
    prev_dir = ""
    home_dir = str(Path.home())
    while(True):
        PromptPrint()
        ip_cmd = input()

        #cmd, args = CommandExtract(ip_cmd)
        cmd_list = ip_cmd.split()
        if (len(cmd_list) == 0):
            continue

        if (cmd_list[0] == "exit"):
            break

        cmd = cmd_list[0]
        del cmd_list[0]
        args = ' '.join([str(a) for a in cmd_list])

        if (cmd == "cd"):
            cd_run(args, prev_dir, curr_dir)
            prev_dir = curr_dir
            curr_dir = os.getcwd()

        elif (cmd == "ls"):
            dir_content = os.listdir()
            for c in sorted(dir_content):
                if c[0] != '.':
                    print (c)

        elif (cmd == "pwd"):
            print (curr_dir)

        elif (cmd == "touch"):
            if (args == ""):
                utils.ErrorPrint("touch: missing file operand\n")
                continue

            # check whether the parent directories exist or not
            p = (str)(Path(args).absolute())
            basedir, f = os.path.split(p)
            if not Path(basedir).exists():
                utils.ErrorPrint("touch: cannot touch {0}: no such file or directory!!\n".format(args))
                continue

            # check whether the file/directory exists or not
            if Path(args).exists():
                os.utime(args, None)
            else:
                with open(args, 'a'):        # new file is created
                    os.utime(args, None)

        #elif (cmd == "grep"):

        else:
            utils.ErrorPrint ("{0}: command not found\n".format(cmd))

    utils.screen_clear()
    utils.BoldPrint("Pyshell Exited...\n\n")
