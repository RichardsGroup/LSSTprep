# Defining functions to be used for plotting light curves
# some really ugly functions gon' be in this jawn
import numpy as np
import math
import matplotlib.pyplot as plt
from sklearn.gaussian_process import GaussianProcessRegressor
import sklearn.gaussian_process.kernels as kern

# keep colors consistent while plotting
colors = {'u':'b', 'g':'g', 'r':'r',
    'i':'orange', 'z':'brown', 'y':'black'}

def krig(x, y, x_test):
    '''
    Function to perform kriging
    '''
    # Define our model and kernel
    kernel = kern.RationalQuadratic()
    gp = GaussianProcessRegressor(kernel=kernel)

    # Fit our model to the data
    gp.fit(x, y)

    # Get prediction and std deviation from model
    pred, sigma = gp.predict(x_test, return_std=True)

    return pred, sigma

def plot_krig(x1, y1, x2, y2, c1, c2, n=2, timerange=(0,1e5)):
    '''
    Function to plot the kriging
    '''
    # if range is specified, use that instead
    if (timerange[1] != 1e5):
        inds = [(time >= timerange[0]) & (time <= timerange[1])]
        flux = flux[inds]
        time = time[inds]

    x = np.concatenate([x1, x2])
    y = np.concatenate([y1, y2])
    x_test = np.linspace(np.min(x), np.max(x), len(x)).reshape(-1, 1)
    ypred, stddev = krig(x,y, x_test)

    # note x2 and y2 should already have added in adjustment
    fig = plt.figure(figsize=(14,8))

    # Plot adjusted kriging fit
    xfill = np.concatenate([x_test, x_test[::-1]])
    yfill = np.concatenate([ypred - n*stddev,(ypred + n*stddev)[::-1]])
    plt.fill(xfill, yfill, alpha=.25, fc='#ABB2B9', ec='None', label='%s$\sigma$ Interval'%n)

    plt.plot(x1, y1, '.', color= colors[c1], label=c1+'-band data', alpha=0.75)
    plt.plot(x2, y2, '.', color= colors[c2], label=c2+'-band data', alpha=0.75)
    plt.plot(x_test, ypred, '#283747', label='Prediction')

    plt.xlabel('Time(days)')
    plt.ylabel('Magnitude')
    plt.legend()

    plt.show()


def plot_shift(x1, y1, x2, y2, dx, dy, c1, c2, n=2):
    '''
    Function to plot the difference in kriging between a non-shifted
    combine and  a shifted combine of light curves from different bands

    Also performs the kriging (using scikit learn)

    God, this is so ugly...
    '''

    # perform default kriging
    og_x = np.concatenate([x1, x2])
    og_y = np.concatenate([y1, y2])
    og_test_x = np.linspace(np.min(og_x), np.max(og_x), len(og_x)).reshape(-1, 1)
    og_pred, og_sigma = krig(og_x, og_y, og_test_x)

    # perform shifted kriging
    shift_x = np.concatenate([x1, x2+dx])
    shift_y = np.concatenate([y1, y2+dy])
    shift_test_x = np.linspace(np.min(shift_x), np.max(shift_x), len(shift_x)).reshape(-1, 1)
    shift_pred, shift_sigma = krig(shift_x, shift_y, shift_test_x)


    # Plotting time!
    f, ax = plt.subplots(2, figsize=(16,12), sharex=True)

    #original kriging
    xfill = np.concatenate([og_test_x, og_test_x[::-1]])
    yfill = np.concatenate([og_pred - n*og_sigma,(og_pred + n*og_sigma)[::-1]])

    ax[0].fill(xfill, yfill, alpha=.25, fc='#ABB2B9', ec='None', label='%s$\sigma$ Interval'%n)
    ax[0].plot(x1, y1, '.', color= colors[c1], label=c1+'-band data', alpha=0.75)
    ax[0].plot(x2, y2, '.', color= colors[c2], label=c2+'-band data', alpha=0.75)
    ax[0].plot(og_test_x, og_pred, '#283747', label=u'Prediction')
    ax[0].set_title('Original')
    ax[0].legend()

    # Adjusted kriging
    xfill = np.concatenate([shift_test_x, shift_test_x[::-1]])
    yfill = np.concatenate([shift_pred - n*shift_sigma,(shift_pred + n*shift_sigma)[::-1]])

    ax[1].fill(xfill, yfill, alpha=.25, fc='#ABB2B9', ec='None', label='%s$\sigma$ Interval'%n)
    ax[1].plot(x1, y1, '.', color= colors[c1], label=c1+'-band data', alpha=0.75)
    ax[1].plot(x2+dx, y2+dy, '.', color= colors[c2], label=c2+'-band data', alpha=0.75)
    ax[1].plot(shift_test_x, shift_pred, '#283747', label=u'Prediction')
    ax[1].set_title(c2+'-band Shifted (Time shift: %s; Magnitude shift: %s)'%(dx, dy))
    ax[1].set_xlabel('Time(days)')
    ax[1].legend()

    # shared y label
    f.text(0.05, 0.5, 'Magnitude', va='center', rotation='vertical')





def extract_filters(color, data, xoffset=0.0, yoffset=0.0, frac=1.0, timerange=(0,1e5)):
    '''
    Extract the data for a given filter and apply an offset or cut if needed
    '''
    # arbitrary offsets to apply to data that lacks noise
    #yoffset = 20.0
    #xoffset = 12.0

    # Define variabbles to filter data by filter
    mask = data['filter']==color

    # Extract and reshape the data for scikit
    time = np.array(data['obsTimes'][mask]) + xoffset
    flux = np.array(data['absFlux'][mask]) + yoffset

    # if range is specified, use that instead
    if (timerange[1] != 1e5):
        inds = [(time >= timerange[0]) & (time <= timerange[1])]
        flux = flux[inds]
        time = time[inds]


    # split into smaller chunks to save computation time (if we want)
    ind = int(len(time)*frac)
    time = time[:ind]
    flux = flux[:ind]

    # reshape for sake of sklearn
    time = time.reshape(-1,1)

    return time, flux


def add_noise(y, sigma=0.1):
    '''
    Add noise to observation data
    '''
    return y+np.random.normal(scale=sigma, size=np.shape(y))

def extract_no_filter(data, xoffset=0.0, yoffset=0.0, frac=1.0, timerange=(0,1e5)):
    '''
    Extracts data without filters and apply an offset or cut if needed
    '''
    # Extract and reshape the data for scikit
    time = np.array(data['obsTimes']) + xoffset
    flux = np.array(data['absFlux']) + yoffset

    # if range is specified, use that instead
    if (timerange[1] != 1e5):
        inds = [(time >= timerange[0]) & (time <= timerange[1])]
        flux = flux[inds]
        time = time[inds]

    # split into smaller chunks to save computation time (if we want)
    ind = int(len(time)*frac)
    time = time[:ind]
    flux = flux[:ind]

    # reshape for sake of sklearn
    time = time.reshape(-1,1)

    return time, flux

def find_nearest_index(array,value):
    '''
    Function to find the index of the nearest value of a np array
    '''
    if (array.ndim > 1): array = array.ravel()

    idx = np.searchsorted(array, value, side="left")
    if idx > 0 and (idx == len(array) or math.fabs(value - array[idx-1]) < math.fabs(value - array[idx])):
        #return array[idx-1]
        return idx-1
    else:
        #return array[idx]
        return idx
