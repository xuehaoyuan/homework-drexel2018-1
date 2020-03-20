import sys
from subprocess import Popen

class GitCnt(object):

    def __init__(self,command):
        self.cmd = Popen (command, stdout=PIPE, stderr=DEVNULL, shell=True)

    def get_commit_cnt(self):

        cnt = 0

        try:
            raw_counts = self.cmd.communicate()[0]
        except IndexError:
            raise IndexError("Git command error")
        # if we request something that does not exist -> 0

        cnt = re.findall('[0-9]*-[0-9]*-[0-9]*', str(raw_counts))
        return len(cnt)

    def get_tag_days(self, base):

        try:
            seconds = self.cmd.communicate()[0]
        except IndexError:
            raise IndexError("Git command error")

        return (int(seconds) - base) // 3600

    def get_base_rev(self):

        git_time = self.cmd.communicate()[0]
        time = str(git_time.decode('UTF-8')).split('v')[0]
        return int(time)

def get_parser():
    pass

def main():

    parser = get_parser()
    args = parser.parser_args()
    rev =args.revision
    rev_range = args.sublevel
    cumulative = args.cumulative

    rev1 = rev

    for sl in range(1,rev_range+1):

        rev2 = rev + "." + str(sl)

        gitcnt = "git rev-list --pretty=format:\"%ai\" " + rev1 + "..." + rev2
        gittag = "git log -1 --pretty=format:\"%ct\" " + rev2

        commit_cnt = GitCnt(gitcnt)
        commits = commit_cnt.get_commit_cnt()

        if cumulative == 0:
            rev1 = rev2

        if commit_cnt:

            days_cnt = GitCnt(gittag)
            days = days_cnt.get_commit_cnt()
            print("%d %d %d" % (sl,days,commit_cnt))

        else:
            break

if __name__ == '__main__':
    main()