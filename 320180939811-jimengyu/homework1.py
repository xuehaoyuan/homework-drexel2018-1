'''
CopyRight 2020 by Jimengyu
ID: 320180939811
email = "jimy18@lzu.edu.cn"
Every body can use this code in any ways
'''

import os, re, sys
from subprocess import Popen, PIPE, DEVNULL
from datetime import datetime as dt

class operation():
    def __init__(self, rev, rev2, rev_range):
        self.rev = rev
        self.rev = rev2
        self.rev_range = rev_range


    def first_func(self):
        gitcnt = "git rev-list --pretty=format:\"%ai\" " + self.rev1 + "..." + self.rev2
        git_rev_list = subprocess.Popen(gitcnt, stdout=PIPE, stderr=DEVNULL, shell=True)
        raw_counts = git_rev_list.communicate()[0]
        cnt = re.findall('[0-9]*-[0-9]*-[0-9]*', str(raw_counts))
        if cnt == 0:
            raise TheValueError('There is something wrong with your input')
        return len(cnt)

    def second_func(self):
        v44 = 1452466892
        gittag = "git log -1 --pretty=format:\"%ct\" " + self.rev2
        git_tag_date = subprocess.Popen(gittag, stdout=PIPE, stderr=DEVNULL, shell=True)
        seconds = git_cmd.communicate()[0]
        return ((int(seconds)-base))//3600


def launch():
    rev = sys.argv[1]
    rev_range = int(sys.argv[2])
    cumulative = 0
    if len(sys.argv) == 4:
        if (sys.argv[3] == "c"):
            cumulative = 1
        else:
            print("There are something wrong with the third parameter.")
    else:
        print("The length of parameter is wrong")
    for i in range(1,self.rev_range+1):
        rev2 = rev + "." +str(i)
        try:
            commit_cnt = operation(rev, rev2, rev_range).first_func()
        except ValueError:
            print('There is something wrong with your input')
        try:
            days = operation(rev, rev2, rev_range).second_func()
        except ValueError:
            print('There is something wrong with your input')
        print("%d %d %d" % (i,days,commit_cnt))
        
if __name__ == "__main__":
    launch()
