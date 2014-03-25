#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import argparse
import subprocess
from cStringIO import StringIO


def begincommandlog(o):
    print >>o, '#^'

def comment(c, o):
    if len(c) > 0:
        print >>o, '##', c

def timestamp(o):
    p = subprocess.Popen('date', stdout=subprocess.PIPE)
    print >>o, '#@', p.communicate()[0].strip()

def runcmd(c, o, u):
    print >>o, '#!'
    print >>o, c
    p = subprocess.Popen(c, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if len(out.strip()) > 0:
        if u:
            print >>o, '#!', '<<<   out  >>>'
            print >>o, out
            print >>o, '#!', '<<<   /out  >>>'
        print >>sys.stdout, out
    if len(err.strip()) > 0:
        if u:
            print >>o, '#!', '!!!   err  !!!'
            print >>o, err
            print >>o, '#!', '!!!   /err  !!!'
        print >>sys.stderr, err
    return p.returncode

def endcommandlog(o):
    print >>o, '#$'
    print >>o


def main(args):

    #c = args[1]
    #args = args[0]

    #print c
    #print args

    #sys.exit()

    o = StringIO()

    begincommandlog(o)
    comment(args.comment, o)
    timestamp(o)
    rc = runcmd(args.command, o, args.include_output)
    endcommandlog(o)

    if args.ignore_err is False:
        rc = 0

    if rc == 0:
        with open(args.logbook, 'a') as lb:
            lb.write(o.getvalue())

    o.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', '--command', dest='command',
        help='The command to launch in a subshell'
    )
    parser.add_argument(
        '-o', '--logbook', dest='logbook',
        default='README',
        help='File to use as a logbook'
    )
    parser.add_argument(
        '-C', '--comment', dest='comment',
        default='',
        help='Any comment to add to the logbook'
    )
    parser.add_argument(
        '-u', '--include_output', dest='include_output',
        action='store_true',
        default=False,
        help='Include output of the command in the logbook'
    )
    parser.add_argument(
        '-r', '--ignore_err', dest='ignore_err',
        action='store_true',
        default=False,
        help='If error, the command is not logged'
    )
    main(parser.parse_args())
    #main(parser.parse_known_args())
