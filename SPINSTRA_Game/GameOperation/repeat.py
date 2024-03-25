from threading import Timer

# Class that implements a repeated threaded task in the style of JavaScript's setInterval
class Repeat(Timer):
    #------------------------------#
    # Function that runs the specified task
    def run(self):
        try:
            while not self.finished.wait(self.interval):
                self.function(*self.args, **self.kwargs)
        except:
            pass
    #------------------------------#