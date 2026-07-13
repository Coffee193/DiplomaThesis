import json
import os

INPUT_REQUIRED_KEYS = {'workcenters', 'resources', 'jobs', 'tasks', 'tasksuitableresources', 'taskprecedenceconstraints', 'setupmatrices'}
INPUT_OPTIONAL_KEYS = {'tooltypes', 'tools', 'mobileresourcetypes', 'mobileresources', 'continueAssignmentsAfterPlanEndDate', 'id', 'planEndDateDay', 'planEndDateMonth', 'planEndDateYear', 'planStartDateDay', 'planStartDateMonth', 'planStartDateYear'}
INPUT_ALL_KEYS = INPUT_REQUIRED_KEYS | INPUT_OPTIONAL_KEYS

JOB_REQUIRED_KEYS = {'name', 'description', 'arrivaldate', 'duedate', 'jobtaskreference', 'jobworkcenterreference', 'id'}
TASK_REQUIRED_KEYS = {'name', 'description', 'properties', 'id'}
RESOURCE_REQUIRED_KEYS = {'name', 'description', 'setupmatrixreference', 'resourceavailability', 'properties', 'endeffectors', 'id'}
TSR_REQUIRED_KEYS = {'resourcereference', 'toolreference', 'mobileresourcereference', 'taskreference', 'operationtimeperbatchinseconds', 'setupcode', 'properties'}
TPC_REQUIRED_KEYS = {'preconditiontaskreference', 'postconditiontaskreference', 'nexttaskinchain', 'resourceunavailableuntilnexttask'}

OUTPUT_REQUIRED_KEYS = {'assignments'}
ASSIGNMENT_REQUIRED_KEYS = {'task', 'resource', 'timeofdispatch', 'durationinmilliseconds', 'properties', 'locked'}
OUTPUT_DATE_KEYS = {'day', 'month', 'year', 'hour', 'minutes', 'seconds'}

packages_dir = os.path.join('json_examples', 'packages')

for root, dirs, files in os.walk(packages_dir):
    for f in files:
        if not f.endswith('.json'):
            continue
        filepath = os.path.join(root, f)
        rel_path = filepath.replace(os.sep, '/')

        with open(filepath, 'r', encoding='utf-8') as fh:
            data = json.load(fh)

        is_input = '/input/' in rel_path
        is_output = '/output/' in rel_path
        issue_types = set()

        if is_input:
            top_keys = set(data.keys())
            missing = INPUT_REQUIRED_KEYS - top_keys
            extra = top_keys - INPUT_ALL_KEYS
            if missing:
                issue_types.add('Missing top-level keys: ' + str(sorted(missing)))
            if extra:
                issue_types.add('Extra top-level keys: ' + str(sorted(extra)))

            jobs = data.get('jobs', {})
            if jobs and 'job' in jobs:
                for job in jobs['job']:
                    jm = JOB_REQUIRED_KEYS - set(job.keys())
                    if jm:
                        issue_types.add('All jobs missing keys: ' + str(sorted(jm)))

            tasks = data.get('tasks', {})
            if tasks and 'task' in tasks:
                for task in tasks['task']:
                    tm = TASK_REQUIRED_KEYS - set(task.keys())
                    if tm:
                        issue_types.add('All tasks missing keys: ' + str(sorted(tm)))

            tsrs = data.get('tasksuitableresources', {})
            if tsrs and 'tasksuitableresource' in tsrs:
                for tsr in tsrs['tasksuitableresource']:
                    tsrm = TSR_REQUIRED_KEYS - set(tsr.keys())
                    if tsrm:
                        issue_types.add('All tasksuitableresources missing keys: ' + str(sorted(tsrm)))

            tpcs = data.get('taskprecedenceconstraints', {})
            if tpcs and 'taskprecedenceconstraint' in tpcs:
                for tpc in tpcs['taskprecedenceconstraint']:
                    tpcm = TPC_REQUIRED_KEYS - set(tpc.keys())
                    if tpcm:
                        issue_types.add('All taskprecedenceconstraints missing keys: ' + str(sorted(tpcm)))

            resources = data.get('resources', {})
            if resources and 'resource' in resources:
                for res in resources['resource']:
                    rm = RESOURCE_REQUIRED_KEYS - set(res.keys())
                    if rm:
                        issue_types.add('All resources missing keys: ' + str(sorted(rm)))

        elif is_output:
            top_keys = set(data.keys())
            missing = OUTPUT_REQUIRED_KEYS - top_keys
            if missing:
                issue_types.add('Missing top-level: ' + str(sorted(missing)))
            asgns = data.get('assignments', {})
            if isinstance(asgns, dict) and 'assignment' in asgns:
                for asn in asgns['assignment']:
                    am = ASSIGNMENT_REQUIRED_KEYS - set(asn.keys())
                    if am:
                        issue_types.add('All assignments missing keys: ' + str(sorted(am)))
                    tod = asn.get('timeofdispatch')
                    if tod:
                        todm = OUTPUT_DATE_KEYS - set(tod.keys())
                        if todm:
                            issue_types.add('All timeofdispatch missing keys: ' + str(sorted(todm)))

        status = 'MALFORMED' if issue_types else 'OK'
        print(status + ': ' + rel_path)
        for it in sorted(issue_types):
            print('    -> ' + it)
