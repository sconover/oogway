import sys
import os
import inspect
import types

this_dir = os.path.dirname(os.path.realpath(__file__))
code_dir = os.path.join(this_dir, "../oogway")

sys.path.append(os.path.join(this_dir, ".."))
sys.path.append(os.path.join(this_dir, "../../mcgamedata"))

from oogway import turtle

functions_to_document = map(lambda element: getattr(turtle, element), dir(turtle))
functions_to_document = filter(lambda element: isinstance(element, types.FunctionType), functions_to_document)
functions_to_document = filter(lambda element: not element.__name__.startswith("_"), functions_to_document)
functions_to_document = filter(lambda element: inspect.getdoc(element) != None, functions_to_document)

# print inspect.getdoc(turtle)

readme = []

print functions_to_document
for f in functions_to_document:
  # print inspect.formatargvalues(f)
  lines = inspect.getdoc(f).strip().split("\n")
  previous_line_was_output = False
  for line in lines:
    if previous_line_was_output:
      readme.append(("output", line))
    elif line.strip() == ">>> get_tiles()":
      previous_line_was_output = True
    elif line.startswith(">>>") or line.startswith("..."):
      readme.append(("code", line[3:]))
      previous_line_was_output = False
    elif line.strip() == "":
      previous_line_was_output = False
      readme.append(("text", line))
    else:
      readme.append(("text", line))

readme_str = ""
previous_line_was_code = False
previous_line_was_output = False
for line_type, line in readme:
  if line_type == "code":
    if not previous_line_was_code:
      readme_str += "```python\n"
    previous_line_was_code = True
    previous_line_was_output = False
  elif line_type == "output":
    if previous_line_was_code:
      readme_str += "```\n"
    if not previous_line_was_output:
      readme_str += "```text\n"
    previous_line_was_code = False
    previous_line_was_output = True
  else:
    if previous_line_was_code or previous_line_was_output:
      readme_str += "```\n"
      previous_line_was_code = False
      previous_line_was_output = False

  readme_str += line.strip() + "\n"

print readme_str

f = open(os.path.join(this_dir, "../README.md"), "w")
f.write(readme_str)
f.close()
