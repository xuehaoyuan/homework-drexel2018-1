#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# get the commit count per sublevel pointwise or cumulative (c)
# arguments is the tag as displayed by git tag and the number
# of sublevels to be counted. If count is out of range for a 
# specific sublevel it will terminate the loop
#
# no proper header in this file 
# no legal/copyright ...OMG !
# 
# things to cleanup:
# restructure the code - use of functions 
# error handling ...where is the try..except ?
# argument handling: you can do better right ?
# documentation: once you understand it - fix the docs !
# transform it into a class rather than just functions !
"""
__Author__ = Nicolas (Hofart)
__Vesion__ = 0.01
__License__ = GPL V3
__Coptright__ = @2020 Qihang Guan LanZhou University
__Status__ =  Expermental

"""

import os, sys, subprocess
from datetime import datetime as dt
from re import findall

class Exception(BaseException):
      def __str__(self):
         wrong = 'Please check your git and the address!'
         return wrong     

class collect():
   def __init__(self,argv[]):
      try:
         if argv[3]:
            pass
      except IndexError:
         print("3 or more argument please")
         sys.exit(1)
      rev = sys.argv[1]
      cumulative = 0
      if len(sys.argv) == 4:
      if (sys.argv[3] == "c"):
      cumulative = 1
      else:
         print("Dont know what you mean with %s" % sys.argv[3])
         sys.exit(-1)
      rev_range = int(sys.argv[2]) 
   def get_commit_cnt(git_cmd):
      cnt = 0
      raw_counts = git_cmd.communicate()[0]
   # if we request something that does not exist -> 0
      cnt = findall('[0-9]*-[0-9]*-[0-9]*', str(raw_counts))
      return len(cnt)

   def get_tag_days(git_cmd, base):
      seconds = git_cmd.communicate()[0]
      return ((int(seconds)-base))//3600

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
   def ver(self,cumulative,rev_range)
   rev1 = self.rev
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
            
if __name__ == '__main__':
    collecter = git_collect(sys.argv)
"""
Title: To get the commit count per sublevel pointwise or cumulative (c)
Requirements:
Rq1:get get all dates of commits without sort.
Rq1:fill them in table."""
