import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker

def demo_plot():
  x = range(100)
  N =len(x)
  y = range(100)
  plt.figure()

  plt.plot(x, y)
  plt.ylim((0, 1000))
  plt.xticks(range(len(x)), x, rotation=270)
  plt.title("Demo")
  plt.xlabel("x")
  plt.ylabel("y")

  # change x internal size
  plt.gca().margins(x=0)
  plt.gcf().canvas.draw()
  maxsize = 30
  m = 0.2  # inch margin
  s = maxsize / plt.gcf().dpi * N + 2 * m
  margin = m / plt.gcf().get_size_inches()[0]

  plt.gcf().subplots_adjust(left=margin, right=1. - margin)
  plt.gcf().set_size_inches(s, plt.gcf().get_size_inches()[1])

  plt.savefig("test.jpg")
  plt.show()

demo_plot()
