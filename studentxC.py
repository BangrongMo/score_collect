from fabric import group
from fabric import Connection
from fabric import runners
from shell import shell
from fabric.exceptions import GroupException
def score_c():
    my_hosts = []
    for hosts_ip in range(122,123):
        my_hosts.append('172.20.{0}.222'.format(hosts_ip))
    # print(my_hosts)
    hosts_score = {}
    for host_name in my_hosts:
        hosts_score[host_name] = []

    # print(hosts_score)
    # print(my_hosts)
    con_group = [Connection(host=host,user='root',connect_kwargs = {'password':'redhat1234'},connect_timeout = 1) for host in my_hosts]
    gp1 = group.ThreadingGroup.from_connections(con_group)

    #第一题：用redhat1234作为密码登陆，检测密码重置情况
    try:
        pwd1 = gp1.run('id',warn = True)
        # re2 = gp1.run('ip a', warn=True)
    except GroupException as no_conn:

        pwd1 = no_conn.result
    except Exception as all_exception:
            print(all_exception)
            print(type(all_exception))
    for conni,result in pwd1.items():
        if isinstance(result,runners.Result):
            if result.exited == 0:
               hosts_score[conni.host].append(4)
            else:
                hosts_score[conni.host].append(0)
        else:
            hosts_score[conni.host].append(0)
            print('can not connect to {0.host} ,{1}'.format(conni,result))

        print('{0.host} get score {1}'.format(conni,hosts_score[conni.host]))
        print('##################')

    #第二题：第一步检测DNS设置
    try:
        dns1 = gp1.run('cat /etc/resolve.conf |grep 114.114.114.114',warn = True)
        # re2 = gp1.run('ip a', warn=True)
    except GroupException as no_conn:

        dns1 = no_conn.result
    except Exception as all_exception:
            print(all_exception)
            print(type(all_exception))
    for conni,result in dns1.items():
        if isinstance(result,runners.Result):
            if result.exited == 0:
               hosts_score[conni.host].append(1)
            else:
                hosts_score[conni.host].append(0)
        else:
            hosts_score[conni.host].append(0)
            print('can not connect to {0.host} ,{1}'.format(conni,result))

        print('{0.host} get score {1}'.format(conni,hosts_score[conni.host]))
        print('##################')


    #第二题第二部：检测网关配置
    try:
        gw1 = gp1.run('ip route |grep default|grep 254',warn = True)
        #dns1 = gp1.run('ping 192.168.233.100 -c4',warn = True)

    except GroupException as no_conn:

        gw1 = no_conn.result
    except Exception as all_exception:
            print(all_exception)
            print(type(all_exception))
    for conni,result in gw1.items():
        if isinstance(result,runners.Result):
            if result.exited == 0:
               hosts_score[conni.host].append(1)
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