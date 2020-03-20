import os, re, subprocess, argparse
from datetime import datetime as dt


class Rev():
    def __init__(self, rev, rev_range):
        self.rev = rev
        self.rev_range = rev_range
        self.repo = 'D:\git\linux-stable'

    def get_commit_cnt(self, next_rev):             #Get the name and range.
        tagrange = self.rev + ".." + next_rev
        gitcnt = "git rev-list --pretty=format:\"%ai\" " + tagrange
        git_rev_list = subprocess.Popen(gitcnt, cwd=self.repo, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
        raw_counts = git_rev_list.communicate()[0]
        cnt = re.findall('[0-9]*-[0-9]*-[0-9]*', str(raw_counts))
        if len(cnt) == 0:
            raise TagNotExistError("No such revision range: {0}..{1}".format(self.rev, self.rev + str(self.rev_range)))
        return len(cnt)

    def get_tag_days(self, rev):                    #Get the data commit time.
        second = 3600
        hour = 24
        gittag = "git log -1 --pretty=format:\"%ct\" " + rev
        git_tag_date = subprocess.Popen(gittag, cwd=self.repo, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
        seconds = int(git_tag_date.communicate()[0])
        day = seconds // (second * hour)
        return day

    def get_log(self, rev2):                        #Get the log.
        commit_cnt = self.get_commit_cnt(rev2)
        if commit_cnt:
            current = self.get_tag_days(rev2)
            base = self.get_tag_days(self.rev)
            days = current - base
            return days, commit_cnt
        else:
            return False

    def log_print(self):                            #Print the result and  beautification file.
        tb = pt.PrettyTable()
        tb.field_names = ["version", "day", "commit"]
        for sl in range(1, self.rev_range+1):
            print(". . .")
            rev2 = self.rev + "." + str(sl)
            day, commit_cnt = self.get_log(rev2)
            if commit_cnt:
                tb.add_row([rev2, day, commit_cnt])
                print(rev2, day, commit_cnt)
            else:
                break
        with open('result', 'a') as f:
            f.write(str(tb))
        print(tb)
        
class TagError(Exception):
    def __init__(self, msg):
        self.msg = msg
        
class TagNotExistError(TagError):
    pass

for sl in range(1,rev_range+1):
    rev2 = rev + "." + str(sl)
    gitcnt = "git rev-list --pretty=format:\"%ai\" " + rev1 + "..." + rev2
    gittag = "git log -1 --pretty=format:\"%ct\" " + rev2
    git_rev_list = subprocess.Popen(gitcnt, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
    commit_cnt = get_commit_cnt(git_rev_list)
    if cumulative == 0:
        rev1 = rev2
    # if get back 0 then its an invalid revision number
    if commit_cnt:
        git_tag_date = subprocess.Popen(gittag, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
        days = get_tag_days(git_tag_date, v44)
        print("%d %d %d" % (sl,days,commit_cnt))
    else:
        break

