import os, re, sys, subprocess, time
import argparse


def write(msg):
    with open('errors.log', 'w') as f:
        f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' : ' + msg + '\n')


class Exception(BaseException):
    collect = []

    def __str__(self):
        error = 'Find nothing! Please check the git and address again!'
        return error


class Log_Collect:
    def __init__(self):
        self.collect = []

        parser = argparse.ArgumentParser(description="parse")
        parser.add_argument('-v', '--version', type=str, default='v4.4',
                            help='The starting version you want to start counting')
        parser.add_argument('-r', '--range', type=str, required=True,
                            help='The revision number you want to query from the base version')
        parser.add_argument('-c', '--cumulative', type=bool, default=False, help='cumulative or not')
        args = parser.parse_args()

        self.rev = args.version
        cumulative = 0
        if (args.cumulative):
            cumulative = 1

        rev_range = int(args.range)
        self.get_base_time(self.rev)
        self.main(cumulative, rev_range)

    def get_base_time(self, v1):
        gettime = "git log -1 --pretty=format:\"%ct\" " + v1
        get_time = subprocess.Popen(gettime, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
        self.basetime = int(get_time.communicate()[0])

    def get_commit_cnt(self, git_cmd):
        cnt = 0
        try:
            raw_counts = git_cmd.communicate()[0]
            if raw_counts == 0:
                raise Exception
        except Exception as err:
            print(err)
            sys.exit(2)
        cnt = re.findall('[0-9]*-[0-9]*-[0-9]*', str(raw_counts))
        return len(cnt)

    def get_tag_days(self, git_cmd, base):
        t = 3600 * 24
        try:
            seconds = git_cmd.communicate()[0]
            if seconds == 0:
                raise Exception
        except Exception as err:
            print(err)
            sys.exit(2)
        return (int(seconds) - base) // t

    def git(self, cumulative, range):

        rev1 = self.rev
        v44 = 1452466892
        for sl in range(1, range + 1):
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
                days = Log_Collect.get_tag_days(git_tag_date, v44)
                print("%d %d %d" % (sl, days, commit_cnt))
            else:
                break


if __name__ == '__main__':
    collecter = Log_Collect()