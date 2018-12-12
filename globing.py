# coding=utf8
# the above tag defines encoding for this document and is for Python 2.x compatibility

import re, os


def pre_output(pattern):
    string = ""
    for i in pattern:
        if i != "." and i != "/":
            break
        string += i
    return string

def findMatching(pattern, string):
    """result[0]: list file, result[1]: list dir"""
    try:
        message_nonexist = "'{0}': No such file or directory..".format(pattern)
        pre_dir = pre_output(pattern)
        current_directory = forward_directory(pattern)
        result = [[], []]
        pattern = pattern[len(pre_dir):]
        if(pattern[0] != "*"):
            pattern = "^" + pattern
        patte= handle_bracket(pattern)
        pattern = pattern.replace("*", ".*")
        pattern = pattern.replace("?", "[A-Za-z0-9]")
        for ele in string:
            matches = re.finditer(pattern, ele)
            if len(list(matches)) > 0:
                if os.path.isfile(ele):
                    ele = pre_dir + ele
                    result[0].append(ele)
                else:
                    ele = pre_dir + ele
                    result[1].append(ele)
        os.chdir(current_directory)
        if(len(result[0]) ==0 and len(result[1]) == 0):
            return message_nonexist
        return result
    except:
        return message_nonexist



def handle_bracket(string):
    i = 0
    while i < (len(string) - 1):
        if string[i] == '[':
            temp = ""
            for j in range(i+1, len(string)):
                if(string[j] == ']'):
                    break
                temp += string[j]
            temp = '[' + temp + ']'
            replace = '(' + temp.lower() + '|'
            replace += temp.upper() + ')'
            string = string.replace(temp, replace)
            i += len(replace) - 1
        i += 1
    return string


def handle_ls(lst):
    try:
        current_directory = forward_directory("../*")
        if type(lst) != list:
            print("ls: cannot access {0}".format(lst))
            exit()
        if len(lst[0]) > 0:
            lst[0].sort(key=lambda str: str.lower())
        if len(lst[1]) > 0:
            lst[1].sort(key=lambda str: str.lower())
        for file in lst[0]:
            print(file, end='  ')
        if len(lst[1]) > 0:
            print()
        for dir in lst[1]:
            print()
            print(dir, end=":")
            if(len(os.listdir(dir)) != 0):
                 print()
            print('  '.join(sorted(os.listdir(dir))))
    except:
        raise("Error: 'handle_ls' function")


def forward_directory(pattern):
    current_directory = os.getcwd()
    for i in range(len(pattern[:-2])):
        if pattern[i:i+3] == "../":
            os.chdir("../")
    return current_directory
