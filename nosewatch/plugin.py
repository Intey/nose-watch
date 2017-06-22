import sys
import os

from nose.plugins import Plugin
from subprocess import Popen


class WatchPlugin(Plugin):
    """
    Plugin that use watchdog for continuous tests run.
    """
    name = 'watch'
    is_watching = False
    sys = sys

    def call(self, args):
        Popen(args).wait()

    def finalize(self, result):
        argv = list(self.sys.argv)
        argv.remove('--with-watch')
        watchcmd = 'clear && ' + ' '.join(argv)
        call_args = ['watchmedo', 'shell-command', 
                     '-c', watchcmd, '-R', 
                     '-p', '*.py',
                     '-W', os.path.abspath(os.path.curdir)]
        try:
            self.call(call_args)
        except KeyboardInterrupt:
            self.sys.stdout.write('\nStopped\n')
