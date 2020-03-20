#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
"""
The function of this code is to get the logs of linux_stable and print them.

"""
__author__ = "Shuhai Cao"
__copyright__ = "Shuhai Cao, Lanzhou University, 2020"
__license__ = "GPL V2 or later"
__credits__ = ["Shuhai Cao"]
__version__ = "5"
__email__ = "caoshh18@lzu.edu.com"
__status__ = "Experimental"


import re, sys
from subprocess import Popen, PIPE, DEVNULL
from argparse import ArgumentParser as AP

class CommunicateError(Exception):
    def __init__(self):
        pass
    def __str__(self):
        warning = "You did not get any thing, please check your git."
        return warning
    
class DatePrinter():
    def __init__(self):
        self.parser = self.get_args()
        self.preprocess(self.parser)
        self.get_base_time(self.rev1)
        
        self.main(self.parser)

    #Gets the version number entered by the user.
    def get_args(self):
        parser = AP(description="Collecting the kernel version you input and output all of the dates of commit.")
        h = """You should input the version as three parts and separate them with SPACE.
        And if you input 'c' as the end of input, the result will be cumulative."""
        parser.add_argument("-v", "--version", required=True, nargs="+", help=h)
        return parser

    #Preprocess and judge the parameters.
    def preprocess(self, prr):
        args = prr.parse_args()
        version = " ".join(args.version)
        level_list = version.split(" ")
        self.rev1 = level_list[0]
        self.rev_range = int(level_list[1])
        length = len(level_list)

        #Determine whether cumulative results need to be printed.
        if length == 3:
            if level_list[2] == "c":
                self.cumulative = 1
            else:
                print("Do not know what you mean with %s" % level_list[2])
                sys.exit(-1)
        elif length == 2:
            self.cumulative = 0
        else:
            print("You must input at least 2 arguments(entire version number).")
            sys.exit(-1)

    #Gets the number of commits.
    def get_commit_cnt(self, git_cmd1):
        try:
            raw_counts = git_cmd1.communicate()[0]
            if raw_counts == 0:
                raise CommunicateError
        except CommunicateError as err:
            print(err)
            sys.exit(-1)
        cnt = re.findall("[0-9]*-[0-9]*-[0-9]*", str(raw_counts))
        return len(cnt)

    #Get the Magic number of current version.
    def get_base_time(self, prev):
        gettime = ["git", "log", "-1", "--pretty=format:\"%ct\"", prev]
        get_time = Popen(gettime, stdout=PIPE, stderr=DEVNULL, shell=True)
        self.base_time = int(eval(get_time.communicate()[0].decode("utf-8")))

    #Get the time of each commit and convert it to days.
    def get_tag_days(self, git_cmd2, base):
        try:
            seconds = int(eval(git_cmd2.communicate()[0].decode("utf-8")))
            if seconds == 0:
                raise CommunicateError
        except CommunicateError as err:
            print(err)
            sys.exit(-1)
        SecPerHour = 3600
        return (seconds-base)//(SecPerHour*24)

    #The function used to get the output of each line.
    def output(self, cnt, tag, base_time):
        git_rev_list = Popen(cnt, stdout=PIPE, stderr=DEVNULL, shell=True)
        self.commit_cnt = self.get_commit_cnt(git_rev_list)
        git_tag_date = Popen(tag, stdout=PIPE, stderr=DEVNULL, shell=True)
        self.days = self.get_tag_days(git_tag_date, self.base_time)

    #Main function.
    def main(self,parser):
        #Print the header of the table.
        print("#sublevel commits {0} stable fixes".format(self.rev1))
        print("{:<6} {:<7} {:<8}".format("lv", "hour", "bugs"))

        #Print line by line in the given output format.
        cumu_commit_cnt = 0
        for sl in range(1, self.rev_range+1):
            rev2 = self.rev1 + "." + str(sl)
            output_range = self.rev1 + "..." + rev2
            gitcnt = ["git", "rev-list", "--pretty=format:\"%ai\"", output_range]
            gittag = ["git", "log", "-1", "--pretty=format:\"%ct\"", rev2]
            self.output(gitcnt, gittag, self.base_time)
            if self.cumulative == 0:
                print("{:<6} {:<7} {:<8}".format(sl, self.days, self.commit_cnt))
            else:
                cumu_commit_cnt += self.commit_cnt
                print("{:<6} {:<7} {:<8}".format(sl, self.days, cumu_commit_cnt))

if __name__ == "__main__":
    DatePrinter()
