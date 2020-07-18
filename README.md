# progress_bar_python
A very simple progress bar for python with accurate time prediction (linear).

In case the average duration of each iteration tends to be stable, you will get an accurate prediction of the time remaining, computed with a linear fit of the durations of the iterations elapsed. 

It won't slow down your code unless the operations of each iteration consist in less than a dozen basic mathematical operations (like addition or multiplication).

# Usage
```python
from perc import Perc

iter_object = range(100000000)

# tqdm like
for i in Perc(iter_object):
  # do stuff
```

or

```python
from perc import Perc

iter_object = range(100000000)

p = Perc(len(iter_object))
for i in iter_object:
  # do stuff
  p.next()  # or p.next(i) in case the step isn't 1
p.done()
```

# Requirements
Python 3
numpy (only reccomended)
