#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__copyright__ = "Chen Qin"
__date__ = "3/19/2020"
__version__   = 0.1

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


import os, re, sys, argparse
from datetime import datetime as dt
from subprocess import *

class GitCount(object):
   
     

   def get_commit_cnt(self,cmd):
      
      
      try:
         raw_counts = self.cmd.communicate()[0]
      except IndexError:
         raise IndexError("wrong git commmands")
      cnt = re.findall('[0-9]*-[0-9]*-[0-9]*', str(raw_counts))
      return len(cnt)

   
   def get_tag_days(self,base,cmd):
      self.cmd =cmd
      try:
         seconds = self.cmd.communicate()[0]

      except IndexError:
         raise IndexError("wrong git commands")
      return ((int(seconds)-base))//3600

   def get_base_time(self):

      git_time = self.cmd.communicate()[0]
      time = int(git_time)
      return time


   def get_parser(self):
      parser = argparse.ArgumentParser()
      parser.add_argument('--revision',required = True)
      parser.add_argument('--sublevel',default=1,type=int,help='how many sublevels you intend to count')
      parser.add_argument('--cumulative',default=0,type=bool)

   
      return parser

   def main(self):
      
      rev1 = rev
    
      gitbase = "git log -1 --pretty=format:\"%ct\"" + rev
      base_count = GitCount(gitbase)
      base_time = base_count.get_base_rev()

      for sl in range(1,rev_range + 1):
         rev2 = rev + "." + str(sl)
         gitcnt = "git rev-list --pretty=format:\"%ai\" " + rev1 + "..." +rev2
         gittag = "git log -1 --pretty=format:\"%ct\" " + rev2
         commit_count = GitCount(gitcnt)
         commits = commit_count.get_commit_cnt()

         if cumulative == 0:
            rev1 = rev2

         if commits:
            
            daytag_count = GitCount(gittag)
            days = daytag_count.get_tag_days(base_time)
            print("Recursion: %d %d $d" % (sl,days,commits))

         else:
            break
      

if __name__ == '__main__':
   gc = GitCount()
   parser = gc.get_parser()
   args = parser.parse_args()
   rev = args.revision
   rev_range = args.sublevel
   main()
   print("#sublevel commits %s stable fixes" % rev)
   print("lv hour bugs")
