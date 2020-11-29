from basic_list import users
from basic_list import roles
from basic_list import permission
from basic_list import myObject
from basic_list import config
import getpass

class Rbac:
    def __init__(self):
        self.users=users.Users()
        self.roles=roles.Roles()
        self.permission=permission.Permission()
        self.object=myObject.MyObject()

        # set by login or user init set
        self.present_user=""

    def init_login(self):
        while True:
            if input("Enter user name: ")==config.default_user:
                passwd_hash=self.users.get_passwd_hash(getpass.getpass("New password: "))
                if passwd_hash==self.users.get_passwd_hash(getpass.getpass("Retype new password: ")):
                    self.users.set_default_user(passwd_hash)
                    self.present_user=config.default_user
                    break
                else:
                    print("Sorry, passwords do not match.")

    def ls(self):
        self.object.ls()

    def user_role_check(self,user,role):
        return role==config.users_roles[user]

    def role_permission_check(self,role,perm):
        return perm in config.roles_permissions[role]

    def user_permission_check(self,user,perm):
        return perm in config.roles_permissions[config.users_roles[user]]

    def user_group_check(self,user):
        return user in config.users_group[self.present_user]

    def su(self,user):
        if self.users.has_user(user):
            if self.users.check_passwd(user,self.users.get_passwd_hash(getpass.getpass("Password: "))):
                self.present_user=user
            else:
                print("su: Authentication failure")
        else:
            print("Sorry, do not match any user.")

    def add_user(self,user,role):
        if self.user_permission_check(self.present_user,config.adduser):
            if not self.users.has_user(user):
                if self.roles.has_role(role):
                    while True:
                        passwd_hash=self.users.get_passwd_hash(getpass.getpass("New password: "))
                        if passwd_hash==self.users.get_passwd_hash(getpass.getpass("Retype new password: ")):
                            print("Successfully add user",user)
                            self.users.add_user(user,passwd_hash)
                            config.users_roles[user]=role
                            config.users_group[self.present_user]=config.users_group[self.present_user]|{user}
                            config.users_group[user]=set()
                            break
                        else:
                            print("Sorry, passwords do not match.")
                else:
                    print("Sorry, do not match any role.")
            else:
                print("Sorry, user {} already exist.".format(user))
        else:
            print("adduser: permission denied.")

    def add_role(self,role,level,perm:set):
        level=int(level)
        if self.user_permission_check(self.present_user,config.addrole)\
                and self.roles.role_level(config.users_roles[self.present_user])<=level:
            if not self.roles.has_role(role):
                if perm-config.permissions!=set():
                    print("Successfully add role",role)
                    self.roles.add_role(role,level)
                    config.roles_permissions[role]=perm
                else:
                    print("Sorry, some of permissions not match.")
            else:
                print("Sorry, role already exist.")
        else:
            print("addrole: permission denied.")

    def add_perm(self,perm:set):
        if self.user_permission_check(self.present_user,config.addperm):
            print("Successfully add permission set",perm-config.permissions)
            config.permissions=config.permissions|perm
        else:
            print("addperm: permission denied.")

    def chRolePerm(self,role,operator,perm:set):
        if self.user_permission_check(self.present_user,config.chRolePerm)\
                and self.roles.compare_role(config.users_roles[self.present_user],role):
            if self.roles.has_role(role):
                if operator=="+":
                    print("Successfully add permission set",perm-config.roles_permissions[role],\
                            "for role",role)
                    config.roles_permissions[role]=config.roles_permissions[role]|perm
                elif operator=="-":
                    print("Successfully delete permission set",config.roles_permissions[role]-perm,\
                            "for role",role)
                    config.roles_permissions[role]=config.roles_permissions[role]-perm
                elif operator=="$":
                    level=int(perm[0])
                    if self.roles.role_level(config.users_roles[self.present_user])<=level:
                        self.roles.change_level(role,level)
                    else:
                        print("chRolePerm: permission denied.\nChoose lower level.")
                else:
                    print("chRolePerm: operator error.")
            else:
                print("Sorry, role already exist.")
        else:
            print("chRolePerm: permission denied.")

    def chUserRole(self,user,role):
        if self.user_permission_check(self.present_user,config.chUserRole)\
                and self.roles.compare_role(config.users_roles[self.present_user],role)\
                and self.user_group_check(user):
            if self.roles.has_role(role):
                config.users_roles[user]=role
            else:
                print("Sorry, do not match any role.")
        else:
            print("chUserRole: permission denied.")

    def roleInherit(self,role,heir):
        if self.user_permission_check(self.present_user,config.chRolePerm):
            if self.roles.has_role(role):
                if self.roles.compare_role(config.users_roles[self.present_user],role):
                    if not self.roles.has_role(heir):
                        config.roles_permissions[heir]=config.roles_permissions[role]
                        self.roles.add_role(heir,self.roles.role_level(role))
                    else:
                        print("Sorry, role {} already exist. Cannot be a heir.".format(heir))
                else:
                    print("RoleInherit: permission denied.\nChoose lower level role.")
            else:
                print("Sorry, role {} can not be inherited.".format(role))
        else:
            print("RoleInherit: permission denied.")

    def create(self,object):
        if self.user_permission_check(self.present_user,config.create):
            if not self.object.create_object(object):
                print("Create: {} already exist.".format(object))
        else:
            print("Create: permission denied.")

    def write(self,object,new_object):
        if self.user_permission_check(self.present_user,config.write):
            if not self.object.write_object(object,new_object):
                print("Create: {} does not exist.".format(object))
        else:
            print("Write: permission denied.")

    def read(self,object):
        if self.user_permission_check(self.present_user,config.read):
            if not self.object.read_object(object):
                print("Create: {} does not exist.".format(object))
        else:
            print("Read: permission denied.")

    def execute(self,object):
        if self.user_permission_check(self.present_user,config.execute):
            if not self.object.execute_object(object):
                print("Create: {} does not exist.".format(object))
        else:
            print("Execute: permission denied.")

    def delete(self,object):
        if self.user_permission_check(self.present_user,config.delete):
            self.object.delete_object(object)
        else:
            print("Delete: premission denied.")

    def check_infos(self):
        print(config.users)
        print(config.roles)
        print(config.permissions)
        print(config.myObject)
        print(config.users_roles)
        print(config.users_group)
        print(config.roles_permissions)