import os
import socket
import traceback
import getpass
import paramiko
import pysftp

from paramiko import SSHClient

def get_auth(host, port, user, password=None, key=None):
    username = getpass.getuser()
    if user != None:
        username = user
    t = get_transport(host, port)
    t.auth_none(username)
    return t

def get_transport(host, port=22):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
    except Exception as e:
        print('*** Connect failed: ' + str(e))
        traceback.print_exc()

    try:
        t = paramiko.Transport(sock)
        try:
            t.start_client()
            return t
        except paramiko.SSHException:
            print('*** SSH negotiation failed.')
        try:
            keys = paramiko.util.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
        except IOError:
            try:
                keys = paramiko.util.load_host_keys(os.path.expanduser('~/ssh/known_hosts'))
            except IOError:
                print('*** Unable to open host keys file')
                keys = {}
        # check server's host key -- this is important.
        key = t.get_remote_server_key()
        print 'Key %r' % key
        if host not in keys:
            print('*** WARNING: Unknown host key!')
        elif key.get_name() not in keys[host]:
            print('*** WARNING: Unknown host key!')
        elif keys[host][key.get_name()] != key:
            print('*** WARNING: Host key has changed!!!')
        else:
            print('*** Host key OK.')
    except Exception as e:
        print('*** Caught exception: ' + str(e.__class__) + ': ' + str(e))
        traceback.print_exc()
        try:
            t.close()
        except:
            pass

def rexists(sftp, path):
    """os.path.exists for paramiko's SCP object
    """
    try:
        sftp.stat(path)
    except IOError, e:
        if e[0] == 2:
            return False
        raise
    else:
        return True


def transfer_file(file_src, file_target, target_dir, host, port=22, username=getpass.getuser(), password=None):
    try:
        t = paramiko.Transport(host, port)
        t.connect(None, username, password, gss_host=socket.getfqdn(host))
        sftp = paramiko.SFTPClient.from_transport(t)
        if target_dir != None:
            if not rexists(sftp, target_dir):
                sftp.mkdir(file_target, mode=755)
            if not target_dir.endswith('/'):
                target_dir = target_dir + '/'
            print 'Pasting source file %r ' % file_src
            sftp.put(file_src, target_dir + file_target)
        else:
            sftp.put(file_src, file_target)
    except Exception as e:
        print 'SFTP Failure %r' % e
        traceback.print_exc()

def execute_script(script_loc, script_name, host, port=22, username=getpass.getuser(), password=None, change_user='root'):
    client = SSHClient()
    client.load_system_host_keys()
    client.connect(host, username=username, password=password)
    stdin, stdout, stderr = client.exec_command('sudo -u %s' % change_user + ';cd %s' % script_loc + ';' + './%s' % script_name)
    return stdout, stderr

def execute_command(command, host, port=22, username=getpass.getuser(), password=None, change_user='root'):
    client = SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.load_system_host_keys()
    client.connect(host, username=username, password=password)
    stdin, stdout, stderr = client.exec_command(command)
    return stdout, stderr

def sftp_file(file_src, file_target, target_dir, host, port=22, username=getpass.getuser(), password=None):
    with pysftp.Connection(host, username=username, password=password) as sftp:
        sftp.put(file_src, target_dir + '/' + file_target)