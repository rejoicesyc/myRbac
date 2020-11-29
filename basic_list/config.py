# global definitions

# user definition
default_user="root"

# role definition
SuperAdmin="SuperAdmin"
Admin="Admin"
user="user"

# permission definition
execute="execute"
write="write"
read="read"
delete="delete"
create="create"
adduser="adduser"
addrole="addrole"
addperm="addperm"
chRolePerm="chRolePerm"
chUserRole="chUserRole"

# infos
users={default_user:""}
roles={SuperAdmin:0,Admin:3,user:5}
permissions={execute,write,read,delete,create,adduser,addrole,addperm} # predefined
myObject=set()

# relationship list
users_roles={default_user:SuperAdmin}
users_group={default_user:set()}
roles_permissions={SuperAdmin:{execute,write,read,delete,create,adduser,addrole,addperm,chRolePerm,chUserRole},Admin:set(),user:set()}