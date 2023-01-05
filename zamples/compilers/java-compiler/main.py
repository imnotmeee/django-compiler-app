import subprocess
import os

java_program = "Index.java"
subprocess.call(["javac", java_program])
process = subprocess.Popen(["java", "Index"], stdout=subprocess.PIPE)
for line in process.stdout:
    print(line.decode('utf-8'))

try:
    os.remove(java_program.replace('java', 'class'))
except FileNotFoundError:
    print(f"The file {java_program.replace('java', 'class')} does not exist")
