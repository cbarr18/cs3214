#!/usr/bin/python
#
# running_a_background_task: tests the shell can execute a command in the background
#
#
# sleep, and background execution
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

# run program sleep in the background
c.sendline("sleep 30 &")

# Used to get the jobid and pid of the sleep process that is printed when a background task is run
# This should match the regular expression provided in eshoutput.py for bgjob_regex
# The default one should be of the form '[jobid] process_group_id'
(jobid, pid) = shellio.parse_regular_expression(c, def_module.bgjob_regex)

# Expect that the prompt is printed within 2 seconds of running the sleep command in the background
# This is more than enough time for any reasonable implementation that is running a background job
assert c.expect(def_module.prompt) == 0, "Shell did not print expected prompt after running a sleep command in the " \
                                         "background "

# Ensure that sleep is running now in the background, and is not
# the foreground process.
assert not proc_check.check_pid_fgpgrp(pid), \
    'Error: sleep is in the foreground process group when it should be in the background'

# sleep should still be running in the background at this point as it has not been 30 seconds
assert proc_check.check_pid_status(pid, 'S'), 'Error: sleep is not running when it should be running in the background'

# exit the shell
c.sendline("exit")
assert c.expect("exit\r\n") == 0, "Shell output extraneous characters"

shellio.success()
