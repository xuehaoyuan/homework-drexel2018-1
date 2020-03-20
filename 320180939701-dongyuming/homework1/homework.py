#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Yuming Dong 320180939701"
__copyright__ = "Copyright 2020, LZU Data Science"
__version__ = "1.0.0"

import os, re, sys, shlex
from subprocess import Popen,PIPE,DEVNULL


class commit_count():
    def __init__(self, git_cmd, base, rev):
        self.git_cmd = git_cmd
        self.base = base
        self.rev = rev

    def get_commit_cnt(self):
        try:
            raw_counts = self.git_cmd.communicate()[0]
            # if we request something that does not exist -> 0
            cnt = re.findall('[0-9]*-[0-9]*-[0-9]*', str(raw_counts))
            return len(cnt)
        except Exception:
            print('Wrong! Please check your git command.')

    def get_tag_days(self):
        try:
            seconds = self.git_cmd.communicate()[0]
            SecPerHour = 3600
            seconds = self.git_cmd.communicate()[0]
            return (int(seconds)-self.base)//SecPerHour
        except Exception:
            print('Wrong! Please check your git command.')


            # get dates of all commits - unsorted 
    
    cumulative = 0
    if len(sys.argv) == 4:
        if (sys.argv[3] == "c"):
            cumulative = 1
        else:
            print("Dont know what you mean with %s" % sys.argv[3])
            sys.exit(-1)
    rev_range = int(sys.argv[2])

    rev = sys.argv[1]
        # setup and fill in the table
    print("#sublevel commits %s stable fixes" % sys.argv[1])
    print("lv hour bugs") #tag for R data.frame
    rev1 = rev
    # base time of v4.1 and v4.4 as ref base
    # fix this to extract the time of the base commit
    # from git !
    # hofrat@Debian:~/git/linux-stable$ git log -1 --pretty=format:"%ct" v4.4
    # 1452466892

    v44 = 1452466892
    for sl in range(1,rev_range+1):
        rev2 = rev + "." + str(sl)
        tag_range = rev1 + "..." + rev2
        gitcnt = "git rev-list --pretty=format:\"%ai\" " + tag_range
        gittag = "git log -1 --pretty=format:\"%ct\" " + rev2
        gitcnt_l = shlex.split(gitcnt)
        gittag_l = shlex.split(gittag)
        git_rev_list = Popen(gitcnt_l, stdout= PIPE, stderr= DEVNULL, shell=True)
        commit_cnt = get_commit_cnt(git_rev_list)
        if cumulative == 0:
            rev1 = rev2
    # if get back 0 then its an invalid revision number
        if commit_cnt:
            git_tag_date = Popen(gittag_l, stdout= PIPE, stderr= DEVNULL, shell=True)
            days = get_tag_days(git_tag_date, v44)
            print("%d %d %d" % (sl,days,commit_cnt))
        else:
            break

if __name__ == '__main__':
    a = commit_count()
    a.get_commit_cnt()
    a.get_tag_days()

