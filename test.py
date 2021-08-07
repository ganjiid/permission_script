import subprocess

commands = [
    "New-Item -Path 'C:/Users/fanni/Desktop/Python/test' -ItemType directory",
    "New-Item -Path 'C:/Users/fanni/Desktop/Python/test/new.txt' -ItemType File",
    "Set-Content C:/Users/fanni/Desktop/Python/test/new.txt 'Curse You!'"
]


print(commands)
def run(cmd):
    completed = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
    return completed

def run_a_list_of_commands(cmd_list):
    output = str()
    for cmd in cmd_list :
        output = output + cmd + '\n'
    _info = run(output)


def append_commands_to_set(cmd):
    commands.append(cmd)


run_a_list_of_commands(commands)

input("press any key !")

#hello_info = run(commands[2])

