# -*- coding: utf-8 -*-
# Copyright: 2009 Nadia Alramli
# License: BSD
#
# from: http://nadiana.com/animated-terminal-progress-bar-in-python
#

"""Draws an animated terminal progress bar
Usage:
    p = ProgressBar("blue")
    p.render(percentage, message)

    from progressbar import ProgressBar
    import time
    p = ProgressBar('green', width=20, block='▣', empty='□')
    for i in range(101):
        p.render(i, 'step %s\nProcessing...\nDescription: write something.' % i)
        time.sleep(0.1)
"""
 
import terminal
import sys
 
class ProgressBar(object):
    """Terminal progress bar class"""
    TEMPLATE = '%(percent)3s%% %(color)s[%(progress)s%(normal)s%(empty)s] %(message)s\n'
    PADDING = 7
 
    def __init__(self, color=None, width=None, block='█', empty=' ', min=0, max=100):
        """
        color -- color name (BLUE GREEN CYAN RED MAGENTA YELLOW WHITE BLACK)
        width -- bar width (optinal)
        block -- progress display character (default '█')
        empty -- bar display character (default ' ')
        """
        if color:
            self.color = getattr(terminal, color.upper())
        else:
            self.color = ''
        if terminal.COLUMNS:
            if width and width < terminal.COLUMNS - self.PADDING:
                self.width = width
            else:
                # Adjust to the width of the terminal
                self.width = terminal.COLUMNS - self.PADDING
        else:
            self.width = 30
        self.block = block
        self.empty = empty
        self.progress = None
        self.lines = 0
        self.min = min
        self.max = max
        self.value = 0

    def step(self, message=''):
        self.value += 1.0
        self.render(int(100.0*( abs(self.value-self.min) )/( abs(self.max-self.min) ) ), message)

    def update(self, value, message=''):
        self.value = value
        self.render(int(100.0*( abs(self.value-self.min) )/( abs(self.max-self.min) ) ), message)
 
    def render(self, percent, message = ''):
        """Print the progress bar
        percent -- the progress percentage %
        message -- message string (optional)
        """
        inline_msg_len = 0
        if message:
            # The length of the first line in the message
            inline_msg_len = len(message.splitlines()[0])
        if inline_msg_len + self.width + self.PADDING > terminal.COLUMNS:
            # The message is too long to fit in one line.
            # Adjust the bar width to fit.
            if terminal.COLUMNS:
                bar_width = terminal.COLUMNS - inline_msg_len -self.PADDING
            else:
                bar_width = self.width
        else:
            bar_width = self.width
 
        # Check if render is called for the first time
        if self.progress != None:
            self.clear()
        self.progress = (bar_width * percent) / 100
        data = self.TEMPLATE % {
            'percent': percent,
            'color': self.color,
            'progress': self.block * self.progress,
            'normal': terminal.NORMAL,
            'empty': self.empty * (bar_width - self.progress),
            'message': message
        }
        sys.stdout.write(data)
        sys.stdout.flush()
        # The number of lines printed
        self.lines = len(data.splitlines())
 
    def clear(self):
        """Clear all printed lines"""
        sys.stdout.write(
            self.lines * (terminal.UP + terminal.BOL + terminal.CLEAR_EOL)
        )

if __name__ == '__main__':
    import time
    nsteps = 50
    p = ProgressBar('blue', width=20, block='▣', empty='□', max=nsteps)
    for i in xrange(nsteps):
        p.step('step %s\nProcessing...\nDescription: write something.' % i)
        time.sleep(0.1)
    print 'Done.'

