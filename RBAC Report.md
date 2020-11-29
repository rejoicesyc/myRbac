# RBAC Report



#### 1. RBAC的设计

如图是rbac的整体设计，一共涉及5张表格：用户表、角色表、权限表、用户角色对应表、角色权限对应表。这5张表用于存储rbac内部的数据，从而实现不同关系之间的协同和约束。

<img src="C:\Users\大菠萝\AppData\Roaming\Typora\typora-user-images\image-20201129005152823.png" alt="image-20201129005152823" />

* **用户表**

用于存储每个用户的用户名和登录密码的hash值，确保每个用户只能被拥有密码的主体登录，基于用户登录是所有操作的前提，实际上本rbac系统安全的前提是用户账号的安全。

* **角色表**

角色表用于存储不同的角色名称，以及不同角色对应的等级，根据等级不同角色的部分权限有高低之分，在本系统中体现在：

1. 用户只能创建和修改不高于自己等级的角色
2. 用户只能将不高于自己等级的角色赋给其他用户
3. 用户只能修改不高于自己等级的角色所对应的权限
4. 用户在创建继承角色时的等级不能高于自己

* **权限表**

权限表规定了本系统中除等级限制以外的操作限制权限，本系统中预设的有10种权限。

1. 执行权限：代表执行一个对象
2. 写权限：代表修改一个对象
3. 读权限：代表读取一个对象信息
4. 删除权限：代表删除一个对象
5. 创建权限：代表创建一个新的对象
6. 添加用户权限：代表创建新用户，并记录其密码的hash值
7. 添加角色权限：代表创建新角色，并添加其对应的等级值
8. 添加权限表权限：代表增加权限表目录
9. 修改用户对应角色权限：代表用户可以将一个角色和一个用户关联起来
10. 修改角色对应权限的权限：代表用户可以修改一个角色对应的权限

* **用户角色对应表**

用户角色对应表记录了每一个用户对应的角色信息，通过该表可以查到某个用户的角色等级以及该角色对应的权限信息，该表只能由拥有上述权限9（修改用户对应角色权限）的用户修改。

* **角色权限对应表**

角色权限对应表记录了每个角色拥有的权限信息，通过该表可以知道某个角色是否有执行某操作的权限，进而限制角色对应用户的行为。该表只能由拥有上述权限10（修改角色对应权限的权限）的用户修改。



#### 2. RBAC的实现

RBAC系统的实现结构图如下，一共分为6个部分：

![image-20201129103742656](C:\Users\大菠萝\AppData\Roaming\Typora\typora-user-images\image-20201129103742656.png)

* **User类**

User类提供的是对用户表的操作，主要功能有增加用户，检查密码，设置初始用户，注意该类不对权限进行检查，同时整个系统中只有该类可以操作用户表。

* **Role类**

Role类主要提供了增加角色，比较和检查用户等级的功能，实际上就是对角色表进行修改的功能。

* **Permission类**

该类主要提供对权限表进行修改的功能。

* **MyObject类**

MyObject类记录了系统中可被操作的对象，相当于简易的文件系统，用户可以通过上层api调用实现对象的各种操作。

* **Rbac类**

Rbac类是访问控制实现的主体，该类提供了切换用户，检查用户权限，添加用户、角色和权限，修改角色对应权限，修改用户对应权限以及角色继承，以及读、写、执行等功能。该类在实现各种操作前进行访问控制，主要的控制实现为：

1. 当用户进行切换时通过密码控制访问
2. 当用户添加用户、角色、权限时对用户拥有的角色进行检查，确保用户拥有访问这些数据的权限，同时控制用户不能创建比自己等级低的角色。
3. 当用户修改角色对应权限时，检查用户是否具有修改的权力以及用户是否在修改比自己级别高的角色的权限
4. 当用户修改用户对应的角色时，检查用户是否在修改比自己级别高的用户的角色，以及是否将高于自己级别的角色赋给了其他人
5. 当用户继承角色时，检查被继承角色的级别是否高于操作主体的权限
6. 当用户进行读、写、执行等操作时检查操作主体是否拥有对应的权限

* **Bash类**

通过命令行的方式让用户可以使用Rbac类提供的功能。



#### 3. 结论

**主要功能的展示**

* 通过系统预设用户名``root``第一次登入系统，并设置用户密码：

<img src="C:\Users\大菠萝\AppData\Roaming\Typora\typora-user-images\image-20201129105147689.png" alt="image-20201129105147689" style="zoom: 80%;" />

* 创建和删除名为``obj``的文件：

<img src="C:\Users\大菠萝\AppData\Roaming\Typora\typora-user-images\image-20201129105330548.png" alt="image-20201129105330548" style="zoom:80%;" />

* 添加一个名为``syc``的用户，并切换到该用户：

<img src="C:\Users\大菠萝\AppData\Roaming\Typora\typora-user-images\image-20201129105551524.png" alt="image-20201129105551524" style="zoom:80%;" />

* 尝试操作文件``obj``，因为``syc``此时没有任何权限，所以操作被拒绝：

<img src="C:\Users\大菠萝\AppData\Roaming\Typora\typora-user-images\image-20201129105801542.png" alt="image-20201129105801542" style="zoom:80%;" />

* 我们切换回``root``为``syc``添加读操作的权限，重新回到该用户发现读取成功：

  <img src="C:\Users\大菠萝\AppData\Roaming\Typora\typora-user-images\image-20201129110040560.png" alt="image-20201129110040560" style="zoom:80%;" />

* 我们通过继承创建一个新角色``HAdmin``，让他继承``Admin``的权限，并且将``syc``的角色切换为``HAdmin``，再切换到``syc``此时可以执行``obj``文件：

<img src="C:\Users\大菠萝\AppData\Roaming\Typora\typora-user-images\image-20201129111357903.png" alt="image-20201129111357903" style="zoom:80%;" />

* 用户``syc``试图将自己的权限修改为SuperAdmin被拒绝（用户不能将对象修改为比自己等级高的角色），用户试图让自己的角色继承SuperAdmin的权限被拒绝（用户不能让对象继承比自己等级高的角色的权限），用户试图修改自己角色的权限被拒绝（用户``syc``没有修改用户对应权限操作的权限）：

<img src="C:\Users\大菠萝\AppData\Roaming\Typora\typora-user-images\image-20201129111602823.png" alt="image-20201129111602823" style="zoom:80%;" />



**安全性分析**

1. 因为权限修改的权限是由拥有该权限的高等级用户分配给拥有低等级角色的用户的，所以分配该权限的动作需要十分谨慎，因为本系统中所有权限的等级都是一样的，一个低等级的用户可以通过被分配该权限就具有高等级用户才有的其他权限，从而绕过等级限制给自己或别人分配其他权限。
2. 本Rbac类没有提供删除用户、角色、权限的操作，这是出于防止用户误删系统预设信息（10个权限，3个角色，1个初始账号）和实现简便的考虑，误删这些信息可能导致系统崩溃。