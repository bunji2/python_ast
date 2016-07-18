# -*- coding: utf-8 -*-

#
# python �X�N���v�g�� AST �c���[�� Graphviz ���g���� PNG ��
# �����_�����O����T���v���X�N���v�g
#

dot_exe = "/opt/graphviz/bin/dot.exe"
out_format = "png"

import sys
import os

def usage(script_path):
  print """Usage:
  python %s in_file.py ...""" % script_path

# AST �c���[�������_�����O���� dot �̃R�[�h���擾����
def get_dot_of_ast(source):
  # mode:�R���p�C�����[�h�B
  # 'exec' ----- ��A�� statements ���Ώ�
  # 'eval' ----- �P��� expression ���Ώ�
  # 'single' --- �P��̑Θb�I�� statement ���Ώ�
  mode = 'exec'

  # AST �c���[���擾
  import ast
  n = ast.parse(source, mode=mode)
  #n = compile(source, sys.argv[1], mode, ast.PyCF_ONLY_AST)

  # AST �c���[�̃_���v
  # dot_code: AST�c���[���\������ dot �R�[�h�̕�����
  # i: �ŏI�I�ɓ����� AST�c���[����������ϐ����̔ԍ��B�ϐ���= "n%d"%i
  import myast
  dot_code,i = myast.dump_dot(n)

  return dot_code

# AST�c���[���摜�t�@�C���֏����o��
def save_img_file(img_file, dot_file):
  # dot �R�}���h�̊m�F
  global dot_exe
  if not os.path.exists(dot_exe):
    print "Not Found: %s" % dot_exe
    quit()
  # dot �R�}���h�����s���A�摜�t�@�C�����o��
  global out_format
  cmd_line=[dot_exe, "-o%s" % img_file, "-T%s" % out_format, dot_file]
  import subprocess
  r = subprocess.check_call(cmd_line)
  if r == 0 and os.path.exists(img_file):
    print "Saved png in %s" % img_file

# dot �`���� AST�c���[�� dot �t�@�C���֏����o��
def save_dot_file(dot_file, dot_code):
  with open(dot_file, 'w') as f:
    f.write("# dumped by %s\n" % sys.argv[0])
    f.write(dot_code)
  print "Saved dot in %s" % dot_file

def process(in_file):
  dot_file = "%s.dot" % in_file
  img_file = "%s.%s" % (in_file, out_format)

  #���̓t�@�C���̓ǂݏo��
  with open(in_file) as f:
    source = f.read()

  #print "----%s-----"%sys.argv[1]
  #print source
  #print "----/%s----"%sys.argv[1]

  # ���̓t�@�C���� AST �c���[�� dot �`���Ƀ_���v
  dot_code = get_dot_of_ast(source)

  # dot �`���� AST�c���[�� dot �t�@�C���֏����o��
  save_dot_file(dot_file, dot_code)

  if os.path.exists(dot_file):
    # AST�c���[���摜�t�@�C���֏����o��
    save_img_file(img_file, dot_file)


def main(argv):
  #�����`�F�b�N
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

