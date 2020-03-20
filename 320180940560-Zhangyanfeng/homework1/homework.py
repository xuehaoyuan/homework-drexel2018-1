#!/usr/bin/env python3
# -*- coding:UTF-8 -*-

__author__ = "Yanfeng Zhang"
__copyright__ = "Lanzhou University, 2020"
__version__ = "2"
__email__ = "zhangyanfeng18@lzu.edu.com"



import os, re, sys, subprocess
from datetime import datetime as dt
import argparse


class ContentException(BaseException):
    collect = []
    def __str__(self):
        error = 'Find nothing! Please check the git and address again!'
        return error

class Log_Collect:
    def __init__(self):
        self.collect = []

        parser = argparse.ArgumentParser(description="parse")
        parser.add_argument('-v', '--version', type=str,default='v4.4', help='The starting version you want to start counting')
        parser.add_argument('-r', '--range', type=str,required=True, help='The revision number you want to query from the base version')
        parser.add_argument('-c', '--cumulative', type=bool,default=False, help='cumulative or not')
        args = parser.parse_args()

        self.rev = args.version
        cumulative = 0
        if (args.cumulative):
            cumulative = 1

        rev_range = int(args.range)
        self.get_base_time(self.rev)
        self.main(cumulative, rev_range)

    def get_base_time(self,v1):
        gettime = "git log -1 --pretty=format:\"%ct\" " + v1
        get_time = subprocess.Popen(gettime, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
        self.basetime = int(get_time.communicate()[0])

    def get_commit_cnt(self, git_cmd):
        cnt = 0
        try:
           raw_counts = git_cmd.communicate()[0]
           if raw_counts == 0:
               raise ContentException
        except ContentException as err:
            print(err)
            sys.exit(2)

     # if we request something that does not exist -> 0
        cnt = re.findall('[0-9]*-[0-9]*-[0-9]*', str(raw_counts))
        return len(cnt)

    def get_tag_days(self, git_cmd, base):
        t = 3600*24
        try:
            seconds = git_cmd.communicate()[0]
            if seconds == 0:
                raise ContentException
        except ContentException as err:
            print(err)
            sys.exit(2)
        return (int(seconds)-base)//t

    def main(self, cumulative, rev_range):

        rev1 = self.rev
        v44 = 1452466892
        for sl in range(1,rev_range+1):
            if sl < int(rev1[-1]):
                continue
            rev2 = self.rev[0:2] + "." + str(sl)
            print(rev2)
        
            gitcnt = "git rev-list --pretty=format:\"%ai\" " + rev1 + "..." + rev2
            gittag = "git log -1 --pretty=format:\"%ct\" " + rev2
            git_rev_list = subprocess.Popen(gitcnt, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
            commit_cnt = self.get_commit_cnt(git_rev_list)
            
            if cumulative == 0:
                rev1 = rev2
            # if get back 0 then its an invalid revision number
            if commit_cnt:
                git_tag_date = subprocess.Popen(gittag, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
                days = get_tag_days(git_tag_date, v44)
                print("%d %d %d" % (sl,days,commit_cnt))
            else:
                break

if __name__ == '__main__':
    collecter = Log_Collect()

