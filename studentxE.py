from fabric import group
from fabric import runners
from fabric import Connection
from fabric.exceptions import GroupException
def score_e():
    my_hosts = []
    for hosts_ip in range(122,123):
        my_hosts.append('172.20.{0}.224'.format(hosts_ip))

    hosts_score = {}
    for host_name in my_hosts:
        hosts_score[host_name] = []

    con_group = [Connection(host=host,user='root',connect_kwargs = {'password':'redhat'},connect_timeout = 1,port=2200) for host in my_hosts]
    gp1 = group.ThreadingGroup.from_connections(con_group)

    try:
        find2 = gp1.run('ls /etc/local/check/system_fix.txt',warn = True)
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
               hosts_score[conni.host].append(12)
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