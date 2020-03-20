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
'''
This is a tool that could help users grab some records from git bash/commandline,
such as git log, git daytime and git commands.
And there are three arguments, e.g.  python homework.py  -v=4.4 -r=3 -c=True
-v The starting version you want to start counting
-r The revision number you want to query from the base version
-c (bool)cumulative or not
'''

__author__ = 'Bofei Zhang'
__email__ = 'zhangbf18@lzu.edu.cn'
__copyright__ = 'Copyright 2020, Lanzhou University'
__version__ = '0.1'
__license__ = 'GPL V3'
__maintainer__ = 'Bofei Zhang'
__status__ = 'Experimental'

import os, re, sys, subprocess
from datetime import datetime as dt
import argparse
import doctest


class ExceptionMonitor(BaseException):

    def __str__(self):
        tip = 'OMG! Recheck your basic element such as git configuration.'
        return tip


class Git_log_grabber:
    '''
    This is a docstring.
    Here we want to have a class to grab the log form git.
    There are four methods exactly.
    '''

    def __init__(self):
        '''
        Just a initialize method.
        there are some required argument.
        '''
        parse = argparse.ArgumentParser(description='parse')
        parse.add_argument('-v', '--version', type=str, default='v4.4', help='version you want to parse')
        parse.add_argument('-r', '--range', type=str, default=True,help='sublevel counter')
        parse.add_argument('-c', '--cumulative', type=bool, default=False,help='choose cumulative or not')
        args = parse.parse_args()

        self.rev = args.revision()

        try:
            rev_range = int(args.rev_range)
        except (ValueError, UnboundLocalError):
            err = 'Please let -r be a integer.'
            print(err)
        if args.cumulative == "c":
            cumulative = 1
        else:
            cumulative = 0
            print("Dont know what you mean with %s" % args.cumulative)
            sys.exit(-1)


        self.get_log(cumulative, rev_range)


    def get_commit_cnt(self, git_cmd):
        # cnt = 0
        # global raw_counts
        try:
            raw_counts = git_cmd.communicate()[0]
            if raw_counts == 0:
                raise ExceptionMonitor
        except ExceptionMonitor as err:
            print(err)
        # if we request something that does not exist -> 0
        cnt = re.findall('[0-9]*-[0-9]*-[0-9]*', str(raw_counts))
        return len(cnt)

    def get_tag_days(self, git_cmd, base):
        # global sec_one_hour, seconds
        try:
            seconds = git_cmd.communicate()[0]
            sec_one_hour = 3600
            if seconds == 0:
                raise ExceptionMonitor
        except ExceptionMonitor as err:
            print(err)
            return (int(seconds) - base) // sec_one_hour

    def get_log(self,cumulative, rev_range):

        print("#sublevel commits %s stable fixes" % self.rev)
        print("lv hour bugs")  # tag for R data.frame
        rev1 = self.rev



    # base time of v4.1 and v4.4 as ref base
    # fix this to extract the time of the base commit
    # from git !
    #
    # hofrat@Debian:~/git/linux-stable$ git log -1 --pretty=format:"%ct" v4.4
    # 1452466892
        v44 = 1452466892

        for sl in range(1, rev_range + 1):
            rev2 = self.rev + "." + str(sl)
            gitcnt = "git rev-list --pretty=format:\"%ai\" " + rev1 + "..." + rev2
            gittag = "git log -1 --pretty=format:\"%ct\" " + rev2
            git_rev_list = subprocess.Popen(
                gitcnt,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                shell=True)
            commit_cnt = self.get_commit_cnt(git_rev_list)
            if cumulative == 0:
                rev1 = rev2
            # if get back 0 then its an invalid revision number
            if commit_cnt:
                git_tag_date = subprocess.Popen(
                    gittag,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    shell=True)
                days = self.get_tag_days(git_tag_date, v44)
                print("%d %d %d" % (sl, days, commit_cnt))
            else:
                break

if __name__ == '__main__':
    gitgrab = Git_log_grabber()