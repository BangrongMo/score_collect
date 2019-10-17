from fabric import group
from fabric import Connection
from fabric import runners
from shell import shell
from fabric.exceptions import GroupException
def score_b():
    my_hosts = []
    for hosts_ip in range(122,123):
        my_hosts.append('172.20.{0}.221'.format(hosts_ip))
    # print(my_hosts)
    hosts_score = {}
    for host_name in my_hosts:
        hosts_score[host_name] = []

    # print(hosts_score)
    # print(my_hosts)
    con_group = [Connection(host=host,user='root',connect_kwargs = {'password':'redhat'},connect_timeout = 1) for host in my_hosts]
    gp1 = group.ThreadingGroup.from_connections(con_group)

    #执行前重启vmB

    #第一题：验证http服务启动状态
    try:
        for hostsB,hostsB_list in hosts_score.items():
            httpd1 = shell('curl {0} -m 10'.format(hostsB))
            # print(re2.output())
            print(hostsB,httpd1.output())

            if httpd1.output() == ['ok']:
                hosts_score[hostsB].append(5)
            else :
                hosts_score[hostsB].append(0)

    except Exception as all_exception:
            print(all_exception)
            print(type(all_exception))

    #第二题 第一步：验证2200端口
    try:
        ssh1 = gp1.run('id',warn = True)
    except GroupException as no_conn:

        ssh1 = no_conn.result

    except Exception as all_exception:
            print(all_exception)
            print(type(all_exception))

    for conni,result in ssh1.items():
        # print("{0.host}:{1.stdout}".format(conni,result))
        if isinstance(result,runners.Result):
            if result.exited == 0:
               hosts_score[conni.host].append(2)

        else:
            hosts_score[conni.host].append(0)
            print('can not connect to {0.host} ,{1}'.format(conni,result))
        print('{0.host} get score {1}'.format(conni,hosts_score[conni.host]))
        print('##################')


    #第二题第二步验证 firewwall rich
    try:
        firewall1 = gp1.run('firewall-cmd --list-all |grep 172.20.',warn = True)
    except GroupException as no_conn:

        firewall1 = no_conn.result

    except Exception as all_exception:
            print(all_exception)
            print(type(all_exception))

    for conni,result in firewall1.items():
        # print("{0.host}:{1.stdout}".format(conni,result))
        if isinstance(result,runners.Result):
            if 'accept' in str(result):
               hosts_score[conni.host].append(2)
            else:
                hosts_score[conni.host].append(0)

        else:
            hosts_score[conni.host].append(0)

            print('can not connect to {0.host} ,{1}'.format(conni,result))
        print('{0.host} get score {1}'.format(conni,hosts_score[conni.host]))
        print('##################')

    #第二题第三步：验证管理员登陆
    try:
        ssh2 = gp1.run('sudo cat /etc/ssh/sshd_config |grep PermitRootLogin|grep -v \#' ,warn = True)
    except GroupException as no_conn:

        ssh2 = no_conn.result

    except Exception as all_exception:
            print(all_exception)
            print(type(all_exception))

    for conni,result in ssh2.items():
        # print("{0.host}:{1.stdout}".format(conni,result))
        if isinstance(result,runners.Result):
            if 'no' in str(result):
               hosts_score[conni.host].append(1)

        else:
            hosts_score[conni.host].append(0)
            print('can not connect to {0.host} ,{1}'.format(conni,result))
        print('{0.host} get score {1}'.format(conni,hosts_score[conni.host]))
        print('##################')

    #检测print.sh脚本可执行性
    try:
        x_per = gp1.run('sudo /usr/local/bin/print.sh' ,warn = True)
    except GroupException as no_conn:

        x_per = no_conn.result

    except Exception as all_exception:
            print(all_exception)
            print(type(all_exception))

    for conni,result in x_per.items():
        # print("{0.host}:{1.stdout}".format(conni,result))
        if isinstance(result,runners.Result):
            if 'sbin' in str(result):
               hosts_score[conni.host].append(3)
            else:
               hosts_score[conni.host].append(0)

        else:
            hosts_score[conni.host].append(0)
            print('can not connect to {0.host} ,{1}'.format(conni,result))
        print('{0.host} get score {1}'.format(conni,hosts_score[conni.host]))
        print('##################')
    #检测脚本中是否含有#!/bin/bash
    try:
        bin_bash = gp1.run('sudo cat /usr/local/bin/print.sh' ,warn = True)
    except GroupException as no_conn:

        bin_bash = no_conn.result

    except Exception as all_exception:
            print(all_exception)
            print(type(all_exception))

    for conni,result in bin_bash.items():
        # print("{0.host}:{1.stdout}".format(conni,result))
        if isinstance(result,runners.Result):
            if '''#!/bin/bash''' in str(result):
               hosts_score[conni.host].append(2)
            else:
               hosts_score[conni.host].append(0)

        else:
            hosts_score[conni.host].append(0)
            print('can not connect to {0.host} ,{1}'.format(conni,result))
        print('{0.host} get score {1}'.format(conni,hosts_score[conni.host]))
        print('##################')

    #final_score
    for hostname,fin_score in hosts_score.items():
        sum_score = sum(fin_score)
        print('{0} get {1},final score is {2}'.format(hostname,fin_score,sum_score))
        #print('2nd score is {0}'.format(fin_score[2]))
        vm_score = {}
        vm_score[hostname] = [sum_score]
    return vm_score