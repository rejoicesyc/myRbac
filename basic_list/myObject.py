from basic_list import config

class MyObject:
    def create_object(self,object):
        if object not in config.myObject:
            config.myObject.add(object)
            return True
        else:
            return False

    def delete_object(self,object):
        config.myObject.discard(object)

    def execute_object(self,object):
        if object in config.myObject:
            print(object+": executed.")
            return True
        else:
            return False

    def write_object(self,object,new_object):
        if object in config.myObject:
            config.myObject.discard(object)
            config.myObject.add(new_object)
            return True
        else:
            return False

    def read_object(self,object):
        if object in config.myObject:
            print(object+": read.")
            return True
        else:
            return False

    def ls(self):
        if len(config.myObject)!=0:
            for i in config.myObject:
                print(i,end="  ")
            print()