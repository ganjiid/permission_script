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
    users_cmd= run("Get-LocalUser | Select name")
    if users_cmd.returncode == 0 :
        users =  to_string_form(users_cmd.stdout).split("\n" ) [3:-3]
        for i in range(len(users)):
            users[i]= users[i].strip()
        return users
    else:
        return None


def get_acl(path):
    command="get-acl \"{}\" | fl".format(path)
    _cmd= run(command)
    if _cmd.returncode == 0 :
        output = to_string_form(_cmd.stdout)
        output = output [output.find("Access") : output.find("Audit")]
        return output 
    else :
        return to_string_form(_cmd.stdout)


def set_acl(path , user , acl_type ):
    command=[   "$acl = Get-Acl \"{}\"".format(path),
                "$AccessRule = New-Object System.Security.AccessControl.FileSystemAccessRule(\"{}\",\"{}\",\"ContainerInherit,ObjectInherit\",\"None\",\"Allow\")".format(user , acl_type),
                "$acl.SetAccessRule($AccessRule)",
                "$acl | Set-Acl \"{}\"".format(path)
    
    ]
    _cmd= run_multiple(command)
    out, err = _cmd.communicate()
    if _cmd.returncode == 0 :
        return "Successful !"
    else :
        return to_string_form(out)


def remove_acl(path , user , acl_type ):
    command=[   "$acl = Get-Acl \"{}\"".format(path),
                "$AccessRule = New-Object System.Security.AccessControl.FileSystemAccessRule(\"{}\",\"{}\",\"ContainerInherit,ObjectInherit\",\"None\",\"Allow\")".format(user , acl_type),
                "$acl.RemoveAccessRule($AccessRule)",
                "$acl | Set-Acl \"{}\"".format(path)
    
    ]
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
