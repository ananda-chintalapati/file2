from matilda_env.helper import encryptor

def test_encryptor():
    text = '64DK2*5u7H34UxN'
    enc_str = encryptor.encrypt(text)
    dec_str = encryptor.decrypt(enc_str)

    print '%s == %s' % (dec_str, enc_str)

def test_decrypt():
    text = 'gAAAAABalc-5YVJJc-wO6xfPfwPimU4ON-pM3Nz9rUdDB9VSi9MT--Mz5BjL4Gi3oqHxV4kpQrS_7tRm3XrdoB3G_d8F1m_6Hg=='
    print encryptor.decrypt(text)

test_encryptor()