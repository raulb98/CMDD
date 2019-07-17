import os
import shutil
import sys
import argparse
import signal
import winreg

HashKeys = {"HKEY_CLASSES_ROOT" : 2147483648,
            "HKEY_CURRENT_CONFIG" : 2147483653,
            "HKEY_LOCAL_MACHINE" : 2147483650,
            "HKEY_USERS" : 2147483651,
            "HKEY_CURRENT_USER" : 2147483649}

parser = argparse.ArgumentParser()
parser.add_argument('-pwd',help="Shows the current absolute path", action="store_true")
parser.add_argument('-cd', nargs=1,help="Changes the directory according to the arg1 path (there is also the cd .. command)")
parser.add_argument('-mkdir', nargs=1,help="Creates a directory named arg1")
parser.add_argument('-ls', action="store_true",help="Shows every directory/file in the current directory")
parser.add_argument('-rmdir',nargs=1,help="Removes the directory and all subdirectories of the arg1")
parser.add_argument('-mkfile', nargs=1,help="Creates a file named arg1")
parser.add_argument('-del', nargs=1,help="Deletes a file named arg1")
parser.add_argument('-cpy', nargs=2,help="Copyes the first arguments file/directory) in the second argument")
parser.add_argument('-move', nargs=2,help=" Moves the entire tree of subdirectories or file to the second arguments(path)")
parser.add_argument('-info', action="store_true",help="Shows the details regardiing size,last acces,etc.. of the directory/file")
parser.add_argument('-tasklist',action="store_true",help="All processes")
parser.add_argument('-taskillP',nargs=1,help="Kill Process by ID")
parser.add_argument('-taskillN',nargs=1,help="Kill Process by Name")
parser.add_argument('-reglistkey',nargs=1,help="List all the subkeys of a register")
parser.add_argument('-reglistval',nargs=1,help="List all values of a key")
parser.add_argument('-regaddkey',nargs=2,help="Adds a new key")
parser.add_argument('-regaddval',nargs=3,help="Adds a new value")
parser.add_argument('-regdelkey',nargs=1,help="Deletes a key")
parser.add_argument('-regdelval',nargs=2,help="Deletes a value")
parser.add_argument('-reggetval',nargs=1,help="Selects a specified value")
parser.add_argument('-regsetval',nargs=3,help="Sets a specified value")
parser.add_argument('-regcopykey',nargs=2,help="Links 2 keys")
args = parser.parse_args()


##################################### CMD
def copy(src,dest):
    try:
        shutil.copytree(src,dest)
    except OSError as e:
        if os.path.isfile(src):
            shutil.copy(src,dest)
        else:
            print('Directory not copied. Error: {}'.format(e))

def cd(Splited_Command,Splited_Current_Directory):
    if (Splited_Command == ".."):
        Number_Of_Elements = len(Splited_Current_Directory)
        current = ""
        for i in range(0, Number_Of_Elements - 1):
            if (i != Number_Of_Elements - 2):
                current = current + Splited_Current_Directory[i] + '\\'
            else:
                current = current + Splited_Current_Directory[i]
    else:
        current = Splited_Command
    return current

def mkfile(Splited_Command,Splited_Current_Directory,Current):
    Path = Splited_Command.split('\\')
    if (len(Path) == 1):
        if not os.path.isfile(os.path.join(Current, Splited_Command)):
            open(os.path.join(Current, Splited_Command), 'w').close()
    else:
        if not os.path.isfile(Splited_Command):
            open(Splited_Command, 'w').close()
        else:
            print("There is already a file named" + Splited_Command)

def move(src,dest):
    if os.path.exists(dest):
        try:
            shutil.move(src,dest)
            return dest
        except OSError as e:
            if os.path.isfile(src):
                shutil.move(src,dest)
            else:
                print('Directory or file not copied. Error: {}'.format(e))

def delete(src):
    if not os.path.exists(src):
        try:
            if os.path.isfile(src):
                os.remove(src)
            else:
                print("There is not file named" + src)
        except Exception as e:
            raise Exception(e)

def mkdir(src):
    if not os.path.exists(src):
        try:
            if not os.path.isdir(src):
                os.makedirs(src)
            else:
                print("There is already a director named" + src)
        except Exception as e:
            raise Exception(e)

def rmdir(src):
    if os.path.exists(src):
        try:
            if os.path.isdir(src):
                shutil.rmtree(src)
            else:
                print("There is no director named" + src)
        except Exception as e:
            raise Exception(e)

def info(src):
    if os.path.exists(src):
        try:
            if os.path.isfile(src):
                print("Size : {}".format(os.path.getsize(src)))
                print("Modify Time : {}".format(os.path.getmtime(src)))
                print("Last Acces Time : {}".format(os.path.getatime(src)))
            elif os.path.isdir(src):
                Nr_Items_In_Directory = len(os.listdir(src))
                print("Number of files/dirs : {}".format(str(Nr_Items_In_Directory)))
                print("Modify Time : {}".format(os.path.getmtime(src)))
                print("Last Acces Time : {}".format(os.path.getatime(src)))
            else:
                print("There is no director/file named" + src)
        except Exception as e:
            raise Exception(e)

def ls(src):
    if os.path.exists(src):
        try:
            for item in os.listdir(src):
                if os.path.isdir(item):
                    print(item + " -- director")
                elif os.path.isfile(item):
                    print(item + " -- file")
                else:
                    print(item + " -- director")
        except Exception as e:
            raise Exception(e)
##################################################  CMD
##################################################  Processes
def tasklist():
    try:
        proces = os.popen('tasklist | sort /R /+58','r')
        print(proces.read())
    except Exception as e :
        raise Exception(e)

def taskillP(pid):
    try:
        os.kill(int(pid),signal.SIGTERM)
    except Exception as e :
        raise Exception(e)

def taskillN(name):
    try:
        tasks = os.popen('tasklist','r')
        sh = tasks.read().split(' ')
        while '' in sh:
            sh.remove('')
        for i in range(0,len(sh)):
              if sh[i] == "K\n"+name:
                os.kill(int(sh[i+1]),signal.SIGTERM)
                return
    except Exception as e :
        raise Exception(e)
######################################################## Processes
######################################################## Registers
def reglistkey(src):
    try:
        rez = []
        if src[1] != '':
            Key = winreg.OpenKey(src[0], src[1] + '\\' + src[2], 0, winreg.KEY_ALL_ACCESS)
        else:
            Key = winreg.OpenKey(src[0], src[2], 0, winreg.KEY_ALL_ACCESS)
        size = winreg.QueryInfoKey(Key)[0]
        for i in range(size):
            rez.append(winreg.EnumKey(Key,i))
        return rez
    except Exception as e:
        print("Could not list he keys and the subkeys")

def reglistval(src):
    try:
        if src[1] != '':
            key = winreg.OpenKey(src[0], src[1] + '\\' + src[2], 0, winreg.KEY_ALL_ACCESS)
        else:
            key = winreg.OpenKey(src[0], src[2], 0, winreg.KEY_ALL_ACCESS)
        size = winreg.QueryInfoKey(key)[1]
        rez = []
        for i in range(size):
            rez.append(winreg.EnumValue(key,i))
        return rez
    except Exception as e :
        print("Could not list the values of the key")


def regaddkey(src,newkey):
    try:
        if src[1] != '':
            key = winreg.OpenKey(src[0],src[1]+'\\'+src[2],0,winreg.KEY_ALL_ACCESS)
        else:
            key = winreg.OpenKey(src[0],src[2], 0, winreg.KEY_ALL_ACCESS)
        x = winreg.CreateKey(key,newkey)
        print(x)
        return x
    except Exception as e :
        print("Could not add key")

def regaddval(src,loc,newval):
    try:
        if src[1] != '':
            key = winreg.OpenKey(src[0], src[1] + '\\' + src[2], 0, winreg.KEY_ALL_ACCESS)
        else:
            key = winreg.OpenKey(src[0], src[2], 0, winreg.KEY_ALL_ACCESS)
        winreg.SetValueEx(key,loc,0,winreg.REG_SZ,newval)
    except Exception as e:
        print("Could not add value")

def regdelkey(src):
    try:
            R = reglistkey(src)
            if len(R) != 0:
                for i in range(len(R)):
                    print('len(R) = ' + str(len(R)))
                    rez = []
                    rez.append(src[0])
                    rez.append(src[1]+'\\'+src[2])
                    rez.append(R[i])
                    regdelkey(rez)
            R = reglistkey(src)
            if len(R) == 0:
                Key = winreg.OpenKey(src[0], src[1], 0, winreg.KEY_ALL_ACCESS)
                winreg.DeleteKey(Key,src[2])

    except Exception as e:
        print("Nothing to delete")


def regdelval(src,val):
    try:
        if src[1] != '':
            Key = winreg.OpenKey(src[0], src[1] + '\\' + src[2], 0, winreg.KEY_ALL_ACCESS)
        else:
            Key = winreg.OpenKey(src[0], src[2], 0, winreg.KEY_ALL_ACCESS)
        winreg.DeleteValue(Key, val)
    except Exception as e:
        print("Nothing to delete")

def reggetval(src,val):
    try:
        rez = ""
        if src[1] != '':
            Key = winreg.OpenKey(src[0], src[1] + '\\' + src[2], 0, winreg.KEY_ALL_ACCESS)
        else:
            Key = winreg.OpenKey(src[0], src[2], 0, winreg.KEY_ALL_ACCESS)
        size = winreg.QueryInfoKey(Key)[1]
        for i in range(size):
            valoare = winreg.EnumValue(Key,i)
            if valoare[0] == val:
                rez = valoare[1]

        if rez != "" :
            print(rez)
        else:
            print("No element found")
    except Exception as e:
        raise Exception(e)

def regsetval(src,valname,val):
    try:
        if src[1] != '':
            Key = winreg.OpenKey(src[0], src[1] + '\\' + src[2], 0, winreg.KEY_ALL_ACCESS)
        else:
            Key = winreg.OpenKey(src[0], src[2], 0, winreg.KEY_ALL_ACCESS)
        print(Key)
        size = winreg.QueryInfoKey(Key)[1]
        for i in range(size):
            valoare = winreg.EnumValue(Key, i)
            if valoare[0] == valname:
                winreg.SetValueEx(Key,valname,0,winreg.REG_SZ,val)
    except Exception as e:
        print("Could not set the Value of the key")


def regcopykey(dest,src):
    try:
        R = reglistkey(src)
        print(R)
        if len(R) == 0:
            y = regaddkey(src,src[2])
            KeyDest = winreg.OpenKey(dest[0],dest[1]+'\\'+dest[2],0,winreg.KEY_ALL_ACCESS)
            KeySrc = winreg.OpenKey(src[0],src[1]+'\\'+src[2],0,winreg.KEY_ALL_ACCESS)
            size = winreg.QueryInfoKey(KeySrc)[1]
            for i in range(size):
                valoare = winreg.EnumValue(KeySrc, i)
                winreg.SetValueEx(KeyDest,valoare[0],0,winreg.REG_SZ,valoare[1])
            regdelkey(src)
        else:
            for i in range(len(R)):
                rez = []
                rez.append(src[0])
                rez.append(src[1] + '\\' + src[2])
                rez.append(R[i])
                regcopykey(dest,rez)

    except Exception as e:
        print("Could not copy the elements")
################################################################ Registers
def mysplit(splited):
    z = splited.split('\\')
    x = []
    x.append(z[0])
    y = ""
    for i in range(1, len(z) - 1):
        if (i != len(z) - 2):
            y = y + z[i] + '\\'
        else:
            y = y + z[i]
    x.append(y)
    x.append(z[len(z) - 1])
    return x

def execute(command, Current_Directory):
    Splited_Command = command.split(' ')
    #split la comanda dupa spatii
    Splited_Current_Directory = Current_Directory.split('\\')
    #split la calea curenta dupa caracterul '\'
    nr1 = len(Splited_Current_Directory)
    nr2 = len(Splited_Command)
    commandList = ["info","rmdir","mkdir","--help","-help","del",
                   "mkfile","pwd","cd","cpy","move","ls","tasklist",
                   "taskillP","taskillN","reglistkey","reglistval",
                   "regaddkey","regaddval","regdelkey","regdelval","reggetval",
                   "regsetval","regcopykey","regcopykey"]

    for i in commandList:
        #splited[0] = nume comanda ('cd','pwd',etc...)
        if Splited_Command[0] == i:
            if(Splited_Command[0] == "--help" or Splited_Command[0] == "-help"):
                args.help

            elif(Splited_Command[0] == "pwd"):
                print(Current_Directory)

            elif(Splited_Command[0] == "cd"):
                if Splited_Command[1] != "..":
                    if not os.path.isdir(Splited_Command[1]):
                        print("There is no directory named {}".format(Splited_Command[1]))
                        return Current_Directory
                Current_Directory = cd(Splited_Command[1],Splited_Current_Directory)

            elif Splited_Command[0] == "mkfile":
                if len(Splited_Command) == 2:
                    mkfile(Splited_Command[1],Splited_Current_Directory,Current_Directory)
                else:
                    print("Incorect Number of Arguments")

            elif Splited_Command[0] == "cpy" :
                if len(Splited_Command) == 3:
                    copy(Splited_Command[1],Splited_Command[2])
                else:
                    print("Incorect Number of Arguments")

            elif Splited_Command[0] == "move":
                if len(Splited_Command) == 3:
                   Current_Directory =  move(Splited_Command[1],Splited_Command[2])
                else:
                    print("Incorect Number of Arguments")

            elif Splited_Command[0] == "del":
                if len(Splited_Command) == 2:
                    delete(Splited_Command[1])
                else:
                    print("Incorect Number of Arguments")

            elif Splited_Command[0] == "mkdir":
                if len(Splited_Command) == 2:
                    mkdir(Splited_Command[1])
                else:
                    print("Incorect Number of Arguments")

            elif Splited_Command[0] == "rmdir":
                if len(Splited_Command) == 2:
                    rmdir(Splited_Command[1])
                else:
                    print("Incorect Number of Arguments")
            elif Splited_Command[0] == "info":
                if len(Splited_Command) == 2:
                    info(Splited_Command[1])
                else:
                    print("Incorect Number of Arguments")
            elif Splited_Command[0] == "ls":
                if len(Splited_Command) == 1:
                    ls(Current_Directory)
                else:
                    print("Incorect Number of Arguments")
            elif Splited_Command[0] == "tasklist":
                if len(Splited_Command) == 1:
                    tasklist()
                else:
                    print("Incorect Number of Args")
            elif Splited_Command[0] == "taskillP":
                if len(Splited_Command) == 2:
                    taskillP(Splited_Command[1])
                else:
                    print("Incorect Number of Args")
            elif Splited_Command[0] == "taskillN":
                if len(Splited_Command) == 2:
                    taskillN(Splited_Command[1])
                else:
                    print("Incorect Number of Args")
            elif Splited_Command[0] == "reglistkey":
                if len(Splited_Command) == 2:
                    Reg_Path_Split = mysplit(Splited_Command[1])
                    key = []
                    key.append(HashKeys[Reg_Path_Split[0]])
                    key.append(Reg_Path_Split[1])
                    key.append(Reg_Path_Split[2])
                    rez = reglistkey(key)
                    print(rez)
                else:
                    print("Incorect Number of Args")
            elif Splited_Command[0] == "reglistval":
                if len(Splited_Command) == 2:
                    Reg_Path_Split = mysplit(Splited_Command[1])
                    key = []
                    key.append(HashKeys[Reg_Path_Split[0]])
                    key.append(Reg_Path_Split[1])
                    key.append(Reg_Path_Split[2])
                    rez = reglistval(key)
                    print(rez)
                else:
                    print("Incorect Number of Args")
            elif Splited_Command[0] == "regaddkey":
                print(len(Splited_Command))
                if len(Splited_Command) == 3:
                    Reg_Path_Split = mysplit(Splited_Command[1])
                    key = []
                    key.append(HashKeys[Reg_Path_Split[0]])
                    key.append(Reg_Path_Split[1])
                    key.append(Reg_Path_Split[2])
                    regaddkey(key,Splited_Command[2])
                else:
                    print("Incorect Number of Args")
            elif Splited_Command[0] == "regaddval":
                if len(Splited_Command) == 4:
                    Reg_Path_Split = mysplit(Splited_Command[1])
                    key = []
                    key.append(HashKeys[Reg_Path_Split[0]])
                    key.append(Reg_Path_Split[1])
                    key.append(Reg_Path_Split[2])
                    regaddval(key,Splited_Command[2],Splited_Command[3])
                else:
                    print("Incorect Number of Args")
            elif Splited_Command[0] == "regdelkey":
                if len(Splited_Command) == 2:
                    Reg_Path_Split = mysplit(Splited_Command[1])
                    key = []
                    key.append(HashKeys[Reg_Path_Split[0]])
                    key.append(Reg_Path_Split[1])
                    key.append(Reg_Path_Split[2])
                    regdelkey(key)
                else:
                    print("Incorect Number of Args")
            elif Splited_Command[0] == "regdelval":
                if len(Splited_Command) == 3:
                    Reg_Path_Split = mysplit(Splited_Command[1])
                    key = []
                    key.append(HashKeys[Reg_Path_Split[0]])
                    key.append(Reg_Path_Split[1])
                    key.append(Reg_Path_Split[2])
                    regdelval(key,Splited_Command[2])
                else:
                    print("Incorect Number of Args")
            elif Splited_Command[0] == "reggetval":
                if len(Splited_Command) == 3:
                    Reg_Path_Split = mysplit(Splited_Command[1])
                    key = []
                    key.append(HashKeys[Reg_Path_Split[0]])
                    key.append(Reg_Path_Split[1])
                    key.append(Reg_Path_Split[2])
                    reggetval(key,Splited_Command[2])
                else:
                    print("Incorect Number of Args")
            elif Splited_Command[0] == "regsetval":
                if len(Splited_Command) == 4:
                    Reg_Path_Split = mysplit(Splited_Command[1])
                    key = []
                    key.append(HashKeys[Reg_Path_Split[0]])
                    key.append(Reg_Path_Split[1])
                    key.append(Reg_Path_Split[2])
                    regsetval(key,Splited_Command[2],Splited_Command[3])
                else:
                    print("Incorect Number of Args")
            elif Splited_Command[0] == "regcopykey":
                if len(Splited_Command) == 3:
                    x1 = mysplit(Splited_Command[1])
                    x2 = mysplit(Splited_Command[2])
                    key1 = []
                    key2 = []
                    key1.append(HashKeys[x1[0]])
                    key1.append(x1[1])
                    key1.append(x1[2])
                    key2.append(HashKeys[x2[0]])
                    key2.append(x2[1])
                    key2.append(x2[2])
                    regcopykey(key1,key2)
                else:
                    print("Incorect Number of Args")
            return Current_Directory
    print("There is no such command")
    return Current_Directory

def main():
    print(">> Command line <<")
    currDir = os.getcwd()
    #currDir = director curent in care este scriptul
    if len(sys.argv) > 1:
        nr = len(sys.argv)
        command = ""
        for i in range(1, nr):
            #extragere informatii din linia de comanda pt task 2
            if (i != nr - 1):
                if i == 1:
                    command = command + sys.argv[i][1:] + ' '
                else:
                    command = command + sys.argv[i] + ' '
            else:
                if i == 1:
                    command = command + sys.argv[i][1:]
                else:
                    command = command + sys.argv[i]
        print(command)
        execute(command, currDir)
        return
    #creeare bucla infinta pt simulare (aka bash)
    quit = False
    while quit != True:
        args.command = ""
        args.command = input(currDir + " >>> ")
        if args.command != "quit":
            os.chdir(currDir)
            currDir = execute(args.command,currDir)
        else:
            quit = True

if __name__ == "__main__":
    main()