from matilda_env.services.portable import transfer
from matilda_env.services.portable import util

def install_mysql(host, username=None, password=None):
    mysql_tar_file = 'mysql-5.7.21-el7-x86_64.tar.gz'
    source_dir = '/opt/matilda/matilda-env/matilda_env/services/portable/mysql'
    transfer.sftp_file(source_dir + '/' + mysql_tar_file, mysql_tar_file, '/tmp', host, 22, username, password)
    transfer.transfer_file(source_dir + '/' + 'mysql_install.sh', 'mysql_install.sh', '/tmp', host, 22, username, password)
    #transfer.transfer_file(source_dir + '/' + 'tomcat_user_create.sh', 'tomcat_user_create.sh', '/tmp', host, 22, username, password)
    stdout, stderr = transfer.execute_command('chmod 755 /tmp/*.sh', host, 22, username, password,
                                             change_user='root')
    #stdout, stderr = transfer.execute_command('sh /tmp/tomcat_user_create.sh', host, 22, username, password,
    #                                          change_user='root')
    stdout, stderr = transfer.execute_command('sh /tmp/mysql_install.sh', host, 22, username, password,
                                              change_user='root')
    #stdout, stderr = transfer.execute_script('/tmp', 'tomcat_user_crete.sh', host, 22, username, password, change_user='root')
    #stdout, stderr = transfer.execute_script('/tmp', 'tomcat_install.sh', host, 22, username, password, change_user='tomcat')
    print 'MySQL install output %r' % stdout
    print 'MySQL install error %r' % stderr




