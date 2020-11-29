import rbac

class Bash:
    def __init__(self):
        self.rbac=rbac.Rbac()

    def run(self):
        self.rbac.init_login()

        while True:
            cmd=input("\033[1;32m"+self.rbac.present_user+"@rbac_monitor\033[0m:"+"\033[1;34m~\033[0m$ ")
            cmd=cmd.split(" ")
            cmdlen=len(cmd)
            
            if cmd[0]=="ls" and cmdlen==1:
                self.rbac.ls()
            elif cmd[0]=="su" and cmdlen==2:
                self.rbac.su(cmd[1])
            elif cmd[0]=="adduser" and cmdlen==3:
                self.rbac.add_user(cmd[1],cmd[2])
            elif cmd[0]=="addrole" and cmdlen>=3:
                self.rbac.add_role(cmd[1],cmd[2],set(cmd[3:]))
            elif cmd[0]=="addperm" and cmdlen>=2:
                self.rbac.add_perm(set(cmd[1:]))
            elif cmd[0]=="chRolePerm" and cmdlen>=4:
                self.rbac.chRolePerm(cmd[1],cmd[2],set(cmd[3:]))
            elif cmd[0]=="chUserRole" and cmdlen==3:
                self.rbac.chUserRole(cmd[1],cmd[2])
            elif cmd[0]=="roleInherit" and cmdlen==3:
                self.rbac.roleInherit(cmd[1],cmd[2])
            elif cmd[0]=="create" and cmdlen==2:
                self.rbac.create(cmd[1])
            elif cmd[0]=="read" and cmdlen==2:
                self.rbac.read(cmd[1])
            elif cmd[0]=="write" and cmdlen==3:
                self.rbac.write(cmd[1],cmd[2]) # change obj1 2 obj2
            elif cmd[0]=="execute" and cmdlen==2:
                self.rbac.execute(cmd[1])
            elif cmd[0]=="delete" and cmdlen==2:
                self.rbac.delete(cmd[1])
            elif cmd[0]=="exit" and cmdlen==1:
                exit()
            else:
                print("-bash: "+cmd[0]+": command not found or argument error.")