import curses
import threading
import time

commands = {
    'quit': [ ord('q'), ord('Q') ],
    'slower': [ ord('-'), ord('_') ],
    'faster': [ ord('+'), ord('=') ]
}

class Control:
    def __init__(self, options, screen):
        self.options = options
        self.screen = screen
        self.runable = True
        self.thread = threading.Thread(name="control", target=self.listen)
        self.thread.start()

    def listen(self):
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(1)
        opt = self.options
        while self.runable:
            c = self.screen.getch()
            if c in commands['quit']:
                curses.echo()
                curses.nocbreak()
                self.screen.keypad(0)
                return
            elif c in commands['slower']:
                opt.rate /= 2
            elif c in commands['faster']:
                opt.rate *= 2
            elif c >= ord('0') and c <= ord('9'):
                if c == ord('0'):
                    opt.display_rate = 10
                else:
                    opt.display_rate = c - ord('0')

    def stop(self):
        self.runable = False


class Display:
    def __init__(self, options, summary):
        self.screen = curses.initscr()
        self.options = options
        self.summary = summary
        self.runable = True
        self.thread = threading.Thread(name="display", target=self.view)
        self.thread.start()

    def view(self):
        screen = self.screen
        while self.runable:
            time.sleep(opt.display_rate)
            max_y, max_x = screen.getmaxyx()
            top_line = "rate: %0.1f" % self.options.rate
            while len(top_line) < max_x:
                top_line += ' '
            screen.addstr(0, 0, top_line, curses.A_REVERSE)
            pass
            screen.refresh()
        curses.endwin()

    def stop(self):
        self.runable = False
