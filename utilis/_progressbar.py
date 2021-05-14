#!/usr/bin/env python
# -*-coding:utf-8-*-
# Author: nomalocaris <nomalocaris.top>
""""""
from __future__ import (absolute_import, unicode_literals)
import time


class ProgressBar(object):
    """the bar status for Progress
    """

    def __init__(self, _tot, _state=None):
        """init the total num of progress
        """
        self._tot = _tot
        self._pstate = _state
        self._current_progress = 0
        self._state_start = r'%4d%% | '
        self._state_mid = ''
        self._state_end = ' | (pass : %8s | remain : %8s)'

        self._time_base = None
        self._time_pair = {'p': time.time(), 'n': time.time()}

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
        if self._time_base is None:
            self._time_base = time.time()

        if self._pstate and not pace:
            print('\n mission : %s' % self._pstate)
            print('-' * 25)

        self._time_pair['n'] = time.time()

        new_progress = int(pace / self._tot * 100)
        self._current_progress = new_progress + 1
        self._state_mid = '#' * (self._current_progress // 5)

        tpass = (self._time_pair['n'] - self._time_base)
        remain = tpass / self._current_progress * (100 - self._current_progress)

        print(
            ('\r' + self._state_start % self._current_progress) + self._state_mid +
            (self._state_end % (self._format_time(int(tpass)), self._format_time(int(remain)))),
            end='',
            flush=True
        )

        self._time_pair['p'] = self._time_pair['n']

        if self._pstate and pace >= self._tot - 1:
            print('\n' + '-' * 25)


if __name__ == '__main__':
    from tqdm import tqdm
    p1 = ProgressBar(200, '测试用例1')
    for i in range(200):
        time.sleep(0.1)
        p1.update(i)
    for i in tqdm(range(100)):
        time.sleep(0.1)

