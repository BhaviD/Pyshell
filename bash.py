import utilities as utils
from pathlib import Path
from datetime import date

import os
import pwd
import time
import stat
import re

# bash commands
EXIT = "exit"
CD = "cd"
LS = "ls"
PWD = "pwd"
TOUCH = "touch"
GREP = "grep"
TAIL = "tail"
HEAD = "head"

SUCCESS = 0
FAILURE = -1

FILE_BEG = 0
FILE_END = 2

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


def RemovePrecedingSpaces(s):
    while (s != "" and s[0] == ' '):
        s = s[1:]
    return s

def RemoveTrailingSpaces(s):
    n = len(s)
    while (s != "" and s[n - 1] == ' '):
        s = s[:n-1]
        n -= 1
    return s


 # Returns the command and args strings
def CommandExtract(s):
    s = RemovePrecedingSpaces(s)

    i = 0
    while (i < len(s) and s[i] != ' '):
        i += 1

    if i == len(s):
        return s, ""

    cmd = s[:i]
    args = s[i+1:]

    args = RemovePrecedingSpaces(args)
    args = RemoveTrailingSpaces(args)

    return cmd, args


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

    elif (args[0] == '-'):     # handling '-'
        if prev_dir != "":
            args = prev_dir
            print (prev_dir)
        else:
            args = curr_dir

    try:
        os.chdir(args)
    except Exception as err:
        utils.ErrorPrint("cd: {0}\n".format(err))
        return FAILURE

    return SUCCESS


def ls_run(args):
    if (args == ""):
        args = os.getcwd()
    elif (args[0] == '~'):
        args = TildeToHomeConvert(args)

    try:
        dir_content = os.listdir(args)
        for c in sorted(dir_content):
            if c[0] != '.':
                if (os.path.isdir("{0}/{1}".format(args, c))):
                    utils.ColorTextPrint(utils.BLUE, "{0}\n".format(c), True)
                else:
                    print (c)
    except Exception as err:
        utils.ErrorPrint("ls: {0}\n".format(err))
        

def touch_run(args):
    if (args == ""):
        utils.ErrorPrint("touch: missing file operand\n")
        return

    if (args[0] == '~'):
        args = TildeToHomeConvert(args)

    # check whether the parent directories exist or not
    p = (str)(Path(args).absolute())
    basedir, f = os.path.split(p)
    if not Path(basedir).exists():
        utils.ErrorPrint("touch: cannot touch '{0}': no such file or directory!!\n".format(args))
        return

    # check whether the file/directory exists or not
    if Path(args).exists():
        os.utime(args, None)
    else:
        with open(args, 'a'):        # new file is created
            os.utime(args, None)


def grep_file(pattern, filepath, flag_n, print_path = False):
    try:
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

    except Exception as err:
        utils.ErrorPrint("grep: {0}: {1}\n".format(filepath, err))
        

def grep_dir_iterative(pattern, dirpath, flag_n):
    try:
        dir_content = os.listdir(dirpath)
        for c in sorted(dir_content):
            if c[0] != '.':
                dest_path = "{0}/{1}".format(dirpath, c);
                if (os.path.isdir(dest_path)):
                    print("grep: {0}: Is a directory".format(dest_path))
                else:
                    grep_file(pattern, dest_path, flag_n, True)
    except Exception as err:
        utils.ErrorPrint("grep: {0}\n".format(err))


def grep_run(args):
    flag_n = False
    flag_r = False
    pattern_found = False
    pattern = ""
    search_dest = ""

    i = 0
    while (i < len(args)):
        if(args[i] == '-'):
            i += 1                      # get to next character
            while(args[i] != ' '):
                if (args[i] == 'r'):
                    flag_r = True
                elif (args[i] == 'n'):
                    flag_n = True
                i += 1

        elif(args[i] == ' '):           # ignore spaces
            i += 1

        elif (not pattern_found):
            pattern_found = True
            if (args[i] == '\''):       # pattern is enclosed in single quotes ('<pattern>')
                i += 1
                while(args[i] != '\'' or args[i-1] == '\\'):    # the pattern may contain ' in itself
                    if(args[i] != '\\'):
                        pattern += str(args[i])

                    i += 1

                i += 1
            else:
                while(args[i] != ' '):
                    pattern += str(args[i])
                    i += 1

                i += 1

        else:                           # search dest is at the of the arguments
            search_dest = args[i:]
            i = len(args)

            if (search_dest[0] == "\""):        # remove double quotes
                search_dest = search_dest[1:]
                search_dest = search_dest[:len(search_dest) - 1]


    if (search_dest == "*"):
        #if flag_r:
        #    grep_dir_recursive(pattern, os.getcwd(), flag_n)
        #else:
        grep_dir_iterative(pattern, ".", flag_n)

    elif (not Path(search_dest).exists()):
        utils.ErrorPrint("grep: '{0}': no such file or directory\n".format(search_dest))
        return

    else: 
        if(os.path.isdir(search_dest)):
            #if not flag_r:
            utils.ErrorPrint("grep: '{0}': Is a directory\n".format(search_dest))
            return
            #else:
            #    grep_dir_recursive(pattern, search_dest, flag_n)

        elif (os.path.isfile(search_dest)):
            grep_file(pattern, search_dest, flag_n)



def tail_run(args):
    if (args == ""):
        utils.ErrorPrint("Error: No arguments provided!!\n")
        return

    lines_reqd = 10
    filename = args
    i = 0
    if args[0] == '-':
        if args[1] != 'n':
            utils.ErrorPrint("tail: {0}: flag not supported\n".format(args[0:2]))
            return

        i = 2
        while (args[i] == ' '):
            i += 1

        j = i
        while ('0' <= args[j] and args[j] <= '9'):
            j += 1

        try:
            lines_reqd = (int)(args[i:j])
            filename = args[j+1:]
        except Exception as err:
            utils.ErrorPrint("tail: Invalid args: {0}\n".format(args))
            utils.ErrorPrint("tail: {0}\n".format(err))
            return

    try:
        with open(filename, 'r') as f:
            BLOCK_SIZE = 4096

            f.seek(0, os.SEEK_END)
            unprocessed_bytes = f.tell()
            lines_remaining = lines_reqd
            block_number = -1
            blocks = [] # blocks of size BLOCK_SIZE, in reverse order starting
                        # from the end of the file
            while lines_remaining > 0 and unprocessed_bytes > 0:
                if (unprocessed_bytes > BLOCK_SIZE):
                    unprocessed_bytes -= BLOCK_SIZE
                    f.seek(unprocessed_bytes)
                    blocks.append(f.read(BLOCK_SIZE))
                else:
                    unprocessed_bytes -= BLOCK_SIZE
                    f.seek(0, FILE_BEG)
                    blocks.append(f.read(unprocessed_bytes))

                lines_found = blocks[-1].count('\n')
                lines_remaining -= lines_found
                unprocessed_bytes -= BLOCK_SIZE
                block_number -= 1

            processed_text = ''.join(reversed(blocks))
            print ('\n'.join(processed_text.splitlines()[-lines_reqd:]))

    except Exception as err:
        utils.ErrorPrint("tail: {0}: {1}\n".format(filename, err))



def head_run(args):
    if (args == ""):
        utils.ErrorPrint("Error: No arguments provided!!\n")
        return

    lines_reqd = 10
    filename = args
    i = 0
    if args[0] == '-':
        if args[1] != 'n':
            utils.ErrorPrint("tail: {0}: flag not supported\n".format(args[0:2]))
            return

        i = 2
        while (args[i] == ' '):
            i += 1

        j = i
        while ('0' <= args[j] and args[j] <= '9'):
            j += 1

        try:
            lines_reqd = (int)(args[i:j])
            filename = args[j+1:]
        except Exception as err:
            utils.ErrorPrint("tail: Invalid args: {0}\n".format(args))
            utils.ErrorPrint("tail: {0}\n".format(err))
            return

    try:
        with open(filename, 'r') as f:
            try:
                while (lines_reqd > 0):
                    line = next(f)
                    print (line, end="")
                    lines_reqd -= 1

            except StopIteration:
                pass

    except Exception as err:
        utils.ErrorPrint("tail: {0}: {1}\n".format(filename, err))







if __name__ == "__main__":
    utils.screen_clear()
    utils.BoldPrint("Pyshell Started...\n\n")

    curr_dir = os.getcwd()
    prev_dir = ""
    while(True):
        PromptPrint()
        ip_cmd = input()

        cmd, args = CommandExtract(ip_cmd)
        #cmd_list = ip_cmd.split()
        #if (len(cmd_list) == 0):
        if (cmd == ""):
            continue

        #if (cmd_list[0] == EXIT):
        if (cmd == EXIT):
            break

        #cmd = cmd_list[0]
        #del cmd_list[0]
        #args = ' '.join([str(a) for a in cmd_list])

        if (args != "" and args[0] == "\""):
            args = args[1:]
            args = args[:len(args) - 1]

        if (cmd == CD):
            if cd_run(args, prev_dir, curr_dir) == SUCCESS:
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

        elif (cmd == TAIL):
            tail_run(args)

        elif (cmd == HEAD):
            head_run(args)

        else:
            utils.ErrorPrint ("'{0}': command not found\n".format(cmd))

    utils.screen_clear()
    utils.BoldPrint("Pyshell Exited...\n\n")
