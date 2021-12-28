import subprocess

out = subprocess.Popen(['docker', 'image', 'ls', '-a'], stdout=subprocess.PIPE,stderr=subprocess.STDOUT)

stdout, stderr = out.communicate()
id = " ".join(str(stdout).split()).split(' ')

for i in id:
    if len(i) == 12 and '\'' not in i:
        print(i, end=' ')