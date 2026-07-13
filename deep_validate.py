import json, os

INPUT_REQUIRED_SECTIONS = {'workcenters', 'resources', 'jobs', 'tasks', 'tasksuitableresources', 'taskprecedenceconstraints', 'setupmatrices'}

WRAPPERS = {
    'workcenters': 'workcenter',
    'resources': 'resource',
    'jobs': 'job',
    'tasks': 'task',
    'tasksuitableresources': 'tasksuitableresource',
    'taskprecedenceconstraints': 'taskprecedenceconstraint',
    'setupmatrices': 'setupmatrix',
}

WORKCENTER_KEYS = {'name', 'description', 'algorithm', 'workcenterresourcereference', 'toolrepository', 'dockingstations', 'id'}
RESOURCE_KEYS = {'name', 'description', 'setupmatrixreference', 'resourceavailability', 'properties', 'endeffectors', 'id'}
JOB_KEYS = {'name', 'description', 'arrivaldate', 'duedate', 'jobtaskreference', 'jobworkcenterreference', 'id'}
TASK_KEYS = {'name', 'description', 'properties', 'id'}
TSR_KEYS = {'resourcereference', 'toolreference', 'mobileresourcereference', 'taskreference', 'operationtimeperbatchinseconds', 'setupcode', 'properties'}
TPC_KEYS = {'preconditiontaskreference', 'postconditiontaskreference', 'nexttaskinchain', 'resourceunavailableuntilnexttask'}
SETUP_KEYS = {'setup', 'id'}

ENTITY_KEYS = {
    'workcenter': WORKCENTER_KEYS,
    'resource': RESOURCE_KEYS,
    'job': JOB_KEYS,
    'task': TASK_KEYS,
    'tasksuitableresource': TSR_KEYS,
    'taskprecedenceconstraint': TPC_KEYS,
    'setupmatrix': SETUP_KEYS,
}

OUTPUT_ASSIGNMENT_KEYS = {'task', 'resource', 'timeofdispatch', 'durationinmilliseconds', 'properties', 'locked'}
TIMEOFDISPATCH_KEYS = {'day', 'month', 'year', 'hour', 'minutes', 'seconds'}

OPTIONAL_TOP = {'tooltypes', 'tools', 'mobileresourcetypes', 'mobileresources', 'continueAssignmentsAfterPlanEndDate', 'id', 'planEndDateDay', 'planEndDateMonth', 'planEndDateYear', 'planStartDateDay', 'planStartDateMonth', 'planStartDateYear'}
ALL_INPUT_KEYS = INPUT_REQUIRED_SECTIONS | OPTIONAL_TOP

corrected_dir = 'json_examples/packages_corrected'

for root, dirs, files in os.walk(corrected_dir):
    for f in sorted(files):
        if not f.endswith('.json'):
            continue
        filepath = os.path.join(root, f)
        rel = os.path.relpath(filepath, corrected_dir).replace(os.sep, '/')

        with open(filepath, 'r') as fh:
            data = json.load(fh)

        is_input = '/input/' in rel
        is_output = '/output/' in rel
        issues = []

        if is_input:
            top_keys = set(data.keys())

            for s in INPUT_REQUIRED_SECTIONS:
                if s not in top_keys:
                    issues.append(f'MISSING required section: {s}')

            for section, wrapper_key in WRAPPERS.items():
                if section in data:
                    val = data[section]
                    if val is None:
                        continue
                    if not isinstance(val, dict):
                        issues.append(f'{section} is {type(val).__name__}, expected dict wrapping "{wrapper_key}"')
                        continue
                    if wrapper_key not in val:
                        issues.append(f'{section} missing wrapper key "{wrapper_key}"')
                        continue
                    if not isinstance(val[wrapper_key], list):
                        issues.append(f'{section}.{wrapper_key} is not a list')
                        continue
                    expected_keys = ENTITY_KEYS.get(wrapper_key, set())
                    if expected_keys:
                        missing_summary = set()
                        extra_summary = set()
                        for item in val[wrapper_key]:
                            item_keys = set(item.keys())
                            missing_summary |= (expected_keys - item_keys)
                            extra_summary |= (item_keys - expected_keys)
                        if missing_summary:
                            issues.append(f'{section}.{wrapper_key}[] missing keys: {sorted(missing_summary)}')
                        if extra_summary:
                            issues.append(f'{section}.{wrapper_key}[] extra keys: {sorted(extra_summary)}')

            for k in OPTIONAL_TOP:
                if k not in top_keys:
                    issues.append(f'MISSING optional key: {k}')

            extra_top = top_keys - ALL_INPUT_KEYS
            if extra_top:
                issues.append(f'EXTRA top-level keys: {sorted(extra_top)}')

        elif is_output:
            top_keys = set(data.keys())
            if 'assignments' not in top_keys:
                issues.append('MISSING top-level key: assignments')
            else:
                asgns = data['assignments']
                if not isinstance(asgns, dict):
                    issues.append(f'assignments is {type(asgns).__name__}, expected dict with "assignment" key')
                elif 'assignment' not in asgns:
                    issues.append('assignments missing wrapper key "assignment"')
                elif not isinstance(asgns['assignment'], list):
                    issues.append('assignments.assignment is not a list')
                else:
                    missing_summary = set()
                    extra_summary = set()
                    tod_missing_summary = set()
                    ref_issues = set()
                    for asn in asgns['assignment']:
                        asn_keys = set(asn.keys())
                        missing_summary |= (OUTPUT_ASSIGNMENT_KEYS - asn_keys)
                        extra_summary |= (asn_keys - OUTPUT_ASSIGNMENT_KEYS)
                        tod = asn.get('timeofdispatch')
                        if tod and isinstance(tod, dict):
                            tod_missing_summary |= (TIMEOFDISPATCH_KEYS - set(tod.keys()))
                        for ref_key in ['task', 'resource']:
                            ref = asn.get(ref_key)
                            if ref is not None and (not isinstance(ref, dict) or 'id' not in ref):
                                ref_issues.add(f'{ref_key} should be dict with "id"')
                    if missing_summary:
                        issues.append(f'assignment[] missing keys: {sorted(missing_summary)}')
                    if extra_summary:
                        issues.append(f'assignment[] extra keys: {sorted(extra_summary)}')
                    if tod_missing_summary:
                        issues.append(f'timeofdispatch missing keys: {sorted(tod_missing_summary)}')
                    for ri in ref_issues:
                        issues.append(ri)

            extra_top = top_keys - {'assignments'}
            if extra_top:
                issues.append(f'EXTRA top-level keys: {sorted(extra_top)}')

        status = 'FAIL' if issues else 'OK'
        print(f'{status}: {rel}')
        for iss in issues:
            print(f'    -> {iss}')
        print()
