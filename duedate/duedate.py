import sys
import argparse
from datetime import datetime
from datetime import time

from termcolor import colored

def parse_args():
    parser = argparse.ArgumentParser(description='manage and display a todo list')
    parser.add_argument('filename', metavar='filename', type=str, help='where to store the list')
    parser.add_argument('-a', metavar='add', type=str, help='add a task')
    parser.add_argument('-r', metavar='remove', type=str, help='remove a task with matching prefix')

    args = parser.parse_args()

    return args.filename, args.a, args.r

def get_lines(filename: str):
    taskfile = open(filename, 'r')
    lines = taskfile.readlines()
    taskfile.close()

    return lines

def parse_date(date_str):
    try:
        date_str = date_str.lstrip().rstrip()
        date_parsed = datetime.strptime('2021' + date_str, '%Y%b %d')
        
        return datetime.combine(date_parsed, time(hour=11, minute=00))
    except ValueError:
        try:
            return datetime.strptime('2021' + date_str, '%Y%b %d @<%I:%M%p')
        except ValueError:
            try:
                return datetime.strptime('2021' + date_str, '%Y%b %d @<%I%p')
            except ValueError:
                return None

def process_lines(lines, rm_prefix):
    # list of tuples of a story name and a list of tasks, i.e. [('CS 418', ['hw 8', 'read p233'])]
    # we use lists to preserve order of stories and tasks
    stories = []

    # dict mapping due dates to tasks, i.e. {9/17/2021 : [task1, task2]}
    dates = {}

    # a task that may be removed
    remove_candidate = None

    for line in lines:
        # trim right whitespace and newline
        line = line.rstrip()
        line_noindent = line.lstrip()

        # a tuple representing the story currently being built up, i.e. ('CS 418', ['hw 8', 'read p233'])
        current_story = stories[-1] if len(stories) else None
        
        # empty line case
        if len(line_noindent) == 0:
            if current_story:
                current_story[1].append((True, None, '', None))
            continue
        
        # no indentation - it's a story / category
        if len(line_noindent) == len(line):
            stories.append((line, []))  # subsequent tasks will go into this story
            continue
        
        # task is marked done if it's formatted like a python comment
        done = (line_noindent[0] == '#')

        # the date is always after a comma, attempt to find it
        words = line_noindent.split(',')

        date = 'no_date'
        date_str = ''
        taskname = line_noindent

        if len(words) > 1:
            d = parse_date(words[-1])

            if d:   # it was in fact the date => the task name is all but the last term
                date = d
                date_str = words[-1]
                taskname = line_noindent[:len(line_noindent) - len(date_str) - 1]
        
        # check if removal prefix matches current task
        if rm_prefix and taskname.lower().startswith(rm_prefix.lower()):
            # if we have multiple tasks that match, the removal operation fails
            if remove_candidate:
                rm_prefix = None
                remove_candidate = None
            else:
                remove_candidate = taskname

        item = (done, current_story[0], taskname, date_str)
        current_story[1].append(item)

        if not done:
            if date in dates:
                dates[date].append(item)
            else:
                dates[date] = [item]
    
    return stories, dates, remove_candidate

def print_tasks(dates_sorted):
    for s in dates_sorted:
        print()

        if s[0] != 'no_date':
            print(colored('Due %s, %s/%s @ %s', 'green') % (s[0].date().strftime('%A'), s[0].date().month, s[0].date().day, s[0].time()))
        else:
            print(colored('No date', 'green'))

        s[1].sort()
        for t in s[1]:
            print('  %s%s %s %s' % ('# ' if t[0] else '', t[2], colored('in', 'magenta'), colored(t[1], 'blue')))

def rewrite_file(filename, stories, to_remove):
    lines = []

    for s in stories:
        lines.append(s[0] + '\n')

        for t in s[1]:
            comment = ''
            if t[2] == to_remove:
                comment = '# '

            lines.append(' ' + comment + t[2] + (', ' + t[3] if t[3] else '') + '\n')

    taskfile = open(filename, 'w')
    taskfile.writelines(lines)
    taskfile.close()

def main():
    filename, add_me, rm_prefix = parse_args()

    lines = get_lines(filename)

    stories, dates, to_remove = process_lines(lines, rm_prefix)

    none_dates = []
    if 'no_date' in dates:
        none_dates = dates['no_date']
        dates.pop('no_date')

    dates_sorted = list(dates.items())
    dates_sorted.sort(reverse=True)

    if none_dates:
        dates_sorted.append(('no_date', none_dates))

    print_tasks(dates_sorted)

    if to_remove:
        print(colored('\nMarked task ', 'green') + colored(to_remove, 'white') + colored(' complete', 'green'))
        rewrite_file(filename, stories, to_remove)

if __name__ == '__main__':
    main()