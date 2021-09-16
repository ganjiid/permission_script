import subprocess


def run(cmd):
    completed = subprocess.run(["powershell",cmd], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return completed


def to_string_form(input):
    stringForm= str(input).replace("\\n" , "\n").replace("\\r" , "")
    return stringForm


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

    

def write_file(data):
    f = open("PermissionOutput.txt", "w")
    f.write(data)
    f.close()