import subprocess


completed = subprocess.run(["python3", "others.py"],
                           capture_output=True,
                           text=True)
print("args", completed.args)
print("returncode", completed.returncode)
print("stderr", completed.stderr)
print("stdout", completed.stdout)


try:
    completed = subprocess.run(["false"],
                               capture_output=True,
                               text=True,
                               check=True
                               )

    print("args", completed.args)
    print("returncode", completed.returncode)
    print("stderr", completed.stderr)
    print("stdout", completed.stdout)
except subprocess.CalledProcessError as ex:
    print(ex)
