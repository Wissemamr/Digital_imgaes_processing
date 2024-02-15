# import numpy as np
# import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D
import cv2
import numpy as np
import matplotlib.pyplot as plt

# generate some sample data
import scipy.misc


def view_surface(path):
    # reads an img in grayscale
    img = cv2.imread(path, 0)

    # downscaling has a "smoothing" effect
    img = cv2.resize(img, (100, 100)) / 250

    # create the x and y coordinate arrays (here we just use pixel indices)
    xx, yy = np.mgrid[0 : img.shape[0], 0 : img.shape[1]]

    # create the figure
    fig = plt.figure(figsize=(10, 10))
    # ax = fig.gca(projection='3d')
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(xx, yy, img, rstride=1, cstride=1, cmap=plt.cm.gray, linewidth=0)

    ax.view_init(elev=80, azim=25)

    plt.figure(figsize=(10, 10), dpi=180)

    # show it
    plt.show()


if __name__ == "__main__":
    img_path = "figs\\flower.png"
    view_surface(img_path)
