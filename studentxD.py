from fabric import group
from fabric import Connection
from fabric import runners
from shell import shell
from fabric.exceptions import GroupException
def score_d(start_h,end_h,port=ssh_port):
    my_hosts = []
    for hosts_ip in range(start_h,end_h):
        my_hosts.append('172.20.{0}.223'.format(hosts_ip))
    # print(my_hosts)
    hosts_score = {}
    for host_name in my_hosts:
        hosts_score[host_name] = []

    # print(hosts_score)
    # print(my_hosts)
    con_group = [Connection(host=host,user='root',connect_kwargs = {'password':'redhat'},connect_timeout = 10,port=ssh_port) for host in my_hosts]
    gp1 = group.ThreadingGroup.from_connections(con_group)

    #检测sdb1文件系统
    try:
        vdb1 = gp1.run('blkid |grep sdb1',warn = True)
        # re2 = gp1.run('ip a', warn=True)
    except GroupException as no_conn:

        vdb1 = no_conn.result
    except Exception as all_exception:
            print(all_exception)
            print(type(all_exception))
    for conni,result in vdb1.items():
        if isinstance(result,runners.Result):
            if 'xfs' in str(result):
               hosts_score[conni.host].append(2)
            else:
                hosts_score[conni.host].append(0)
        else:
            hosts_score[conni.host].append(0)
            print('can not connect to {0.host} ,{1}'.format(conni,result))

        print('{0.host} get score {1}'.format(conni,hosts_score[conni.host]))
        print('##################')

    #判断sdb1 容量
    try:
        xfs1 = gp1.run(''' lsblk -b |grep sdb1 | awk '{ print $4 }' ''',warn = True)
        # re2 = gp1.run('ip a', warn=True)
    except GroupException as no_conn:

        xfs1 = no_conn.result
    except Exception as all_exception:
            print(all_exception)
            print(type(all_exception))
    for conni,result in xfs1.items():
        if isinstance(result,runners.Result):
            try:
                result_int = int(str(result))
            except Exception:
                result_int = 0
            if  (result_int < 5568709120) & (result_int > 4568709120) :
               hosts_score[conni.host].append(2)
            else:
                hosts_score[conni.host].append(0)
        else:
            hosts_score[conni.host].append(0)
            print('can not connect to {0.host} ,{1}'.format(conni,result))

        print('{0.host} get score {1}'.format(conni,hosts_score[conni.host]))
        print('##################')

    #check auto_mount
    try:
        mnt2 = gp1.run('df -h|grep sdb1',warn = True)
        # re2 = gp1.run('ip a', warn=True)
    except GroupException as no_conn:

        mnt2 = no_conn.result
    except Exception as all_exception:
            print(all_exception)
            print(type(all_exception))
    for conni,result in mnt2.items():
        if isinstance(result,runners.Result):
            if '''/mnt/sdb1''' in str(result):
               hosts_score[conni.host].append(1)
            else:
                hosts_score[conni.host].append(0)
        else:
            hosts_score[conni.host].append(0)
            print('can not connect to {0.host} ,{1}'.format(conni,result))

        print('{0.host} get score {1}'.format(conni,hosts_score[conni.host]))
        print('##################')

    #check filesystem swap
    try:
        swap1 = gp1.run('blkid |grep sdb2',warn = True)
        # re2 = gp1.run('ip a', warn=True)
    except GroupException as no_conn:

        swap1 = no_conn.result
    except Exception as all_exception:
            print(all_exception)
            print(type(all_exception))
    for conni,result in swap1.items():
        if isinstance(result,runners.Result):
            if 'swap' in str(result):
               hosts_score[conni.host].append(2)
            else:
                hosts_score[conni.host].append(0)
        else:
            hosts_score[conni.host].append(0)
            print('can not connect to {0.host} ,{1}'.format(conni,result))

        print('{0.host} get score {1}'.format(conni,hosts_score[conni.host]))
        print('##################')

    #check swap_auto mount
    try:
        mnt1 = gp1.run(''' swapon -s |grep sdb2 | awk '{ print $4 }' ''',warn = True)
        # re2 = gp1.run('ip a', warn=True)
    except GroupException as no_conn:

        mnt1 = no_conn.result
    except Exception as all_exception:
            print(all_exception)
            print(type(all_exception))
    for conni,result in mnt1.items():
        if isinstance(result,runners.Result):
            try:
                result_int = int(str(result))
            except Exception:
                result_int = 0
            if (result_int < 2568709120) & (result_int > 1568709120):
               hosts_score[conni.host].append(3)
            else:
                hosts_score[conni.host].append(0)
        else:
            hosts_score[conni.host].append(0)
            print('can not connect to {0.host} ,{1}'.format(conni,result))

        print('{0.host} get score {1}'.format(conni,hosts_score[conni.host]))
        print('##################')



    ### check lvm

    #check size 22G
    try:
        lvm1 = gp1.run(''' lsblk -b |grep lv_redhat | awk '{ print $4 }' ''',warn = True)
        # re2 = gp1.run('ip a', warn=True)
    except GroupException as no_conn:

        lvm1 = no_conn.result
    except Exception as all_exception:
            print(all_exception)
            print(type(all_exception))
    for conni,result in lvm1.items():
        if isinstance(result,runners.Result):
            try:
                result_int = int(str(result))
            except Exception:
                result_int = 0
            if (result_int < 25622320128) & (result_int > 20622320128):
               hosts_score[conni.host].append(4)
            else:
                hosts_score[conni.host].append(0)
        else:
            hosts_score[conni.host].append(0)
            print('can not connect to {0.host} ,{1}'.format(conni,result))

        print('{0.host} get score {1}'.format(conni,hosts_score[conni.host]))
        print('##################')


    #check ext4
    try:
        ext4 = gp1.run('blkid|grep lv_redhat',warn = True)
        #
        # re2 = gp1.run('ip a', warn=True)
    except GroupException as no_conn:

        ext4 = no_conn.result
    except Exception as all_exception:
            print(all_exception)
            print(type(all_exception))
    for conni,result in ext4.items():
        if isinstance(result,runners.Result):
            if 'ext4' in str(result):
               hosts_score[conni.host].append(2)
            else:
                hosts_score[conni.host].append(0)
        else:
            hosts_score[conni.host].append(0)
            print('can not connect to {0.host} ,{1}'.format(conni,result))

        print('{0.host} get score {1}'.format(conni,hosts_score[conni.host]))
        print('##################')

    #check auto_mount
    try:
        mnt3 = gp1.run('df -h|grep lv_redhat',warn = True)
        # re2 = gp1.run('ip a', warn=True)
    except GroupException as no_conn:

        mnt3 = no_conn.result
    except Exception as all_exception:
            print(all_exception)
            print(type(all_exception))
    for conni,result in mnt3.items():
        if isinstance(result,runners.Result):
            if '''/mnt/lv_redhat''' in str(result):
               hosts_score[conni.host].append(1)
            else:
                hosts_score[conni.host].append(0)
        else:
            hosts_score[conni.host].append(0)
            print('can not connect to {0.host} ,{1}'.format(conni,result))

        print('{0.host} get score {1}'.format(conni,hosts_score[conni.host]))
        print('##################')
    vm_score = {}
    for hostname,fin_score in hosts_score.items():
        sum_score = sum(fin_score)
        print('{0} get {1},final score is {2}'.format(hostname,fin_score,sum_score))
        #print('2nd score is {0}'.format(fin_score[2]))

        vm_score[hostname] = [sum_score]
    return vm_score
