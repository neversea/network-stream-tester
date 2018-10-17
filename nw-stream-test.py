#!/usr/bin/python

import sys
import threading

import nw_stream_test

opt = nw_stream_test.Options()
summary = nw_stream_test.Summary()
display = nw_stream_test.Display(opt, summary)

if opt.verbose:
    print "%s started" % (sys.argv[0])

control = nw_stream_test.Control(opt, display.screen)
control.thread.join()
summary.stop()
display.stop()

main_thread = threading.currentThread()
for t in threading.enumerate():
    if t is main_thread:
        continue
    if opt.verbose:
        print 'waiting for %s thread to finish...' % t.getName()
    t.join()
