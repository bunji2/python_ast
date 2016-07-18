# -*- coding: utf-8 -*-

#
# AST ツリーをダンプするサンプルスクリプト
#

import ast

i=0

import re

def escape(s, quoted=u'\'"\\', escape=u'\\'):
    return re.sub(
            u'[%s]' % re.escape(quoted),
            lambda mo: escape + mo.group(),
            s)

def unescape(s, quoted=u'\'"\\', escape=u'\\'):
    return re.sub(
            ur'%s([%s])' % (re.escape(escape), re.escape(quoted)),
            ur'\1',
            s)

def dump(n):

  def _dump(n, r=[], name=""):
    global i

    #print type(r)

    #print "#%d:%s:%s" % (i, str(type(n)), name)
    if isinstance(n, ast.AST):

      fields={}
      nodes={}
      for k in n._fields:
        attr = getattr(n, k)
        if attr == None:
          fields[k] = None
        elif isinstance(attr, list) and len(attr)==0:
          fields[k] = []
        elif isinstance(attr, ast.AST) and len(attr._fields)==0 and len(attr._attributes)==0:
          fields[k] = "ast.%s()" % (attr.__class__.__name__)
        else:
          j,t = _dump(attr, r, k)
          if t == None:
            nodes[k] = j
          else:
            fields[k] = t

      attributes={}
      for k in n._attributes:
        attr = getattr(n, k)
        if attr == None:
          attributes[k] = None
        elif isinstance(attr, list) and len(attr)==0:
          attributes[k] = []
        else:
          j,t = _dump(attr, r, k)
          if t == None:
            nodes[k] = j
          else:
            attributes[k] = t

      fields = ["%s=%s" % (k, fields[k]) for k in fields.keys()]
      nodes = ["%s=n%d" % (k, nodes[k])  for k in nodes.keys()]
      #print "fields:"+str(fields)
      #print "nodes:"+str(nodes)

      attributes = ["%s=%s" % (k, attributes[k]) for k in attributes.keys()]

      fields.extend(nodes)
      fields.extend(attributes)

      a = ",".join(fields)

      j=i
      #print type(r)
      r.append("n%d=ast.%s(%s)" % (j, n.__class__.__name__, a))
      i=i+1
      #print "n%d=%s" % (i, n.__class__.__name__)
      return j, None

    elif isinstance(n, list):

      items=[]
      for x in n:
        j,t = _dump(x, r, "%s_" % name)
        if t == None:
          items.append("n%d"%j)
        else:
          items.append(t)

      #print "#items="+str(items)
      j = i
      r.append("n%d=[%s]" % (j, str(",".join(items))))
      i = i+1
      return j, None

    elif isinstance(n, str):
      #print "n%d=\"%s\"" % (i, n)
      return i, "\"%s\"" % escape(n)

    elif isinstance(n, int):
      #print "n%d=%d" % (i, n)
      return i, str(n)

    else:
      r.append("#unknown" + str(type(n)))
      j = i
      r.append("n%d=%s" % (j, str(n)))
      i = i+1
      return j, n

  i = 0
  r = []
  j,t = _dump(n, r)
  return "\n".join(r), j

def dump_dot(n):

  def _dump(n, r=[], name=""):
    global i

    #print type(r)

    #print "#%d:%s:%s" % (i, str(type(n)), name)
    if isinstance(n, ast.AST):

      fields={}
      nodes={}
      for k in n._fields:
        attr = getattr(n, k)
        if attr == None:
          fields[k] = None
        elif isinstance(attr, list) and len(attr)==0:
          fields[k] = []
        elif isinstance(attr, ast.AST) and len(attr._fields)==0 and len(attr._attributes)==0:
          fields[k] = "%s()" % (attr.__class__.__name__)
        else:
          j,t = _dump(attr, r, k)
          if t == None:
            nodes[k] = j
          else:
            fields[k] = t

      fields = ["<%s>%s=%s" % (k, k, fields[k]) for k in fields.keys()]
      #nodes = ["%s=n%d" % (k, nodes[k])  for k in nodes.keys()]
      #print "fields:"+str(fields)
      #print "nodes:"+str(nodes)

      fields.extend(["<%s>%s" % (k, k)  for k in nodes.keys()])

      labels=["<cn>%s" % n.__class__.__name__]
      labels.extend(fields)

      j=i
      #print type(r)
      r.append("\"n%d\" [label=\"%s\"];" % (j, "|".join(labels)))
      for k in nodes.keys():
        r.append("\"n%d\":<%s> -> \"n%d\":<cn>;" % (i,k,nodes[k]))
      i=i+1
      #print "n%d=%s" % (i, n.__class__.__name__)
      return j, None

    elif isinstance(n, list):

      fields=[]
      items=[]
      for x in n:
        j,t = _dump(x, r, "%s_" % name)
        if t == None:
          items.append(j)
        else:
          fields.append(t)

      #print "#items="+str(items)
      j = i
      if len(fields) == 0:
        r.append("\"n%d\" [label=\"[%d]\", shape=circle];" % (j, len(n)))
        for idx in range(len(items)):
          r.append("\"n%d\" -> \"n%d\":<cn> [label=\"%d\"];" % (j, items[idx], idx))
      else:
        r.append("\"n%d\" [label=\"[%d]|%s\"];" % (j, len(n), "|".join(fields)))

      i = i+1
      return j, None

    elif isinstance(n, str):
      #print "n%d=\"%s\"" % (i, n)
      return i, "\\\"%s\\\"" % escape(n).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('{', "\\{")

    elif isinstance(n, unicode):
      #print "n%d=\"%s\"" % (i, n)
      return i, "\\\"%s\\\"" % escape(n).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('{', "\\{")

    elif isinstance(n, int):
      #print "n%d=%d" % (i, n)
      return i, str(n)

    else:
      r.append("#unknown" + str(type(n)))
      j = i
      r.append("#n%d=%s" % (j, str(n)))
      i = i+1
      return j, n

  i = 0
  r = ["digraph ast {",
       "graph [rankdir = \"LR\"];",
       "node [shape = record, fontname = \"Helvetica\", fontsize = 10];"]
  j,t = _dump(n, r)
  r.append("}")
  return "\n".join(r), j

