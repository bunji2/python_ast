# -*- coding: utf-8 -*-

#
# python スクリプトから Graphviz の dot コマンドを実行する例
#

dot_exe = "/opt/graphviz/bin/dot.exe"
out_format = "png"

import sys,os.path,subprocess

def usage():
  print """Usage:
  python %s infile.dot""" % sys.argv[0]


def main(argv):

  global dot_exe
  global out_format

  if len(argv) < 2:
    usage()
    return

  if not os.path.exists(dot_exe):
    print "Not Found: %s" % dot_exe
    return

  infile = argv[1]

  if not os.path.exists(infile):
    print "Not Found: %s" % infile
    return

  outfile = "%s.%s" % (infile, out_format)
  cmd_line=[dot_exe, "-o%s" % outfile, "-T%s" % out_format, infile]

  #p = subprocess.Popen(cmd_line)
  r = subprocess.check_call(cmd_line)

  if r == 0 and os.path.exists(outfile):
    print "Saved in %s" % outfile

if __name__ == '__main__':
  main(sys.argv)
