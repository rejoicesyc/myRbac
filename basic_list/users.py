import getpass
import hashlib
from basic_list import config

class Users:
    def get_passwd_hash(self,passwd):
        return hashlib.sha512(passwd.encode('utf-8')).hexdigest()

    def check_passwd(self,user,passwd_hash):
        if user in config.users.keys():
            return config.users[user]==passwd_hash
        else:
            return False

    def add_user(self,user,passwd_hash):
        config.users[user]=passwd_hash

    # only can be used while initializing the system
    def set_default_user(self,passwd_hash):
        config.users[config.default_user]=passwd_hash
    
    def has_user(self,user):
        return user in config.users.keys()