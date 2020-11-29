from basic_list import config

class Roles:
    def has_role(self,role):
        return role in config.roles.keys()

    def add_role(self,role,level):
        if not self.has_role(role):
            config.roles[role]=level
            return True
        else:
            return False

    def delete_role(self,role):
        config.roles.pop(role)

    def compare_role(self,role1,role2):
        return config.roles[role1]<=config.roles[role2]

    def role_level(self,role):
        return config.roles[role]

    def change_level(self,role,level):
        config.roles[role]=level
        