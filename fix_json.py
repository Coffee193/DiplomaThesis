import json
import os
import shutil
from datetime import datetime

packages_dir = os.path.join('json_examples', 'packages')
corrected_dir = os.path.join('json_examples', 'packages_corrected')

if os.path.exists(corrected_dir):
    shutil.rmtree(corrected_dir)

for root, dirs, files in os.walk(packages_dir):
    for f in sorted(files):
        if not f.endswith('.json'):
            continue
        src = os.path.join(root, f)
        rel = os.path.relpath(src, packages_dir)
        dst = os.path.join(corrected_dir, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)

        with open(src, 'r', encoding='utf-8') as fh:
            data = json.load(fh)

        rel_slash = rel.replace(os.sep, '/')
        is_input = '/input/' in rel_slash or rel_slash.startswith('input/')
        is_output = '/output/' in rel_slash or rel_slash.startswith('output/')

        if is_input:
            # Fix workcenters: add missing toolrepository and dockingstations
            wcs = data.get('workcenters')
            if wcs and isinstance(wcs, dict) and 'workcenter' in wcs:
                for wc in wcs['workcenter']:
                    if 'toolrepository' not in wc:
                        wc['toolrepository'] = None
                    if 'dockingstations' not in wc:
                        wc['dockingstations'] = None

            # Fix jobs: add missing description
            jobs = data.get('jobs')
            if jobs and isinstance(jobs, dict) and 'job' in jobs:
                for job in jobs['job']:
                    if 'description' not in job:
                        job['description'] = None

            # Fix tasksuitableresources: remove extra 'id', add missing keys
            tsrs = data.get('tasksuitableresources')
            if tsrs and isinstance(tsrs, dict) and 'tasksuitableresource' in tsrs:
                for tsr in tsrs['tasksuitableresource']:
                    if 'id' in tsr:
                        del tsr['id']
                    if 'toolreference' not in tsr:
                        tsr['toolreference'] = None
                    if 'mobileresourcereference' not in tsr:
                        tsr['mobileresourcereference'] = None
                    if 'properties' not in tsr:
                        tsr['properties'] = None

            # Fix taskprecedenceconstraints: add missing keys
            tpcs = data.get('taskprecedenceconstraints')
            if tpcs and isinstance(tpcs, dict) and 'taskprecedenceconstraint' in tpcs:
                for tpc in tpcs['taskprecedenceconstraint']:
                    if 'nexttaskinchain' not in tpc:
                        tpc['nexttaskinchain'] = None
                    if 'resourceunavailableuntilnexttask' not in tpc:
                        tpc['resourceunavailableuntilnexttask'] = None

            # Add missing optional top-level keys as null
            for key in ['tooltypes', 'tools', 'mobileresourcetypes', 'mobileresources']:
                if key not in data:
                    data[key] = None

        elif is_output:
            # Remove extra top-level keys
            for key in ['scheduleId', 'generatedAt']:
                if key in data:
                    del data[key]

            # Fix assignments structure: list -> {"assignment": list}
            asgns = data.get('assignments')
            if isinstance(asgns, list):
                fixed_assignments = []
                for asn in asgns:
                    fixed = {}

                    # task: "string" -> {"id": "string"}
                    task_val = asn.get('task')
                    if isinstance(task_val, str):
                        fixed['task'] = {'id': task_val}
                    else:
                        fixed['task'] = task_val

                    # resource: "string" -> {"id": "string"}
                    res_val = asn.get('resource')
                    if isinstance(res_val, str):
                        fixed['resource'] = {'id': res_val}
                    else:
                        fixed['resource'] = res_val

                    # startTime: ISO string -> timeofdispatch dict
                    start_time = asn.get('startTime')
                    if isinstance(start_time, str):
                        dt = datetime.fromisoformat(start_time)
                        fixed['timeofdispatch'] = {
                            'day': dt.day,
                            'month': dt.month,
                            'year': dt.year,
                            'hour': dt.hour,
                            'minutes': dt.minute,
                            'seconds': dt.second
                        }
                    elif 'timeofdispatch' in asn:
                        fixed['timeofdispatch'] = asn['timeofdispatch']

                    # durationSeconds -> durationinmilliseconds
                    if 'durationSeconds' in asn:
                        fixed['durationinmilliseconds'] = asn['durationSeconds'] * 1000
                    elif 'durationinmilliseconds' in asn:
                        fixed['durationinmilliseconds'] = asn['durationinmilliseconds']

                    # Add properties and locked
                    fixed['properties'] = asn.get('properties', None)
                    fixed['locked'] = asn.get('locked', None)

                    fixed_assignments.append(fixed)

                data['assignments'] = {'assignment': fixed_assignments}

        with open(dst, 'w', encoding='utf-8') as fh:
            json.dump(data, fh, indent=4, ensure_ascii=False)

        print('Written: ' + rel.replace(os.sep, '/'))

print('\nDone! Corrected files in: ' + corrected_dir.replace(os.sep, '/'))
