import subprocess
import os
import re
from datetime import datetime
from datetime import timedelta
from pytz import timezone


def humanize_date(date):
    # Get the current time in the given time zone.
    current_time = datetime.now(timezone("US/Pacific"))

    # Calculate the difference between the given date and the current time.
    delta = current_time - date

    # If the difference is less than a second, return "just now".
    if delta < timedelta(seconds=1):
        return "just now"

    # If the difference is less than a minute, return "x seconds ago".
    elif delta < timedelta(minutes=1):
        return f"{delta.seconds} seconds ago"

    # If the difference is less than an hour, return "x minutes ago".
    elif delta < timedelta(hours=1):
        return f"{delta.seconds // 60} minutes ago"

    # If the difference is less than a day, return "x hours ago".
    elif delta < timedelta(days=1):
        return f"{delta.seconds // 3600} hours ago"

    # If the difference is less than a month, return "x days ago".
    elif delta < timedelta(days=30):
        return f"{delta.days} days ago"

    # If the difference is less than a year, return "x months ago".
    elif delta < timedelta(days=365):
        return f"{delta.days // 30} months ago"

    # If the difference is more than a year, return "x years ago".
    else:
        return f"{delta.days // 365} years ago"


def extension_of_lang(lang):
    if lang == "Java":
        return ".java"
    elif lang == "Python":
        return ".py"
    elif lang == "JavaScript":
        return ".js"
    elif lang == "Php":
        return ".php"
    elif lang == "Ruby":
        return ".rb"
    elif lang == "C++":
        return ".cpp"
    elif lang == "CSharp":
        return ".cs"
    elif lang == "Golang":
        return ".go"
    else:
        return ".java"


def check_what_language(post):
    if post.extension == '.py':
        return execute_python(post)
    elif post.extension == '.java':
        return execute_java(post)
    elif post.extension == '.php':
        return execute_php(post)
    elif post.extension == '.js':
        return execute_js(post)


def file_write(file, source):
    with open(file, "w") as f:
        f.write(source)


def remove_file_after(post):
    file = post.lang + post.extension
    try:
        os.remove(file)
        os.remove(post.lang + '.class')
    except FileNotFoundError:
        return f"The file {post.lang + '.class'} does not exist"


def to_array(string, is_str=False, is_js=False):
    output = []
    string = str(string.strip()).strip("'")[2:]
    if is_str:
        for err in string.split("\\n"):
            return err

    if is_js:
        for val in string.split("\\n"):
            output.append(val)
        return output

    for val in string.split("\\r\\n"):
        output.append(val)
    return output


def execute_java(post):
    file = post.lang + post.extension
    output = []
    src = re.sub(r"public class (\w+)",
                 r"public class " + post.lang, post.source)
    if 'Scanner(System.in)' in src:
        return {
            'output': 'Scanner is not supported.',
            'is_str': True,
            'is_err': True
        }
    file_write(file, src)
    try:
        process = subprocess.Popen(
            ["javac", file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.wait()
        process = subprocess.Popen(
            ["java", post.lang], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        out, error = process.communicate()

        output = to_array(out)
        error = to_array(error, True)

        if error:
            remove_file_after(post)
            return {
                'output': error,
                'is_str': True,
                'is_err': True
            }

        remove_file_after(post)
        return {
            'output': output,
            'is_str': False,
            'is_err': False
        }
    except:
        remove_file_after(post)
        return {
            'output': 'The code is not valid Java',
            'is_str': True,
            'is_err': True
        }


def execute_python(post):
    file = post.lang + post.extension
    file_write(file, post.source)
    output = ""

    try:
        output = subprocess.check_output(
            ['python', file], stderr=subprocess.STDOUT).strip()
        filtered_output = str(output).strip("'")[2:]
    except:
        remove_file_after(post)
        return {
            'output': 'The code is not valid Python',
            'is_err': True,
            'is_str': True
        }

    remove_file_after(post)

    return {
        'output': filtered_output,
        'is_err': False,
        'is_str': True
    }


def execute_php(post):
    file = post.lang + post.extension
    file_write(file, post.source)
    output = []

    result = subprocess.run(['php', file],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if 'error' in str(result):
        remove_file_after(post)
        return {
            'output': str(result.stderr),
            'is_err': True,
            'is_str': True
        }

    try:
        process = subprocess.Popen(["php", file], stdout=subprocess.PIPE)
        process.wait()
        filtered_output = str(process.stdout.read().strip()).strip("'")[2:]

        array = filtered_output.split(
            '<br/>') if '<br/>' in filtered_output else filtered_output.split('<br>')
        for val in array:
            output.append(val)
    except:
        remove_file_after(post)
        return {
            'output': 'The code is not valid Php script.',
            'is_err': True,
            'is_str': True
        }

    remove_file_after(post)
    return {
        'output': output,
        'is_err': False,
        'is_str': False
    }


def execute_js(post):
    javascript_code = post.source
    process = subprocess.Popen(
        ["node", "-e", javascript_code], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    output, error = process.communicate()

    output = to_array(output, False, True)
    error = to_array(error, True)

    if not error:
        return {
            'output': output,
            'is_str': False,
            'is_err': False
        }
    else:
        return {
            'output': error,
            'is_str': True,
            'is_err': True
        }
