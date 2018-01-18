#!/usr/bin/python
#
# cmdfail-test: tests that the shell properly terminates any forked
# children and returns to the prompt if the user types in a command
# that is neither a built-in nor a Unix command.
# 
# Requires the following commands to be implemented
# or otherwise usable:
#
#	exit
#

import sys, imp, atexit
sys.path.append("/home/courses/cs3214/software/pexpect-dpty/");
import pexpect, shellio, signal, time, os, re, proc_check


#Ensure the shell process is terminated
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

# ensure that the shell prints the expected prompt
assert c.expect(def_module.prompt) == 0, "Shell did not print expected prompt"



# run a non-existent command
c.sendline("this_command_does_not_exist")

time.sleep(2)
# this should fail somehow and not leave any children behind
proc_check.count_active_children(c, 0)

# eventually, the shell should go back to the prompt
assert c.expect(def_module.prompt) == 0, "Shell did not print expected prompt"

# end the shell program by sending it an end-of-file character
c.sendline("exit");

# ensure that no extra characters are output after exiting
assert c.expect_exact("exit\r\n") == 0, "Shell output extraneous characters"


# the test was successful
shellio.success()
