import studentxA as vmA
import studentxB as vmB
import studentxC as vmC
import studentxD as vmD
import studentxE as vmE
start_h = 138
end_h = 139
students_score_collection = {}

for student_num in range(start_h, end_h):
    students_score_collection[str(student_num)]=[]

reA = vmA.score_a(start_h,end_h)
reB = vmB.score_b(start_h,end_h,ssh_port=2200)
reC = vmC.score_c(start_h,end_h)
reD = vmD.score_d(start_h,end_h)
reE = vmE.score_e(start_h,end_h)


print("*print collection")
for std_num,fin_score in students_score_collection.items():
    try:
        students_score_collection[std_num] = reA['172.20.{0}.220'.format(std_num)]
        students_score_collection[std_num] = reA['172.20.{0}.220'.format(std_num)] +reB['172.20.{0}.221'.format(std_num)] \
                                             +reC['172.20.{0}.222'.format(std_num)] +reD['172.20.{0}.223'.format(std_num)] \
                                             +reE['172.20.{0}.224'.format(std_num)]
    except Exception :
        students_score_collection[std_num] =  students_score_collection[std_num].append(0)

    print(std_num,students_score_collection[std_num],sum(students_score_collection[std_num]))