from fabric import group
from fabric import runners
from fabric import Connection
from fabric.exceptions import GroupException
from socket import timeout
def score_a(start_h,end_h,ssh_port=22):
    my_hosts = []
    for hosts_ip in range(start_h,end_h):
        my_hosts.append('172.20.{0}.220'.format(hosts_ip))

    hosts_score = {}
    for host_name in my_hosts:
        hosts_score[host_name] = []

    con_group = [Connection(host=host,user='root',connect_kwargs = {'password':'redhat'},connect_timeout = 10 port=ssh_port) for host in my_hosts]
    gp1 = group.ThreadingGroup.from_connections(con_group)


    #查找jerry的文件
    try:
        find1 = gp1.run('diff /etc/local/check/check_find.txt /local_tmp/find/found.txt',warn = True)
        # re2 = gp1.run('ip a', warn=True)
    except GroupException as no_conn:

        find1 = no_conn.result
    except Exception as all_exception:
            print(all_exception)
            print(type(all_exception))
    for conni,result in find1.items():
        # print("{0.host}:{1.stdout}".format(conni,result))
        if isinstance(result,runners.Result):
            if result.exited == 0:
               hosts_score[conni.host].append(4)
            else:
                hosts_score[conni.host].append(0)
        else:
            hosts_score[conni.host].append(0)
            print('can not connect to {0.host} ,{1}'.format(conni,result))

        print('{0.host} 的得分 {1}'.format(conni,hosts_score[conni.host]))
        print('##################')
    #校验将找到的文件是否被复制出来
    try:
        find2 = gp1.run('ls /local_tmp/find/file_49.txt',warn = True)
        # re2 = gp1.run('ip a', warn=True)
    except GroupException as no_conn:

        find2 = no_conn.result
    except Exception as all_exception:
            print(all_exception)
            print(type(all_exception))
    for conni,result in find2.items():
        # print("{0.host}:{1.stdout}".format(conni,result))
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


    #tar命令压缩/local_tmp/find文件夹

    try:
        tar1 = gp1.run('file /root/jerry_tmp.tar.xz',warn = True)
        # re2 = gp1.run('ip a', warn=True)
    except GroupException as no_conn:

        tar1 = no_conn.result
    except Exception as all_exception:
            print(all_exception)
            print(type(all_exception))
    for conni,result in tar1.items():
        # print("{0.host}:{1.stdout}".format(conni,result))
        if isinstance(result,runners.Result):
            if 'XZ' in str(result):
               hosts_score[conni.host].append(4)
            else:
                hosts_score[conni.host].append(0)
        else:
            hosts_score[conni.host].append(0)
            print('can not connect to {0.host} ,{1}'.format(conni,result))

        print('{0.host} get score {1}'.format(conni,hosts_score[conni.host]))
        print('##################')

    #用户管理1.1 验证redhat用户组
    try:
        user1 = gp1.run('getent group redhat',warn = True)
        # re2 = gp1.run('ip a', warn=True)
    except GroupException as no_conn:

        user1 = no_conn.result
    except Exception as all_exception:
            print(all_exception)
            print(type(all_exception))
    for conni,result in user1.items():
        # print("{0.host}:{1.stdout}".format(conni,result))
        if isinstance(result,runners.Result):
            if '5000' in str(result):
               hosts_score[conni.host].append(1)
            else:
                hosts_score[conni.host].append(0)
        else:
            hosts_score[conni.host].append(0)
            print('can not connect to {0.host} ,{1}'.format(conni,result))

        print('{0.host} get score {1}'.format(conni,hosts_score[conni.host]))
        print('##################')

    #用户管理：1.2 验证wingcloud用户组
    try:
        user2 = gp1.run('getent group wingcloud',warn = True)
        # re2 = gp1.run('ip a', warn=True)
    except GroupException as no_conn:

        user2 = no_conn.result
    except Exception as all_exception:
            print(all_exception)
            print(type(all_exception))
    for conni,result in user2.items():
        # print("{0.host}:{1.stdout}".format(conni,result))
        if isinstance(result,runners.Result):
            if '6000' in str(result):
               hosts_score[conni.host].append(1)
            else:
                hosts_score[conni.host].append(0)
        else:
            hosts_score[conni.host].append(0)
            print('can not connect to {0.host} ,{1}'.format(conni,result))

        print('{0.host} get score {1}'.format(conni,hosts_score[conni.host]))
        print('##################')

    #用户管理1.3 验证用户marry
    try:
        user3 = gp1.run('id marry',warn = True)
        # re2 = gp1.run('ip a', warn=True)
    except GroupException as no_conn:

        user3 = no_conn.result
    except Exception as all_exception:
            print(all_exception)
            print(type(all_exception))
    for conni,result in user3.items():
        # print("{0.host}:{1.stdout}".format(conni,result))
        if isinstance(result,runners.Result):
            if ('3000' in str(result) )& ('7000' in str(result)):
               hosts_score[conni.host].append(1)
            else:
                hosts_score[conni.host].append(0)
        else:
            hosts_score[conni.host].append(0)
            print('can not connect to {0.host} ,{1}'.format(conni,result))

        print('{0.host} get score {1}'.format(conni,hosts_score[conni.host]))
        print('##################')

    #用户管理2：验证用户jim不可登陆
    try:
        user4 = gp1.run('cat /etc/passwd |grep jim',warn = True)
        # re2 = gp1.run('ip a', warn=True)
    except GroupException as no_conn:

        user4 = no_conn.result
    except Exception as all_exception:
            print(all_exception)
            print(type(all_exception))
    for conni,result in user4.items():
        if isinstance(result,runners.Result):
            if 'nologin' in str(result):
               hosts_score[conni.host].append(3)
            else:
                hosts_score[conni.host].append(0)
        else:
            hosts_score[conni.host].append(0)
            print('can not connect to {0.host} ,{1}'.format(conni,result))

        print('{0.host} get score {1}'.format(conni,hosts_score[conni.host]))
        print('##################')


    #用户管理3 把wingcloud和redhat作为marry的附属组
    try:
        user4 = gp1.run('cat /etc/passwd |grep marry',warn = True)
        # re2 = gp1.run('ip a', warn=True)
    except GroupException as no_conn:

        user4 = no_conn.result
    except Exception as all_exception:
            print(all_exception)
            print(type(all_exception))
    for conni,result in user4.items():
        if isinstance(result,runners.Result):
            if ('5000(redhat)' in str(result)) & ('6000(wingcloud)' in str(result)):
               hosts_score[conni.host].append(3)
            else:
                hosts_score[conni.host].append(0)
        else:
            hosts_score[conni.host].append(0)
            print('can not connect to {0.host} ,{1}'.format(conni,result))

        print('{0.host} get score {1}'.format(conni,hosts_score[conni.host]))
        print('##################')


    #检验/student目录的o+t权限和umask值
    try:
        user5_1 = gp1.run('ls -ld /student',warn = True)
        # re2 = gp1.run('ip a', warn=True)
    except GroupException as no_conn:

        user5_1 = no_conn.result
    except Exception as all_exception:
            print(all_exception)
            print(type(all_exception))
    for conni,result in user5_1.items():
        if isinstance(result,runners.Result):
            if 'rwt' in str(result):
               hosts_score[conni.host].append(6)
               print('This is {0.host}'.format(conni))
            else:
                hosts_score[conni.host].append(0)
        else:
            hosts_score[conni.host].append(0)
            print('can not connect to {0.host} ,{1}'.format(conni,result))

        print('{0.host} get score {1}'.format(conni,hosts_score[conni.host]))
        print('##################')


    # try:
    #     user5_2 = gp1.run('su - jerry -c umask',warn = True)
    #     # re2 = gp1.run('ip a', warn=True)
    # except GroupException as no_conn:
    #
    #     user5_2 = no_conn.result
    # except Exception as all_exception:
    #         print(all_exception)
    #         print(type(all_exception))
    # for conni,result in user5_2.items():
    #     if isinstance(result,runners.Result):
    #         if '022' in str(result):
    #            hosts_score[conni.host].append(3)
    #         else:
    #             hosts_score[conni.host].append(0)
    #     else:
    #         hosts_score[conni.host].append(0)
    #         print('can not connect to {0.host} ,{1}'.format(conni,result))
    #
    #     print('{0.host} get score {1}'.format(conni,hosts_score[conni.host]))
    #     print('##################')


    #计划任务
    try:
        sys1 = gp1.run('crontab -l |grep -E "13\s+1\s+.\*\s+.\*\s+6\s+tar\s+*c*" ',warn = True)
        #匹配13 1 * * 6 tar c
        # re2 = gp1.run('ip a', warn=True)
    except GroupException as no_conn:

        sys1 = no_conn.result
    except Exception as all_exception:
            print(all_exception)
            print(type(all_exception))
    for conni,result in sys1.items():
        if isinstance(result,runners.Result):
            if result.exited == 0:
               hosts_score[conni.host].append(7)
            else:
                hosts_score[conni.host].append(0)
        else:
            hosts_score[conni.host].append(0)
            print('can not connect to {0.host} ,{1}'.format(conni,result))

        print('{0.host} get score {1}'.format(conni,hosts_score[conni.host]))
        print('##################')

    #验证软件仓库
    try:
        sys2 = gp1.run('yum clean all && yum reinstall rsyslog -y',warn = True)
        # re2 = gp1.run('ip a', warn=True)
    except GroupException as no_conn:

        sys2 = no_conn.result
    except Exception as all_exception:
            print(all_exception)
            print(type(all_exception))
    for conni,result in sys2.items():
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

    #验证安装包含iostat的软件包
    try:
        sys3 = gp1.run('iostat',warn = True)
        # re2 = gp1.run('ip a', warn=True)
    except GroupException as no_conn:

        sys3 = no_conn.result
    except Exception as all_exception:
            print(all_exception)
            print(type(all_exception))
    for conni,result in sys3.items():
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



    #验证字符串替换 172.20.3.254 替换为192.168.20.254
    try:
        sys4 = gp1.run('diff /root/kickstart.txt /etc/local/check/kickstart.txt',warn = True)
        # re2 = gp1.run('ip a', warn=True)
    except GroupException as no_conn:

        sys4 = no_conn.result
    except Exception as all_exception:
            print(all_exception)
            print(type(all_exception))
    for conni,result in sys4.items():
        if isinstance(result,runners.Result):
            if result.exited == 0:
               hosts_score[conni.host].append(5)
            else:
                hosts_score[conni.host].append(0)
        else:
            hosts_score[conni.host].append(0)
            print('can not connect to {0.host} ,{1}'.format(conni,result))

        print('{0.host} get score {1}'.format(conni,hosts_score[conni.host]))
        print('##################')

    #final_score
    vm_score = {}
    for hostname,fin_score in hosts_score.items():
        sum_score = sum(fin_score)
        print('{0} get {1},final score is {2}'.format(hostname,fin_score,sum_score))
        #print('2nd score is {0}'.format(fin_score[2]))
        vm_score[hostname] = [sum_score]
    return vm_score
