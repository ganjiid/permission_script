import subprocess




def run(cmd):
    completed = subprocess.run(["powershell",cmd], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return completed


def run_multiple(cmds):
    Process = subprocess.Popen(["powershell"],
                               stdin=subprocess.PIPE, 
                               stdout = subprocess.PIPE,
                               universal_newlines=True,
                               bufsize=0,
                               stderr=subprocess.STDOUT)
    for cmd in cmds:
        Process.stdin.write(cmd + "\n")
    Process.stdin.close()
    
    return Process


def to_string_form(input):
    stringForm= str(input).replace("\\n" , "\n").replace("\\r" , "")
    return stringForm


def get_users ():
    users_cmd= run("net users /domain")
    if users_cmd.returncode == 0 :
        output = to_string_form(users_cmd.stdout)
        output = output [output.find("User accounts") : output.find("The command")] 
        output = output.split("\n",3)[2]
        users =  output.split()
        return users
    else:
        return None


def single_get_acl(path):
    command="get-acl \"{}\" | fl".format(path)
    _cmd= run(command)
    if _cmd.returncode == 0 :
        output = to_string_form(_cmd.stdout)
        output = output [output.find("Access") : output.find("Audit")]
        return output 
    else :
        return to_string_form(_cmd.stdout)

def get_subfolder(path):
    command="Get-ChildItem \"{}\" -dir -name".format(path)
    _cmd= run(command)
    if _cmd.returncode == 0 :
        output = to_string_form(_cmd.stdout).split("\n")[:-1]
        if len(output):
            output[0] = output[0][2:]
        return output 
    else :
        print (to_string_form(_cmd.stdout))
        return []

def sub_folders_pathes(path , dep_num):
    pathes =[ [path] , [] , [] ]
    
    for x in range(dep_num-1):
        for _path in pathes[x]:
            Dsubfolders = get_subfolder(_path)
            for subfolder in Dsubfolders :
                pathes[x+1].append(_path + "/" + subfolder)

    result = pathes[0] + pathes[1] + pathes[2]
    
    return result



def get_acl(path , dep_num):
    results= dict()
    all_folders = sub_folders_pathes(path, dep_num)
    for _path in all_folders:
        results [_path] = single_get_acl(_path)
    f = open("PermissionOutput.txt", "w")
    for folder , result in  results.items() :
        f.write(folder + "\n\n" + result + "\n*************************\n")
    f.close()
    return "see \"PermissionOutput.txt\" file"
    




def set_acl(inheritance , path , user , acl_type ):
    command=[   "$acl = Get-Acl \"{}\"".format(path),
                "$AccessRule = New-Object System.Security.AccessControl.FileSystemAccessRule(\"{}\",\"{}\",\"ContainerInherit,ObjectInherit\",\"None\",\"Allow\")".format(user , acl_type),
                "$acl.SetAccessRule($AccessRule)",
                "$acl | Set-Acl \"{}\"".format(path)
    
    ]
    if not inheritance :
        command[1]="$AccessRule = New-Object System.Security.AccessControl.FileSystemAccessRule(\"{}\",\"{}\",\"Allow\")".format(user , acl_type)
    _cmd= run_multiple(command)
    out, err = _cmd.communicate()
    if _cmd.returncode == 0 :
        return "Successful !"
    else :
        return to_string_form(out)


def remove_acl(inheritance , path , user , acl_type ):
    command=[   "$acl = Get-Acl \"{}\"".format(path),
                "$AccessRule = New-Object System.Security.AccessControl.FileSystemAccessRule(\"{}\",\"{}\",\"ContainerInherit,ObjectInherit\",\"None\",\"Allow\")".format(user , acl_type),
                "$acl.RemoveAccessRule($AccessRule)",
                "$acl | Set-Acl \"{}\"".format(path)
    
    ]
    if not inheritance :
        command[1]="$AccessRule = New-Object System.Security.AccessControl.FileSystemAccessRule(\"{}\",\"{}\",\"Allow\")".format(user , acl_type)
    _cmd= run_multiple(command)
    out, err = _cmd.communicate()
    if _cmd.returncode == 0 :
        return "Successful !"
    else :
        return to_string_form(out)



def purge_acl(path , user ):
    command=[   "$acl = Get-Acl \"{}\"".format(path),
                "$usersid = New-Object System.Security.Principal.Ntaccount (\"{}\")".format(user),
                "$acl.PurgeAccessRules($usersid)",
                "$acl | Set-Acl \"{}\"".format(path)
    
    ]
    _cmd= run_multiple(command)
    out, err = _cmd.communicate()
    if _cmd.returncode == 0 :
        return "Successful !"
    else :
        return to_string_form(out)
