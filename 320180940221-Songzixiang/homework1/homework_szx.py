#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2020 Wang Yichen,Song Zixiang All Rights Reserved
# Record all the commits starting at a git revision

__author__ = "Wang Yichen, Song Zixiang"
__sid__ = "320180940341,  320180940221"
__date__ = "3/19/2020"
__email__ = "ychwang2018@lzu.edu.cn, songzx18@lzu.edu.cn"

import os,re,sys
from subprocess import Popen,PIPE,DEVNULL
from datetime import datetime as dt

class revision():
    """
    a rivision is an object
    """
    def __init__(self,rev,rev2):
        """
        For each revision you need to provide the base version and the target revision
        Key arguments:
        rev -- the basic version
        rev2 -- the target
        """
        self.rev = rev
        self.rev2 = rev2
        self.repo = 'D:\git repository\linux-stable'

    def get_current_cnt(self):
        """
        Return the cnt of the target
        """
        target = self.rev +".."+self.rev2
        gitcnt = "git rev-list --pretty=format:\"%ai\" " + target
        git_rev_list = Popen(gitcnt, cwd=self.repo, stdout=PIPE, stderr=DEVNULL, shell=True)
        raw_counts = git_rev_list.communicate()[0]
        cnt = re.findall('[0-9]*-[0-9]*-[0-9]*', str(raw_counts))
        if len(cnt) == 0:
            raise TagNotExistError("There is something wrong with your input of tag:{0}..{1}"
                                   .format(self.rev, self.rev2))
        return len(cnt)

    def get_time(self,revision):
        """
        Return the time of the revision given
        """
        gittag = "git log -1 --pretty=format:\"%ct\" " + rev
        git_tag_date = Popen(gittag, cwd=self.repo, stdout=PIPE, stderr=DEVNULL, shell=True)
        seconds = int(git_tag_date.communicate()[0])
        return seconds

    def get_target_time(self):
        """
        Return the target revision's time
        """
        S_per_H = 3600
        H_per_D = 24
        second = self.get_time(self.rev2)-self.get_time(self.rev)
        day = second // (S_per_H*H_per_D)
        return day

def main():
    rev = sys.argv[1]
    revrange = int(sys.argv[2])
    if  not sys.argv[3] == "c":
        raise ValueError("You have an invalid in put on the 3rd param")

    for sl in range(1,revrange+1):
        try:
            print("commits: {0}, ".format(revision(rev,rev+"."+str(sl)).get_current_cnt()),end="  ")
        except TypeError:
            print("You have an invalid in put on the 1st param")
        try:
            print("time: {0}, ".format(revision(rev,rev+"."+str(sl)).get_target_time()),end="  ")
        except TypeError:
            print("You have an invalid in put on the 2nd param")

if __name__ == "__main__":
    main()


        
        
        
        
