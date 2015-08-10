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
  nicer_block_name = b.lower().replace("_", " ")
  if const_re.search(str(b)):
    markdown_lines.append("* [" + nicer_block_name + "](#" + b + ")")

markdown_lines.append("---------------------------------------")

for b in dir(block):
  if const_re.search(str(b)):
    nicer_block_name = b.lower().replace("_", " ")
    markdown_lines.append("# <a name='" + b + "'></a> " + nicer_block_name)
    markdown_lines.append("".format(b))
    markdown_lines.append("    pen_down(block.{})".format(b))
    markdown_lines.append("")
    for p in dir(eval("block." + b)):
      if str(p).startswith("PROPERTY_"):
        property_name = p.replace("PROPERTY_", "")
        nicer_property_name = property_name.lower().replace("_", " ")
        markdown_lines.append("* **" + nicer_property_name + "**")

        property_re = re.compile("^" + property_name + "_.*")
        for v in dir(eval("block." + b)):
          nicer_value_name = v.replace(property_name + "_", "", 1).lower().replace("_", "-")
          if property_re.search(str(v)):
            markdown_lines.append("    * **" + nicer_value_name + ":**  ```pen_down(block.{}, block.{}.{})```".format(b, b, v))
    # markdown_lines.append("<br/>")
    markdown_lines.append("")

markdown_str = "\n".join(markdown_lines)
f = open(os.path.join(this_dir, "../docs/blocks.md"), 'w')
f.write(markdown_str)
f.close()
