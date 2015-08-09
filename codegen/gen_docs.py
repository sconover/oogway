import os
import sys
import re

this_dir = os.path.dirname(os.path.realpath(__file__))
mcgamedata_dir = os.path.join(this_dir, "../../mcgamedata")
sys.path.append(mcgamedata_dir)

from mcgamedata import block

markdown_lines = []

const_re = re.compile('^[A-Z0-9_]+$')
const_property_re = re.compile('^PROPERTY_.*$')

for b in dir(block):
  if const_re.search(str(b)):
    markdown_lines.append("* [" + b.lower() + "](#" + b + ")")

markdown_lines.append("---------------------------------------")

for b in dir(block):
  if const_re.search(str(b)):
    markdown_lines.append("* <a name='" + b + "'></a> block: " + b + " `pen_down(block.{})`".format(b))
    for p in dir(eval("block." + b)):
      if str(p).startswith("PROPERTY_"):
        property_name = p.replace("PROPERTY_", "")
        markdown_lines.append("    * property: " + property_name)

        property_re = re.compile("^" + property_name + "_.*")
        for v in dir(eval("block." + b)):
          if property_re.search(str(v)):
            markdown_lines.append("        * " + v + "  `pen_down(block.{}, block.{}.{})`".format(b, b, v))

markdown_str = "\n".join(markdown_lines)
f = open(os.path.join(this_dir, "../docs/block.md"), 'w')
f.write(markdown_str)
f.close()
