import re
import getopt
import sys

def getArgvs(argv):
    result = {"machineid": "", "bootid": "", "cgroup": ""}
    try:
        opts, args = getopt.getopt(argv, "hu:p:a:m:b:c:",
                                   ["help", "username=", "path=", "address=", "machineid", "bootid", "cgroup"])
    except getopt.GetoptError:
        print('flaskpin.py -h')
        sys.exit(2)
    # print(opts)

    if len(opts) == 0:
        sys.exit("flaskpin.py -h")

    # 处理 返回值options是以元组为元素的列表。
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("*" * 60 + "参数解释" + "*" * 60)
            print("username:用户名(/etc/passwd)\npath:flask下app.py的绝对路径(页面报错得到,moddir别名)\naddress:网卡地址("
                  "/sys/class/net/eth0/address,16进制或10进制均可)\nmachineid:(/etc/machine-id，没有则不填)\nbootid("
                  "/proc/sys/kernel/random/boot_id，没有则不填)\ncgroup(/proc/self/cgroup,没有则不填,支持输入本地cgroup文件路径自动解析字符串)")
            print("*" * 60 + "用法" + "*" * 60)
            print('python flaskpin.py -u <username> -p <path> -a <address> -m <machineid> -b <bootid> -c <cgroup>')
            print('python flaskpin.py --username=<username> --path=<path> --address=<address> '
                  '--machineid=<machineid> --bootid=<bootid> --cgroup=<cgroup>')
            sys.exit()
        elif opt in ("-u", "--username"):
            username = arg
            result["username"] = username
        elif opt in ("-p", "--path"):
            path = arg
            result["path"] = path
        elif opt in ("-a", "--address"):
            address = arg
            result["address"] = address
        elif opt in ("-m", "--machineid"):
            machineid = arg
            result["machineid"] = machineid
        elif opt in ("-b", "--bootid"):
            bootid = arg
            result["bootid"] = bootid
        elif opt in ("-c", "--cgroup"):
            cgroup = arg
            result["cgroup"] = cgroup
    return result

def compare(version1, version2):
    # 版本号转换为list，使用str是为了兼容版本里带字母的情况
    version2 = re.search("\d.\d+", version2).group()
    v1 = [float(x) for x in str(version1).split('.')]
    v2 = [float(x) for x in str(version2).split('.')]

    # # 对2个list进行排序，小的排在前面
    list_sort = [v1, v2]
    # 对排序后的list判断大小
    if list_sort[0][0] > list_sort[1][0]:
        return False
    elif list_sort[0][0] < list_sort[1][0]:
        return True
    else:
        if list_sort[0][1] > list_sort[1][1]:
            return False
        else:
            return True


if __name__ == "__main__":
    print(compare("3.6", "/usr/local/lib/python4.0/site-packages/flask/app.py"))
