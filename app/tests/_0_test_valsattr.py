'''
### JOB ###
vars possible:
    name
    arrivaldate
    duedate
    jobtaskreference
    jobworkcenterreference
    id

# Question Possible
    _NONE_
user_question = "List all jobs"
user_question = "Give me the jobs"
    _POSITION_
user_question = "Return the first job"
user_question = "Return the job at index 5"
user_question = "Return the fifth job"
    _ATTRIBUTE_
user_question = "Return the job with arrival date 31/3"
user_question = "Return the job with id 8"
user_question = "Are there any jobs with arrival date 31 2"
user_question = "What jobs require the task with id 584"
user_question = "List jobs with id 51"
user_question = "Find jobs that require task 581"
user_question = "Find jobs that require task with id 581"
user_question = "Find the last job that requires task with id 581"

'''

'''
### TASKPRECEDENCECONSTRAINT ###
vars possible
    preconditiontaskreference
    postconditiontaskreference

# Question possible
user_question = "Is there a task to be executed before task with id 483?" #old: pos
user_question = "Is there a task to be executed before task 483?" #old: pos
user_question = "Is there a task to be executed before 183?" #old: pos
user_content = 'Which task should i execute before task 1?' #old: pos
user_content = 'What task can i execute after completing task 1?' #old: pos
user_content = 'Which task can i do after task 1?' #old: pos
user_content = 'Does task 53 require another task to be executed beforehand?' #old: none
user_content = 'Is task 11 independent of other tasks?' #old: none
'''

'''
### TASKSUITABLERESOURCES ###
vars possible
    resourcereference
    taskreference
    operationtimeperbatchinseconds
    setupcode

# Question possible
user_content = 'Which tasks can be done in resource 1?' #old: attr
user_content = 'Where can task 1 be executed' #old: none
user_content = 'Which resource can execute task 1?' #old: attr
user_content = 'Can Task 1 be executed in the MELTSHOP?' #old: none
user_content = 'How long does task 1 take?' #old: none
user_content = 'What resource can execute each task?' #old:none
'''