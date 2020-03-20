#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 get the commit count per sublevel pointwise or cumulative (c)
 arguments is the tag as displayed by git tag and the number
 of sublevels to be counted. If count is out of range for a
 specific sublevel it will terminate the loop
"""
__copyright__ = "Lanzhou University, 2020"
__Author__ = "Wang Yancong, Liang Yuanbo in T4"
__licences__ = "GPL V2 or later"
__version__ = "0.1"
__email__ = "wangyc18@lzu.edu.cn; liangyuanbo18@lzu.edu.cn"
__status__ = "Experimental"


import re, sys
import argparse
from subprocess import Popen, PIPE, DEVNULL


class ContentNotFountErr(Exception):
    pass


class CommitCount:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("revision", help='revision number, e.g. v4.4')
        parser.add_argument("sublevel", type=int, help='sublevel range')
        parser.add_argument("-c", type=str)
        args = parser.parse_args()
        self.rev = args.revision
        self.rev_range = args.sublevel
        self.cumulative = 0

        # setup and fill in the table
        if args.c == 'c':
            self.cumulative = 1
        elif args.c:
            err = "Dont know what you mean with {}".format(args.c)
            print(err)
            sys.exit(-1)

        print("#sublevel commits %s stable fixes" % self.rev)
        print("lv hour bugs")  # tag for R data.frame
        self.get_cnt()

    def get_commit_cnt(self, git_cmd):
        try:
            raw_counts = git_cmd.communicate()[0]
            if raw_counts == 0:
                raise ContentNotFountErr
        # if we request something that does not exist -> 0
        except ContentNotFountErr:
            print("The request does not exist")

        cnt = re.findall('[0-9]*-[0-9]*-[0-9]*', str(raw_counts))
        return len(cnt)

    # get dates of all commits - unsorted
    def get_tag_days(self, git_cmd, base):
        try:
            seconds = git_cmd.communicate()[0]
            if seconds == 0:
                raise ContentNotFountErr
        except ContentNotFountErr:
            print("The request does not exist")
        SecPerHour = 3600
        return (int(seconds)-base)//SecPerHour


    def get_cnt(self):
        rev1 = self.rev
        v4_4 = 1452466892
        for sl in range(1, self.rev_range+1):
            rev2 = self.rev + "." + str(sl)
            gitcnt = "git rev-list --pretty=format:\"%ai\" {0}...{1}".format(rev1, rev2)
            gittag = "git log -1 --pretty=format:\"%ct\" {0}".format(rev2)
            git_rev_list = Popen(gitcnt, stdout=PIPE, stderr=DEVNULL, shell=True)
            commit_cnt = self.get_commit_cnt(git_rev_list)
            if self.cumulative == 0:
                rev1 = rev2
            # if get back 0 then its an invalid revision number
            if commit_cnt:
                git_tag_date = Popen(gittag, stdout=PIPE, stderr=DEVNULL, shell=True)
                days = self.get_tag_days(git_tag_date, v4_4)
                print("%d %d %d" % (sl, days, commit_cnt))
            else:
                break


if __name__ == "__main__":
    a = CommitCount()

