import subprocess

def call(cmdline):
    output = subprocess.check_output(cmdline)
    lines = output.splitlines()
    lines = [line.decode("utf-8") for line in lines]
    return lines
