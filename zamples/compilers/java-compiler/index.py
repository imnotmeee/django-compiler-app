import subprocess

java_file = "Index.java"
class_file = "Index"

# Open the Java file using the subprocess module
process = subprocess.Popen(
    ["javac", java_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

process.wait()
process = subprocess.Popen(
    ["java", class_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# Get the output and error messages from the process
output, error = process.communicate()
output = str(output.strip()).strip("'")[2:]
error = str(error.strip()).strip("'")[2:]

# Print the output
print(f'output {output}')

# If there was an error, print it
if error:
    print(f'error {error}')
