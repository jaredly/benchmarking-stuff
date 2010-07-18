#!/usr/bin/env python

import os
import sys
import timeit
import textwrap
import optparse

def options():
    parser = optparse.OptionParser()
    parser.add_option('--num', '-n', dest='num', type='int', default=1, help='number of times to run it')
    parser.add_option('--out', '-o', dest='out', help='destination file')
    opts, pos = parser.parse_args()
    result = validate_options(pos, opts)
    if result is not None:
        parser.print_help()
        sys.exit(result)
    mod = pos[0]
    return mod, opts

def validate_options(pos, opts):
    if len(pos) != 1:
        print 'bench takes exactly one positional argument'
        return 1
    if opts.out is not None:
        logdir = os.path.dirname(opts.out)
        if os.path.exists(opts.out):
            print>>sys.stderr, 'Log file %s already exists' % opts.out
            return 2
        elif logdir and not os.path.exists(logdir):
            print>>sys.stderr, 'Log directory %s does not exist' % os.path.dirname(opts.out)
            return 3

    mod = pos[0]
    if not os.path.exists(mod):
        print>>sys.stderr, 'folder %s does not exist.' % mod
        return 4
    elif not os.path.exists(os.path.join(mod, '__init__.py')):
        print>>sys.stderr, 'folder %s is not a python module' % mod
        return 5

def get_bench_data(mod):
    sys.path.insert(0, mod)
    try:
        tobench = __import__(mod)
    except ImportError, e:
        print>>sys.stderr, 'Either there\'s no module %s, or it raised an ImportError some other way' % mod
        sys.exit(1)
    return tobench.text, tobench.functions

def benchmark(number, text, functions):
    titles = functions.keys()
    results = []
    lines = []
    for name in titles:
        print 'benching', name
        results.append(bench_one(number, text, functions[name][0]))
        lines.append(functions[name][1])
    return titles, results, lines

def save_data(outfile, titles, results, lines):
    tpl = textwrap.dedent('''\
    var titles = %s;
    var results = %s;
    var lines = %s;
    ''')
    outfile.write(tpl % (titles, results, lines))

func = None
text = None
def bench_one(number, txt, fn):
    global func, text
    func = fn
    text = txt
    return timeit.timeit('func(text)', 'from __main__ import func, text', number=number)/number

def main():
    mod, opts = options()
    benched = benchmark(int(opts.num), *get_bench_data(mod))
    for name, item in zip(('titles', 'results', 'lines'), benched):
        print '%s: %s' % (name, item)
    if opts.out:
        outfile = open(opts.out, 'w')
        save_data(outfile, *benched)
        outfile.close()

if __name__ == '__main__':
    main()

# vim: et sw=4 sts=4
