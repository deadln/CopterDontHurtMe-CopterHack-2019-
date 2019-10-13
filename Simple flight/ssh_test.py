import paramiko

host = "192.168.11.1"
user = "pi"
pas = "raspberry"

client = paramiko.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=host, username=user, password=pas)
stdin, stdout, stderr = client.exec_command('python sq_mk.py 3 3 3 1 0 1')
data = stdout.read() + stderr.read()
print data
client.close()
