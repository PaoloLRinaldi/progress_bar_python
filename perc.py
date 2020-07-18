import time
import sys
if 'numpy' in sys.modules:
	import numpy as np

class Perc:
    def __init__(self, vmax, verbose=3, inline=True, showbar=True, disable=False):
        if type(vmax) == int:
            self._vmax = vmax
        else:
            self._vmax = len(vmax)
            self._tomanage = iter(vmax)
        self._it = 0
        self._perc = -1
        self._times = [time.time()]
        self._verbose = verbose
        self._inline = inline
        self._showbar = showbar
        self._progsz = 20
        self._passedits = []
        self._disable = disable


    def __new__(cls, *args, **kwargs):
        return super(Perc, cls).__new__(cls)

    def tomins(self, secs):
        '''
          Seconds to minutes format.
        '''
        secs = int(round(secs))
        mins = secs // 60
        secs = secs % 60
        if secs < 10:
            return '{}:0{}'.format(mins, secs)
        return '{}:{}'.format(mins, secs)
    
    def next(self, it = None):
        '''
          Update to next iteration.
        '''
        if self._disable:
            return

        if it != None:
            self._it = it
        self._it += 1

        current_perc = self._it * 100 // self._vmax
        if current_perc != self._perc:
            if self._inline:
                print('\r', end='')
            if self._showbar:
                prog = int((self._it / self._vmax) * self._progsz)
                print('[' + '=' * prog, end='')
                if (prog != self._progsz):
                    print('>' + '.' * (self._progsz - prog - 1), end='')
                print('] ', end='')

            print('{}%'.format(current_perc), end=' ')
            if self._verbose > 0:
            # Print time elapsed from last percentace step, current iteration and iteraztions per second
                self._times.append(time.time())
                self._passedits.append(self._it)

                if len(self._times) > 2:
                    step = self._times[-1] - self._times[-2]
                    itspersec = (self._passedits[-1] - self._passedits[-2]) / step
                    print('in %.1f/%s (%i/%i %.2fit/s).' % (step, self.tomins(step), self._it, self._vmax, itspersec), end='')

                    if self._verbose > 1:
                    # Print time elapsed from beginning of execution
                        elps = self._times[-1] - self._times[0]
                        print(' Elapsed %s.' % (self.tomins(elps)), end='')

                        if self._verbose > 2 and current_perc != 100 and 'numpy' in sys.modules:
                        # Print time remaining and total time estimated
                            p = np.poly1d(np.polyfit(self._passedits, self._times[1:], w=np.arange(1, len(self._times)), deg=1))
                            secs_remaining = p(self._vmax) - p(self._it)
                            print(' Ends in %s (Tot ~= %s).' % (self.tomins(secs_remaining), self.tomins(secs_remaining + elps)), end='')

                            if self._verbose > 3:
                            # Print estimated time until next percentage step
                                nxt = p(int(round((current_perc + 1) * self._vmax / 100 - 0.5) + 1)) - p(self._it)
                                print(' Next in %.1f/%s' % (nxt, self.tomins(nxt)), end='')

                if not self._inline:
                    print()
            if self._it == self._vmax:
                self._printdone()
            self._perc = current_perc
    
    def _printdone(self):
        '''
          Print execution time.
        '''
        if self._inline:
            print('\r', end='')
        print('Done in %s' % (self.tomins(time.time() - self._times[0])))

    def done(self):
        '''
          Close progress bar
        '''
        if self._it != self._vmax and not disable:
            self._printdone()
    
    def __iter__(self):
        return self

    def __next__(self):
        if self._it < self._vmax:
            self.next()
            return next(self._tomanage)
        else:
            raise StopIteration
