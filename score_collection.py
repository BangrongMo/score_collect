import studentxA as vmA
import studentxB as vmB
import studentxC as vmC
import studentxD as vmD
import studentxE as vmE

students_score_collection = {}

for student_num in range(122, 199):
    students_score_collection[str(student_num)]=[]

reA = vmA.score_a()
reB = vmB.score_b()
reC = vmC.score_c()
reD = vmD.score_d()
reE = vmE.score_e()


print(reA)
print(reB)
print(reC)
print(reD)
print(reE)

for std_num,fin_score in students_score_collection.items():
    try:
        students_score_collection[std_num] = reA['172.20.{0}.220'.format(std_num)] +reB['172.20.{0}.221'.format(std_num)] \
                                             +reC['172.20.{0}.222'.format(std_num)] +reD['172.20.{0}.223'.format(std_num)] \
                                             +reE['172.20.{0}.224'.format(std_num)]
    except Exception :
        students_score_collection[std_num] = [0]

    print(std_num,sum(students_score_collection[std_num]))