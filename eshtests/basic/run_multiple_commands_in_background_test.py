#!/usr/bin/python
#
# run_multiple_commands_in_background_test: tests that multiple commands separated by a & are both run
# 
# Test that the sleep and echo commands are both run and in the correct order
#
# Requires the following commands to be implemented
# or otherwise usable:
#
#     running a command in the background
#     running multiple commands
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

# ensure that shell prints expected prompt
assert c.expect(def_module.prompt) == 0, "Shell did not print expected prompt before running any commands"

# run a command line with multiple pipelines of a single command
c.sendline("sleep 20 & echo bye")

assert c.expect("bye") == 0, "The shell did not print bye in a reasonable time after the command was sent"

# check the prompt prints
assert c.expect(def_module.prompt) == 0, "Shell did not print expected prompt after the command was sent"

# exit the shell
c.sendline("exit")
assert c.expect_exact("exit\r\n") == 0, "Shell output extraneous characters"

shellio.success()
