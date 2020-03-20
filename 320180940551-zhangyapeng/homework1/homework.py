#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "ZhangYapeng"
__id__ = "320180940551"
__email__ = "ypzhang2018@lzu.edu.cn"
__copyright__ = 'ZhangYapeng only reserved'

import os, re, sys, subprocess, argparse
from datetime import datetime as dt


class get_dates_commit():
	
	def __init__(self,rev,rev1):
		self.rev = rev
		self.rev1 = rev1
		self.repository = 'F:\git_repository\linux-stable'	
	
	def get_parse(self):
		parser = argparse.ArgumentParser(description='get_parser')
		parser.add_argument('-sv','--starting_version', type=str,default='v4.4',help='The starting version to start counting')
		parser.add_argument('-rn','--revison_number', type=str,required=True,help='The revision number to query from the base version')
		parser.add_argument('-wc','--whether_cumulative', type=bool,default=False,help='whether to cumulative')	
		return parser
  
	def get_commit_cnt(self):
		gitcnt = "git rev-list --pretty=format:\"%ai\" " + self.rev +".."+self.rev1
		git_rev_list = subprocess.Popen(['ubuntu',gitcnt],cwd=self.repository,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,shell=True)
		raw_counts = git_cmd.communicate()[0]
		cnt = re.findall('[0-9]*-[0-9]*-[0-9]*', str(raw_counts))
		return len(cnt)

	def get_tag_days(self, git_cmd, base):
		seconds = git_cmd.communicate()[0]
		return ((int(seconds)-base))//3600
	
def main():
	rev = sys.argv[1]
	rev_range = int(sys.argv[2])
	try:
		if len(sys.argv) == 4:
			if (sys.argv[3] == "c"):
				cumulative = 1
			else:
				print("Dont know what you mean with %s" % sys.argv[3])
				sys.exit(-1)               
	except:
		pass
	 
	for sl in range(1,rev_range+1):
		try:
			print("commits: {0}, ".format(get_dates_commit(rev,rev+"."+str(sl)).get_commit_cnt()))
		except TypeError:
			print("You have an invalid input on the 1st param")
		try:
			print("time: {0}, ".format(get_dates_commit(rev,rev+"."+str(sl)).get_tag_days()))
		except TypeError:
			print("You have an invalid input on the 2nd param")

if __name__ == "__main__":
	main()

