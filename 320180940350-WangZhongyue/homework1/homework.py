#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# get the commit count per sublevel pointwise or cumulative (c)

# arguments is the tag as displayed by git tag and the number

# of sublevels to be counted. If count is out of range for a

# specific sublevel it will terminate the loop

'''

Name:Zhongyue Wang
Student ID:320180940350

'''



import os, re, sys, subprocess

from datetime import datetime as dt

from suprocess import Popen, DEVNULL



class Check(Check_Exception):
 
    def get_commit_cnt(self, git_cmd):
        cnt = 0
        try:
            raw_counts = git_cmd.communicate()[0]
            # if we request something that does not exist -> 0
            if raw_counts == 0:
                raise Check

        except Check as error_occurred:
            print(error_occurred)
        cnt = re.findall('[0-9]*-[0-9]*-[0-9]*', str(raw_counts))

        return len(cnt)
    
    
    def __str__(self):
        exception_prompt = 'There was an error here, please review your content'
        return exception_prompt
    
    def get_tag_days(self, git_cmd, base):
   
        try:
           seconds = git_cmd.communicate()[0]
           if seconds == 0:
               raise Check

        except Check as error_occurred:
            print(error_occurred)
            time = 3600
            return ((int(seconds)-base))//time
        
class Collect:

    def __init__(self, args):
        try:
            if args[2]:
                pass
            
        except:
            print('There are invalid arguments here')

        self.rev = args[1]
        cumulative = 0
        if len(args) == 4:
            if (args[3] == "c"):
                cumulative = 1

            else:
                print("An error occurred in %s" % args[3])
        rev_range = int(args[2])
        self.git(cumulative, rev_range)        
        
    def git(self, cumulative, rev_range):
        com = args[0]
        v44 = 1452466892
        for sl in range(1,rev_range+1):
            if sl < int(com[-1]):
                continue

            com1 = self.rev[0:2] + "." + str(sl)

            print(com1)

            gitcnt = "git rev-list --pretty=format:\"%ai\" " + com + "..." + com1

            gittag = "git log -1 --pretty=format:\"%ct\" " + com1

            git_rev_list = subprocess.Popen(gitcnt, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)

            commit_cnt = self.get_commit_cnt(git_rev_list)

            if cumulative == 0:
                com = com1
                
            if commit_cnt:

                git_tag_date = subprocess.Popen(gittag, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)

                days = self.get_tag_days(git_tag_date, v44)

                print("%d %d %d" % (sl,days,commit_cnt))

            else:

                break


if __name__ == '__main__':

    collecter = Collect(sys.argv)

