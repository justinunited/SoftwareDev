from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from Database.DatabaseSetup import Base,Lecturer,Student,Enrollment,Subject,Grouping,Group,Task,Score,Credit,Archive

engine = create_engine('sqlite:///database.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

def create_student(id,user,password,name,year,section,gpax):
    new_student = Student(id_student = id, user_student = user, password_student = password, name_student =  name,year_student = year, section_student = section , gpax_student = gpax)
    session.add(new_student)
    session.commit()
    return
def delete_student(id):
    student = session.query(Student).filter_by(id_student = id)[0]
    student_enrollment = session.query(Enrollment).filter_by(student_id_enrollment = id)
    for enrollment in student_enrollment:
        student_grouping = session.query(Grouping).filter_by(subject_grouping = enrollment.subject_enrollment)
        for grouping in student_grouping:
            student_group = session.query(Group).filter_by(grouping_group =grouping,student_id_group =id)
            for group in student_group:
                session.delete(group)
            student_task = session.query(Task).filter_by(task_score = grouping)
            for task in student_task:
                student_score = session.query(Score).filter_by(task_score = task,student_id_score = id)
                for score in student_score:
                    session.delete(score)
        session.delete(enrollment)
    session.delete(student)
    session.commit()
    return
######################################################################################
def create_lecturer(id,user,password,name):
    new_lecturer = Lecturer(id_lecturer = id, user_lecturer = user, password_lecturer = password, name_lecturer =  name)
    session.add(new_lecturer)
    session.commit()
    return
def delete_lecturer(id):
    old_lecturer = session.query(Lecturer).filter_by(id_lecturer=id)[0]
    session.delete(old_lecturer)
    old_lecturer_enrollment = session.query(Enrollment).filter_by(lecturer_id_enrollment = id)
    for someone in old_lecturer_enrollment:
        session.delete(someone)
    session.commit()
    return
######################################################################################
def create_subject(name,code):
    new_subject = Subject(name_subject = name , code_subject = code)
    session.add(new_subject)
    session.commit()
    return
def delete_subject(subject_code):
    subject_code = session.query(Subject).filter_by(code_subject = subject_code)[0]
    subject_enrollment = session.query(Enrollment).filter_by(subject_enrollment = subject_code)
    subject_grouping = session.query(Grouping).filter_by(subject_grouping = subject_code)
    for grouping in subject_grouping:
        subject_group =session.query(Group).filter_by(grouping_group = grouping)
        for group in subject_group:
            session.delete(group)
        subject_task = session.query(Task).filter_by(grouping_task = grouping)
        for task in subject_task:
            subject_score = session.query(Score).filter_by(task_score = task)
            for score in subject_score:
                session.delete(score)
            session.delete(task)
        session.delete(grouping)
    for enrollment in subject_enrollment:
        session.delete(enrollment)
    session.delete(subject_code)
    session.commit()
    return
######################################################################################
def create_enrollment(subject_code, student_id ,lecturer_id ):
    subject_code = session.query(Subject).filter_by(code_subject= subject_code)[0]
    new_enrollment = Enrollment(subject_enrollment = subject_code , student_id_enrollment = student_id,lecturer_id_enrollment = lecturer_id)
    session.add(new_enrollment)
    session.commit()
    return
#delete student in specific subject
def delete_student_enrollment(student_id,subject_code):
    subject_code = session.query(Subject).filter_by(code_subject = subject_code)[0]
    student = session.query(Enrollment).filter_by(student_id_enrollment = student_id,subject_enrollment = subject_code)[0]
    enrollment_grouping = session.query(Grouping).filter_by(subject_grouping = subject_code)[0]
    enrollment_group = session.query(Group).filter_by(grouping_group = enrollment_grouping,student_id_group = student_id)[0]
    enrollment_task = session.query(Task).filter_by(grouping_task = enrollment_grouping)[0]
    enrollment_score = session.query(Score).filter_by(task_score = enrollment_task,student_id_score = student_id)[0]
    session.delete(enrollment_score)
    session.delete(enrollment_group)
    session.delete(student)
    session.commit()
    return
#delete lecturer in specific subject
def delete_lecturer_enrollment(lecturer_id,subject_code):
    lecturer = session.query(Enrollment).filter_by(lecturer_id_enrollment = lecturer_id,subject_code_enrollment = subject_code)[0]
    session.delete(lecturer)
    session.commit()
    return
######################################################################################
def create_grouping(grouping_name,grouping_type,subject_code):
    subject_code = session.query(Subject).filter_by(code_subject= subject_code)[0]
    new_grouping = Grouping(name_grouping=grouping_name,type_grouping=grouping_type,subject_grouping=subject_code)
    session.add(new_grouping)
    session.commit()
    return

def delete_grouping(grouping_id):
    #change subject_code into object
    grouping = session.query(Grouping).filter_by(id_grouping = grouping_id)[0]
    grouping_group = session.query(Group).filter_by(grouping_group = grouping)
    grouping_task = session.query(Task).filter_by(grouping_task = grouping)
    for sometask in grouping_task:
        grouping_score = session.query(Score).filter_by(task_score = sometask)
        for somescore in grouping_score:
            session.delete(somescore)
        session.delete(sometask)
    for somegroup in grouping_group:
        session.delete(somegroup)
    session.delete(grouping)
    session.commit()
    return
######################################################################################
def create_group(grouping_id,student_id,group_id):
    grouping_id = session.query(Grouping).filter_by(id_grouping=grouping_id)[0]
    new_group = Group(student_id_group = student_id ,group_id_group = group_id, grouping_group = grouping_id)
    session.add(new_group)
    session.commit()
    return
#Dont have delete function in group
######################################################################################
def create_task(grouping_id,name,weight):
    if grouping_id is not None:
        grouping_id = session.query(Grouping).filter_by(id_grouping=grouping_id)[0]
        new_task = Task(name_task = name, weight_task = weight ,grouping_task = grouping_id)
    else:
        new_task = Task(name_task = name, weight_task = weight ,grouping_task = None)
    session.add(new_task)
    session.commit()
    return
def delete_task(task_id):
    task = session.query(Task).filter_by(id_task = task_id)[0]
    session.delete(task)
    session.commit()
    return
######################################################################################
def create_score(task_id,student_id,score):
    task_id = session.query(Task).filter_by(id_task=task_id)[0]
    new_score = Score(score_score = score,student_id_score = student_id,task_score = task_id)
    session.add(new_score)
    session.commit()
    return
def delete_score(task_id,student_id):
    task_id = session.query(Task).filter_by(id_task = task_id)[0]
    score = session.query(Score).filter_by(task_score = task_id,student_id_score = student_id)[0]
    session.delete(score)
    session.commit()
    return
######################################################################################

def create_credit(group_id,subject_code,credit,task_name):
    groups = session.query(Group).filter_by(group_id_group = group_id)
    for somegroup in groups:
        if somegroup.grouping_group.subject_code_grouping == subject_code:
            new_credit = Credit(group_id_credit = group_id , grouping_id_credit = somegroup.grouping_id_group,credit = credit,task_name_credit = task_name)
            session.add(new_credit)
            session.commit()
            return
######################################################################################
def create_archive(name_lecturer,subject_code):
    lecturer = session.query(Lecturer).filter_by(user_lecturer = name_lecturer).one()
    new_archive = Archive(subject_code_archive = subject_code,lecturer_archive = lecturer)
    session.add(new_archive)
    session.commit()
    return

def delete_archive(name_lecturer,subject_code):
    lecturer = session.query(Lecturer).filter_by(user_lecturer = name_lecturer)[0]
    archive = session.query(Archive),filter_by(subject_code_archive = subject_code,lecturer_id_archive = name_lecturer )
    session.delete(archive)
    session.commit()
    return
######################################################################################
def create_storage(student_id,task_name,score):
    storage = session.query(storage).filter_by(student_id_storage = student_id,task_name_storage = task_name,score_storage = score)
    session.add(storage)
    session.commit()
    return
######################################################################################

# create_archive("Mr.Bawornsak","FRA111")
# create_archive("Mr.Bawornsak","FRA222")

# create_student(59340500001,'user1','12345','Kanyarat Kovitmongkol',2,'A',1.55)
# create_student(59340500002,'user2','12345','Kittipop liaosuthamat',2,'A',2.00)
# create_student(59340500004,'user3','12345','Kelwalee rattanasakulthong',2,'A',3.00)
# create_student(59340500005,'user4','12345','Kanut Thummaruksa',2,'A',4.00)
# create_student(59340500006,'user5','12345','Komkrit Thongbunchu',2,'A',3.00)
# create_student(59340500008,'user6','12345','Chakputtana Sangpradit',2,'A',2.00)
# create_student(59340500009,'user7','12345','Chonnapat Kitpasert',2,'A',1.60)
# create_student(59340500010,'user8','12345','Chanagan Kanokwattananon',2,'A',2.00)
# create_student(59340500011,'user9','12345','Chanittha Techasombooranakit',2,'A',3.00)
# create_student(59340500012,'user10','12345','Chalita Rattanopas',2,'A',4.00)
# create_student(59340500013,'user11','12345','Chawakorn Chaichanawirote',2,'A',3.00)
# create_student(59340500014,'user12','12345','Chawisorn Samrit',2,'A',2.00)
# create_student(59340500015,'user13','12345','Natanon Trangratanajit',2,'A',2.00)
# create_student(59340500016,'user14','12345','Nuttida Peeklom',2,'B',3.00)
# create_student(59340500017,'user15','12345','Natthaphon Sudadech',2,'B',4.00)
# create_student(59340500018,'user16','12345','Natworpong Loyswai',2,'B',3.00)
# create_student(59340500019,'user17','12345','Nuttawat Chantraphakorn',2,'B',2.00)
# create_student(59340500020,'user18','12345','Tretap Promwiset',2,'B',2.00)
# create_student(59340500021,'user19','12345','Thipawan Pairam',2,'B',3.00)
# create_student(59340500022,'user20','12345','Thanatorn Khumrang',2,'B',4.00)
# create_student(59340500023,'user21','12345','Warasinee Chaisangmongkon',9,'B',4.00)
# create_student(59340500024,'user22','12345','Suriya Natsupakpong',9,'B',4.00)
# create_student(59340500025,'user23','12345','Bawornsak Sakulkueakulsuk',9,'B',4.00)


# create_lecturer(1,"pitiwut","teerakittikul","Pitiwut")
# create_lecturer(3,"warasinee","chaisangmongkon","Warasinee")
# create_lecturer(2,"bawornsak","sakulkueakulsuk","Bawornsak")
# create_lecturer(4,"suriya","natsupakpong","Suriya")
# create_lecturer(5,"djitt","laowattana","Djitt")

# create_subject('Software Development','FRA241')

# create_enrollment("FRA241", 59340500001 , None)
# create_enrollment("FRA241", 59340500002 , None)
# create_enrollment("FRA241", 59340500003 , None)
# create_enrollment("FRA241", 59340500004 , None)
# create_enrollment("FRA241", 59340500005 , None)
# create_enrollment("FRA241", 59340500006 , None)
# create_enrollment("FRA241", 59340500007 , None)
# create_enrollment("FRA241", 59340500008 , None)
# create_enrollment("FRA241", 59340500009 , None)
# create_enrollment("FRA241", 59340500010 , None)
# create_enrollment("FRA241", 59340500011 , None)
# create_enrollment("FRA241", 59340500012 , None)
# create_enrollment("FRA241", 59340500013 , None)
# create_enrollment("FRA241", 59340500014 , None)
# create_enrollment("FRA241", 59340500015 , None)
# create_enrollment("FRA241", 59340500016 , None)
# create_enrollment("FRA241", 59340500017 , None)
# create_enrollment("FRA241", 59340500018 , None)
# create_enrollment("FRA241", 59340500019 , None)
# create_enrollment("FRA241", 59340500020 , None)

# create_grouping('Grouping by RANDOM','RANDOM','FRA241')

# create_group(1,59340500001,'AB01')
# create_group(1,59340500002,'AB02')
# create_group(1,59340500003,'AB03')
# create_group(1,59340500004,'AB04')
# create_group(1,59340500005,'AB05')
# create_group(1,59340500006,'AB06')
# create_group(1,59340500007,'AB07')
# create_group(1,59340500008,'AB08')
# create_group(1,59340500009,'AB09')
# create_group(1,59340500010,'AB10')
# create_group(1,59340500011,'AB01')
# create_group(1,59340500012,'AB02')
# create_group(1,59340500013,'AB03')
# create_group(1,59340500014,'AB04')
# create_group(1,59340500015,'AB05')
# create_group(1,59340500016,'AB06')
# create_group(1,59340500017,'AB07')
# create_group(1,59340500018,'AB08')
# create_group(1,59340500019,'AB09')
# create_group(1,59340500020,'AB10')

# create_task(1,'Software Development',5)

# create_score(1,59340500001,5)
# create_score(1,59340500002,4)
# create_score(1,59340500003,3)
# create_score(1,59340500004,2)
# create_score(1,59340500005,1)
# create_score(1,59340500006,5)
# create_score(1,59340500007,4)
# create_score(1,59340500008,3)
# create_score(1,59340500009,2)
# create_score(1,59340500010,1)
# create_score(1,59340500011,5)
# create_score(1,59340500012,4)
# create_score(1,59340500013,3)
# create_score(1,59340500014,2)
# create_score(1,59340500015,1)
# create_score(1,59340500016,5)
# create_score(1,59340500017,4)
# create_score(1,59340500018,3)
# create_score(1,59340500019,2)
# create_score(1,59340500020,1)

# for i in range(1,3):
#     create_enrollment('FRA241', None, i)

# create_credit('AB01',"FRA241",10,"Software Development")
# create_credit('AB02',"FRA241",20,"Software Development")
# create_credit('AB03',"FRA241",30,"Software Development")
# create_credit('AB04',"FRA241",40,"Software Development")
# create_credit('AB05',"FRA241",50,"Software Development")
# create_credit('AB06',"FRA241",60,"Software Development")
# create_credit('AB07',"FRA241",70,"Software Development")
# create_credit('AB08',"FRA241",80,"Software Development")
# create_credit('AB09',"FRA241",90,"Software Development")
# create_credit('AB10',"FRA241",100,"Software Development")
