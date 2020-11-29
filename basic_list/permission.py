from basic_list import config

class Permission:
    def add_perm(self,perm):
        config.permissions.add(perm)

    def delete_perm(self,perm):
        config.permissions.discard(perm)