#!/usr/bin/python
#
# file_descriptor: tests that the correct number of file descriptors are open in the command spawned by the shell
#
#
# sleep in the background
#

import sys, imp, atexit

sys.path.append("/home/courses/cs3214/software/pexpect-dpty/")
import pexpect, shellio, signal, time, os, re, proc_check


# Ensure the shell process is terminated
def force_shell_termination(shell_process):
    c.close(force=True)


# pulling in the regular expression and other definitions
definitions_scriptname = sys.argv[1]

def_module = imp.load_source('', definitions_scriptname)
logfile = None
if hasattr(def_module, 'logfile'):
    logfile = def_module.logfile

# spawn an instance of the shell
c = pexpect.spawn(def_module.shell, drainpty=True, logfile=logfile)
atexit.register(force_shell_termination, shell_process=c)

# set timeout for all following 'expect*' calls to 2 seconds
c.timeout = 2

# ensure that shell prints expected prompt at startup
assert c.expect(def_module.prompt) == 0, "Shell did not print expected prompt"

c.sendline("sleep 30 &")

# Used to get the jobid and pid of the sleep process that is printed when a background task is run
# This should match the regular expression provided in eshoutput.py for bgjob_regex
# The default one should be of the form '[jobid] process_group_id'
(jobid, pid) = shellio.parse_regular_expression(c, def_module.bgjob_regex)


# now use the pid to check the file descriptors
def assert_correct_fds(pid, message):
    '''Checks that file descriptors are not leaked into
    the child.'''

    time.sleep(0.5)
    fds = sorted(os.listdir('/proc/{0}/fd'.format(pid)))
    tty = True
    print fds
    if '3' in fds:
        tty = os.path.samefile('/proc/{0}/fd/3'.format(pid), '/dev/tty')

    if not (fds == list('012') or (fds == list('0123') and tty)):
        raise Exception('File descriptors leaked into child! Remember to close() all of the pipes and IO redir file descriptors')

assert_correct_fds(pid,"If any extra opened file descriptors are not closed before the exec then this check will fail.")


# exit the shell
c.sendline("exit")
assert c.expect("exit\r\n") == 0, "Shell output extraneous characters"

shellio.success()