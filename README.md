Create a new turtle, about 5 blocks out from where the player is facing.

```python
begin()
```
```text
v
```
Broadcast a message to all minecraft players.

```python
chat("hi everyone")
```
[was broadcast to all players] hi everyone
Duration of pause, in seconds, between turtle moves.

Slowing down the turtle is useful to see exactly what the turtle is
doing, especially when you're "debugging" - or, trying to figure out
why something you've done isn't working. A good delay in a situation
like this is a half-second:

delay(0.5)

On the other hand, if you're confident that a program is doing what
you expect it to do, you may not want to wait around. You might want
to have no delay at all:

delay(0)

By default, the delay is one tenth of a second:

delay(0.1)
Start a new minecraft turtle session.
Returns a new subclass of tuple with named fields.

```python
Point = namedtuple('Point', ['x', 'y'])
Point.__doc__                   # docstring for the new class
```
'Point(x, y)'
```python
p = Point(11, y=22)             # instantiate with positional args or keywords
p[0] + p[1]                     # indexable like a plain tuple
```
33
```python
x, y = p                        # unpack like a regular tuple
x, y
```
(11, 22)
```python
p.x + p.y                       # fields also accessable by name
```
33
```python
d = p._asdict()                 # convert to a dictionary
d['x']
```
11
```python
Point(**d)                      # convert from a dictionary
```
Point(x=11, y=22)
```python
p._replace(x=100)               # _replace() is like str.replace() but targets named fields
```
Point(x=100, y=22)
Change the type of trail the turtle is leaving behind. When the turtle
moves forward or back, it will leave this thing behind.

The first argument must be a type of block, or a type of living thing.

Example: pen_down(block.STONE)
Example: pen_down(living.OCELOT)

The rest of the arguments may be any number of property values for a block type.

Example: pen_down(block.FLOWER_POT, block.FLOWER_POT.CONTENTS_BLUE_ORCHID)

TODO: see mcgamedata for details on block and living

```python
begin()
forward(2)
pen_down(block.STONE)
forward(2)
```
```text
G
G
S
S
v
```
Change the type of trail the turtle is leaving behind to be air blocks.

```python
begin()
forward(2)
pen_up()
forward(2)
```
```text
G
G
<BLANKLINE>
<BLANKLINE>
v
```
Turn the turtle to the right, the given number of degrees.

A complete turn (a circle) has 360 degrees, so:
- 90 degrees is a "right turn"
- 180 degrees (a half circle) turns the turtle around
- 270 degrees (3/4th of a circle) turns the turtle around so that
she is actually making a "left turn".
- 360 degrees (a whole circle) turns the turtle all the way around,
which points her in the same direction as before.
- 45 degrees is a right-diagonal move (between straight forward and a right turn)

Degrees must be a number.

```python
begin()
forward(2)
right(90) # face right
forward(2)
```
```text
G
G
< G G

>>> begin()
>>> forward(2)
>>> right(180) # face backwards
>>> forward(2)
>>> get_tiles()
^
G
G

>>> begin()
>>> forward(2)
>>> right(270) # face left (!)
>>> forward(2)
>>> get_tiles()
G
G
G G >

>>> begin()
>>> forward(2)
>>> right(360) # ...turn ALL the way around, meaning she's back facing the same direction as before
>>> forward(2)
>>> get_tiles()
G
G
G
G
v

>>> begin()
>>> forward(1)
>>> right(45) # ...move in a diagonal (right/front)
>>> forward(2)
>>> get_tiles()
G
G G
<
