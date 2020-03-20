#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#__author__:ZhangYi

import os, re, sys, subprocess,argparse
from datetime import datetime as dt

parser = argparse.ArgumentParser()
parser.add_argument("accumulation")
parser.add_argument("revision", help="revision")
parser.add_argument("range",type=int, help="get the input number")
args = parser.parse_args()

class commit_collect():
    def init(self,git_cmd,base):
        self.git_cmd = git_cmd
        self.base = base
    
    def get_commit_cnt(self,git_cmd):
        raw_counts = self.git_cmd.communicate()[0]
        #git_rev_list = subprocess.Popen(self.git_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
        # if we request something that does not exist -> 0]
        cnt = re.findall('[0-9]*-[0-9]*-[0-9]*', str(raw_counts))
        if len(cnt) != 0:
            return len(cnt)

    def get_tag_days(self,git_cmd, base):
        seconds = self.git_cmd.communicate()[0]
        SecPerHour = 3600
        return ((int(seconds)-self.base))//SecPerHour

         
    # get dates of all commits - unsorted    
    rev = sys.argv[1]
    cumulative = 0
    if len(sys.argv) == 4:
        if (sys.argv[3] == "c"):
            cumulative = 1
        else:
            print("Dont know what you mean with %s" % sys.argv[3])
            sys.exit(-1)
    rev_range = int(sys.argv[2])

    # setup and fill in the table
    print("#sublevel commits %s stable fixes" % rev)
    print("lv hour bugs") #tag for R data.frame
    rev1 = rev
    # base time of v4.1 and v4.4 as ref base
    # fix this to extract the time of the base commit
    # from git ! 
    # hofrat@Debian:~/git/linux-stable$ git log -1 --pretty=format:"%ct" v4.4
    # 1452466892
    
    def start(self, cumulative, rev_range):
        v44 = 1452466892
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


