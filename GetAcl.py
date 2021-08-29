import subprocess


def run(cmd):
    completed = subprocess.run(["powershell",cmd], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return completed


def to_string_form(input):
    stringForm= str(input).replace("\\n" , "\n").replace("\\r" , "")
    return stringForm


def get_acl(path):
    command="get-acl \"{}\" | fl".format(path)
    _cmd= run(command)
    if _cmd.returncode == 0 :
        output = to_string_form(_cmd.stdout)
        output = output [output.find("Access") : output.find("Audit")]
        return output 
    else :
        return to_string_form(_cmd.stdout)
