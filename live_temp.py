#!/usr/bin/env python3
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.ticker as ticker
import numpy as np
import numpy.ma as ma
import Temperature as temp

# parameters
sample_speed = 250                                 # milliseconds
seconds_to_plot = 300                              # total second to plot, used to calculate the amount of samples required
x_len = (1000 // sample_speed) * seconds_to_plot   # number of points to display
y_range = [0, 50]                                  # range of possible Y values to display

# create figure for plotting
fig = plt.figure()

ax = fig.add_subplot(1, 1, 1)
ax.set_ylim(y_range)

# add locators and grid to the figure
ax.xaxis.set_major_locator(ticker.AutoLocator())
ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())

ax.yaxis.set_major_locator(ticker.AutoLocator())
ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())

ax.grid(True)

xs = list(range(0, x_len))
ys = [0] * x_len
ann_list = []

# initialize communication with sensor
# if it returns false it failed getting the I2C device and
# we need to abort execution
temperature = temp.Temperature()
if temperature.setup() == False:
    exit(-1)

# create a blank line. We will update the line in animate
line, = ax.plot(xs, ys)

# format plot
plt.title('Temperature over Time')
plt.xlabel('Samples')
plt.ylabel('Temperature (Celcius)')

# set window title
mngr = plt.gcf()
mngr.canvas.set_window_title("Live Temperature")

# this function is called periodically from FuncAnimation
# adding a new temperature reading to data set
def animate(i,ys):
    # read temperature (Celsius) from ADC device
    temp_c = round(temperature.get_temp_celsius(), 2)
    # add y to list
    ys.append(temp_c)
    # limit y list to set number of items
    ys = ys[-x_len:]
    # update line with new Y values
    line.set_ydata(ys)

    annotations(xs,ys,ax,temp_c)

    return line,

# does the annotations showing min, max and current temperature values
def annotations(x,y, ax=None, latest=0.0):
    # remove annotations
    for i, a in enumerate(ann_list):
       a.remove()
    ann_list[:] = []

    # calculates min and max temperature
    masked_y = ma.masked_equal(y, 0.0, copy=False)
    ymin = masked_y.min()    
    ymax = y[np.argmax(y)]

    text= "min={:.2f}\nmax={:.2f}\ncurrent={:.2f}".format(ymin,ymax,latest)

    if not ax:
        ax=plt.gca()
    bbox_props = dict(boxstyle="round,pad=0.3", fc="w", ec="k", lw=0.70)
    kw = dict(xycoords='data',textcoords="axes fraction",
              arrowprops=None, bbox=bbox_props, ha="right", va="top", color="purple")
    ann = ax.annotate(text, xy=(ymin, ymax), xytext=(0.95,0.95), **kw)  
    ann_list.append(ann)    

def destroy():
    temperature.destroy()

if __name__ == '__main__':  # program entrance
    # set up plot to call animate() function periodically
    ani = animation.FuncAnimation(fig,
        animate,
        fargs=(ys,),
        interval=sample_speed,
        blit=False)  
        
    try:
        plt.show()

    except KeyboardInterrupt: # press ctrl-c to end the program.
        destroy()