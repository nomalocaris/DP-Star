#!/usr/bin/env python
# -*-coding:utf-8-*-
# Author: nomalocaris <nomalocaris.top>
"""
    progress bar module
"""
from __future__ import (absolute_import, unicode_literals)
import time


class ProgressBar(object):
    """the bar status for Progress
    """

    def __init__(self, _tot_pace, _state=None):
        """init the total num of progress
        """
        self._tot_pace = _tot_pace
        self._pstate = _state
        self._current_progress = 0
        self._state_start = r'%4d%% | '
        self._state_mid = ''
        self._state_end = ' | (pass : %8s | remain : %8s)'

        self._time_base = None
        self._time_pair = {'p': time.time(), 'n': time.time()}  # p means privous and n means now

    @staticmethod
    def _format_time(time_in_sec):
        """format the time in HH-MM-SS
        """
        if time_in_sec < 60:
            return str(time_in_sec) + ' s'
        else:
            mins = time_in_sec // 60
            secs = time_in_sec % 60
            if mins < 60:
                return str(mins) + ' m ' + str(secs) + ' s'
            else:
                hours = mins // 60
                mins %= 60
                return str(hours) + ' h' + str(mins) + ' m' + str(secs) + ' s'

    def update(self, pace):
        """cal and print the pace progress with every iter
        """
        # init time base
        if self._time_base is None:
            self._time_base = time.time()

        # init print state
        if self._pstate and not pace:
            print('\n mission : %s' % self._pstate)
            print('-' * 25)
        # record now time
        self._time_pair['n'] = time.time()
        # cal the progress bar
        new_progress = int(pace / self._tot_pace * 100)
        self._current_progress = new_progress + 1
        self._state_mid = '#' * (self._current_progress // 5)
        # cal pass time
        tpass = (self._time_pair['n'] - self._time_base)
        # cal remain time
        remain = tpass / self._current_progress * (100 - self._current_progress)

        # print msg
        print(
            ('\r' + self._state_start % self._current_progress) + self._state_mid +
            (self._state_end % (self._format_time(int(tpass)), self._format_time(int(remain)))),
            end='',
            flush=True
        )
        # update the previous time
        self._time_pair['p'] = self._time_pair['n']
        # when the pace satisfy the tot pace, print the end bar
        if self._pstate and pace >= self._tot_pace - 1:
            print('\n' + '-' * 25)


if __name__ == '__main__':
    p1 = ProgressBar(200, '测试用例1')
    for i in range(200):
        time.sleep(0.1)
        p1.update(i)


