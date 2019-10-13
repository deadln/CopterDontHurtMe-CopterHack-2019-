import paramiko

host = "192.168.11.1"
user = ""
pas = "raspberry"

client = paramiko.SSHClient()
#client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=host, password=pas)
stdin, stdout, stderr = client.exec_command('python sq_mk.py')
data = stdout.read() + stderr.read()
print data
client.close()
