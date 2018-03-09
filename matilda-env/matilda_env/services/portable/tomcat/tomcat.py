from matilda_env.services.portable import transfer
from matilda_env.services.portable import util

def install_tomcat(host, username=None, password=None):
    tomcat_tar_file = 'apache-tomcat-7.0.85.tar.gz'
    jdk_tar_file = 'jdk-8u161-linux-x64.tar.gz'
    source_dir = '/opt/matilda/matilda-env/matilda_env/services/portable/tomcat'
    transfer.sftp_file(source_dir + '/' + tomcat_tar_file, tomcat_tar_file, '/tmp', host, 22, username, password)
    transfer.sftp_file(source_dir + '/' + jdk_tar_file, jdk_tar_file, '/tmp', host, 22, username, password)
    transfer.transfer_file(source_dir + '/' + 'tomcat_install.sh', 'tomcat_install.sh', '/tmp', host, 22, username, password)
    #transfer.transfer_file(source_dir + '/' + 'tomcat_user_create.sh', 'tomcat_user_create.sh', '/tmp', host, 22, username, password)
    stdout, stderr = transfer.execute_command('chmod 755 /tmp/*.sh', host, 22, username, password,
                                             change_user='root')
    stdout, stderr = transfer.execute_command('sh /tmp/tomcat_user_create.sh', host, 22, username, password,
                                              change_user='root')
    stdout, stderr = transfer.execute_command('sh /tmp/tomcat_install.sh', host, 22, username, password,
                                              change_user='root')
    #stdout, stderr = transfer.execute_script('/tmp', 'tomcat_user_crete.sh', host, 22, username, password, change_user='root')
    #stdout, stderr = transfer.execute_script('/tmp', 'tomcat_install.sh', host, 22, username, password, change_user='tomcat')
    print 'Tomcat install output %r' % stdout
    print 'Tomcat install error %r' % stderr

def deploy_application(warfile_location, warfile_name, host, username=None, password=None):
    home = str(util.get_home_directory())
    if not home.endswith('/'):
        home = home + '/'
    transfer.sftp_file(warfile_location, '/tmp/' + warfile_name, home + 'apache-tomcat-7.0.85/webapps',
                           host, username, password)
    stdout, stderr = transfer.execute_command('sh /tmp/tomcat_restart.sh', host, 22, username, password,
                                              change_user='root')


