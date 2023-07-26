# getFlaskPIN
`getFlaskPIN`是一款烂大街的算`Flask PIN`脚本。
#### 不同之处
1. 程序支持对于`username`以及`moddir(程序中定义为path)`的爆破，用户可自行前往`https://github.com/yuebusao/getFlaskPIN/blob/master/flaskpin.py#L88` 针对这两个参数进行修改。
2. 用户可输入`machine_id,boot_id,cgroup`，程序自行计算机器码。其中`cgroup`可输入文件路径，程序会自动读取。
3. 网卡地址参数`address(uuid)`支持输入`mac`地址或者`mac`地址转换为`10`进制之后的结果。
4. `werkzeug 2.0`之后的加密方式方式为`sha1`，`python3.6`之后安装`flask`默认安装`werkzeug>=2.0`，并且`python2`的`moddir`是`app.pyc`而不是`app.py`。基于以上几点考虑，本程序根据`path(moddir)`对`python`版本进行自识别。
#### 局限
`werkzeug 0.16.0(2019-9-19)`及以前版本计算`machine_id`的方式有所不同，脚本并没有处理这种情况。

因为经过测试发现在`python2.7`安装`flask`版本为`1.14`，依赖的`werkzeug`为`1.0.1`，现在很难见到`0.16`以下版本的`werkzeug`。并且`werkzeug`的版本取决于`flask`版本。
#### 安装
`git clone https://github.com/yuebusao/getFlaskPIN.git`

`getFlaskPIN`工作在`python 3`，无需安装任何依赖。
#### 用法
支持长短参数输入。
```commandline
python flaskpin.py -h          //查看帮助
python flaskpin.py -u <username> -p <path> -a <address> -m <machineid> -b <bootid> -c <cgroup>
python flaskpin.py --username=<username> --path=<path> --address=<address> --machineid=<machineid> --bootid=<bootid> --cgroup=<cgroup>
```
#### 参数解释
1. `username`:用户名(`/etc/passwd`)
2. `path`:`flask`下`app.py`的绝对路径(页面报错得到,`moddir`别名)
3. `address`:网卡地址(`/sys/class/net/eth0/address`,16进制或10进制均可)
4. `machineid`:(`/etc/machine-id`，没有则不填)
5. `bootid`(`/proc/sys/kernel/random/boot_id`，没有则不填)
6. `cgroup`(`/proc/self/cgroup`,没有则不填,支持输入本地`cgroup`文件路径自动解析字符串)
