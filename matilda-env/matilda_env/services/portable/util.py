from os.path import expanduser

def get_home_directory():
    home = expanduser("~")
    return home