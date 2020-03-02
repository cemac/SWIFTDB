"""
Bespoke example script for creating archive
take current snap shot of site and last night's backup
"""

import pandas as pd
import glob

print('requires pandas 1.0.0')
# The current state of WPS,tasks,deliverables
workpackages = pd.read_csv('current/work_packages.csv')
tasks = pd.read_csv('current/tasks.csv')
deliverables = pd.read_csv('current/deliverables.csv')
workpackages = workpackages[['code', 'status', 'issues',
                            'next_deliverable', 'date_edited']]
tasks = tasks[['code', 'person_responsible', 'progress',
               'percent', 'papers', 'paper_submission_date', 'date_edited']]
deliverables = deliverables[['code', 'person_responsible', 'month_due',
                             'progress', 'percent', 'papers',
                             'paper_submission_date', 'date_edited']]
# go back through backups


def create_archive(table, tablename):
    """create_archive
    description: go through old csvs and append a mega dataframe of all the
                 weeks data, add in approximate date_edited if doesn't exist
                 remove duplicates to show date update came into effect and
                 generate count of updates for each item
    args:
         table (dataframe): dataframe of current table
         tablename (str): name of table (work_packages, deliverables, tasks)
    returns:
         table (dataframe): the full table of items indexed by date and with
                            entry for each update
         count (dataframe): code and count to show number of updates to each
                            item
    """
    for wp in glob.iglob('../BACKUP/csvs/*/' + tablename + '.csv'):
        wparchive = pd.read_csv(wp)
        try:
            if tablename == 'work_packages':
                wparchive = wparchive[['code', 'status', 'issues',
                                       'next_deliverable', 'date_edited']]
            else:
                wparchive = wparchive[['code', 'person_responsible',
                                       'progress', 'percent', 'papers',
                                       'paper_submission_date', 'date_edited']]
        except KeyError:
            if tablename == 'work_packages':
                wparchive = wparchive[['code', 'status', 'issues',
                                       'next_deliverable']]
            else:
                wparchive = wparchive[['code', 'progress', 'percent']]
                wparchive['person_responsible'] = 'not recorded'
                wparchive['papers'] = 'not recorded'
                wparchive['paper_submission_date'] = 'not recorded'
            datestr = wp[15:-18]
            year = datestr[0:4]
            mnt = datestr[4:6]
            day = datestr[6::]
            wparchive['date_edited'] = str(year + '-' + mnt + '-' + day)
        table = table.append(wparchive)

    # set edit date as index to sort by date and allow duplicates to be found
    table = table.set_index('date_edited')
    # remove blank entrys
    if tablename == 'work_packages':
        table = table[table.status.notnull()]
    else:
        table = table[table.progress.notnull()]
    # old to new
    table = table.sort_index()
    # select only the different ones
    table = table.drop_duplicates(keep='first')
    # Counts
    counts = table['code'].value_counts()
    table = table.reset_index()
    counts = counts.reset_index()
    counts = counts.rename(columns={'index': 'code', 'code': 'count'})
    return table, counts


workpackagesnew, countswp = create_archive(workpackages, 'work_packages')
deliverablesnew, countsd = create_archive(deliverables, 'deliverables')
tasksnew, countst = create_archive(tasks, 'tasks')
# save to tab files
workpackagesnew.to_csv('wp_archive.tab', sep='\t', index=False, header=False)
tasksnew.to_csv('tasks_archive.tab', sep='\t', index=False, header=False)
deliverablesnew.to_csv('deliverables_archive.tab', sep='\t', index=False,
                       header=False)
# concatonate counts
allcounts = countswp.append(countsd)
allcounts = allcounts.append(countst)
allcounts.to_csv('counts.tab', sep='\t', index=False,
                 header=False)
