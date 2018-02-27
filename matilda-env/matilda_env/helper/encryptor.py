from cryptography.fernet import Fernet

key = 'Hp9Pf7d_XP2gnruFn3wbaZdTJTxZUSxKa4jqv6DKns4='
print 'Key %r' % key
cipher_suite = Fernet(key)

def encrypt(content):
    return cipher_suite.encrypt(b"%s" % content)

def decrypt(encoded_text):
    return cipher_suite.decrypt(encoded_text)