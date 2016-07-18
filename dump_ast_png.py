# -*- coding: utf-8 -*-

#
# python スクリプトの AST ツリーを Graphviz を使って PNG に
# レンダリングするサンプルスクリプト
#

dot_exe = "/opt/graphviz/bin/dot.exe"
out_format = "png"

import sys
import os

def usage(script_path):
  print """Usage:
  python %s in_file.py ...""" % script_path

# AST ツリーをレンダリングする dot のコードを取得する
def get_dot_of_ast(source):
  # mode:コンパイルモード。
  # 'exec' ----- 一連の statements が対象
  # 'eval' ----- 単一の expression が対象
  # 'single' --- 単一の対話的な statement が対象
  mode = 'exec'

  # AST ツリーを取得
  import ast
  n = ast.parse(source, mode=mode)
  #n = compile(source, sys.argv[1], mode, ast.PyCF_ONLY_AST)

  # AST ツリーのダンプ
  # dot_code: ASTツリーを構成する dot コードの文字列
  # i: 最終的に得られる ASTツリーが代入される変数名の番号。変数名= "n%d"%i
  import myast
  dot_code,i = myast.dump_dot(n)

  return dot_code

# ASTツリーを画像ファイルへ書き出し
def save_img_file(img_file, dot_file):
  # dot コマンドの確認
  global dot_exe
  if not os.path.exists(dot_exe):
    print "Not Found: %s" % dot_exe
    quit()
  # dot コマンドを実行し、画像ファイルを出力
  global out_format
  cmd_line=[dot_exe, "-o%s" % img_file, "-T%s" % out_format, dot_file]
  import subprocess
  r = subprocess.check_call(cmd_line)
  if r == 0 and os.path.exists(img_file):
    print "Saved png in %s" % img_file

# dot 形式の ASTツリーを dot ファイルへ書き出し
def save_dot_file(dot_file, dot_code):
  with open(dot_file, 'w') as f:
    f.write("# dumped by %s\n" % sys.argv[0])
    f.write(dot_code)
  print "Saved dot in %s" % dot_file

def process(in_file):
  dot_file = "%s.dot" % in_file
  img_file = "%s.%s" % (in_file, out_format)

  #入力ファイルの読み出し
  with open(in_file) as f:
    source = f.read()

  #print "----%s-----"%sys.argv[1]
  #print source
  #print "----/%s----"%sys.argv[1]

  # 入力ファイルの AST ツリーを dot 形式にダンプ
  dot_code = get_dot_of_ast(source)

  # dot 形式の ASTツリーを dot ファイルへ書き出し
  save_dot_file(dot_file, dot_code)

  if os.path.exists(dot_file):
    # ASTツリーを画像ファイルへ書き出し
    save_img_file(img_file, dot_file)


def main(argv):
  #引数チェック
  if len(argv) < 2:
    usage(argv[0])
    quit()

  import glob
  for in_file in glob.glob(argv[1]):
    process(in_file)

if __name__ == '__main__':
  main(sys.argv)

#http://docs.python.jp/3.4/library/ast.html#ast.AST
#http://docs.python.jp/2.7/library/ast.html#module-ast

