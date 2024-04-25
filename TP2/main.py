from typing import List, Tuple, Union
import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread("figs\\flower.png", cv2.IMREAD_GRAYSCALE)


def Conv2D(
    matrix: Union[List[List[float]], np.ndarray],
    kernel: Union[List[List[float]], np.ndarray],
    stride: Tuple[int, int] = (1, 1),
    dilation: Tuple[int, int] = (1, 1),
    padding: Tuple[int, int] = (0, 0),
) -> np.ndarray:
    """Makes a 2D convolution with the kernel over matrix using defined stride, dilation and padding along axes.
    Args:
        matrix (Union[List[List[float]], np.ndarray]): 2D matrix to be convolved.
        kernel (Union[List[List[float]], np.ndarray]): 2D odd-shaped matrix (e.g. 3x3, 5x5, 13x9, etc.).
        stride (Tuple[int, int], optional): Tuple of the stride along axes. With the `(r, c)` stride we move on `r` pixels along rows and on `c` pixels along columns on each iteration. Defaults to (1, 1).
        dilation (Tuple[int, int], optional): Tuple of the dilation along axes. With the `(r, c)` dilation we distancing adjacent pixels in kernel by `r` along rows and `c` along columns. Defaults to (1, 1).
        padding (Tuple[int, int], optional): Tuple with number of rows and columns to be padded. Defaults to (0, 0).
    Returns:
        np.ndarray: 2D Feature map, i.e. matrix after convolution.
    """
    matrix, kernel, k, h_out, w_out = _check_params(
        matrix, kernel, stride, dilation, padding
    )
    matrix_out = np.zeros((h_out, w_out))

    b = k[0] // 2, k[1] // 2
    center_x_0 = b[0] * dilation[0]
    center_y_0 = b[1] * dilation[1]
    for i in range(h_out):
        center_x = center_x_0 + i * stride[0]
        indices_x = [center_x + l * dilation[0] for l in range(-b[0], b[0] + 1)]
        for j in range(w_out):
            center_y = center_y_0 + j * stride[1]
            indices_y = [center_y + l * dilation[1] for l in range(-b[1], b[1] + 1)]

            submatrix = matrix[indices_x, :][:, indices_y]

            matrix_out[i][j] = np.sum(np.multiply(submatrix, kernel))
    return matrix_out


def _check_params(matrix, kernel, stride, dilation, padding):
    params_are_correct = (
        isinstance(stride[0], int)
        and isinstance(stride[1], int)
        and isinstance(dilation[0], int)
        and isinstance(dilation[1], int)
        and isinstance(padding[0], int)
        and isinstance(padding[1], int)
        and stride[0] >= 1
        and stride[1] >= 1
        and dilation[0] >= 1
        and dilation[1] >= 1
        and padding[0] >= 0
        and padding[1] >= 0
    )
    assert (
        params_are_correct
    ), "Parameters should be integers equal or greater than default values."
    if not isinstance(matrix, np.ndarray):
        matrix = np.array(matrix)
    n, m = matrix.shape
    matrix = matrix if list(padding) == [0, 0] else add_padding(matrix, padding)
    n_p, m_p = matrix.shape

    if not isinstance(kernel, np.ndarray):
        kernel = np.array(kernel)
    k = kernel.shape

    kernel_is_correct = k[0] % 2 == 1 and k[1] % 2 == 1
    assert kernel_is_correct, "Kernel shape should be odd."
    matrix_to_kernel_is_correct = n_p >= k[0] and m_p >= k[1]
    assert (
        matrix_to_kernel_is_correct
    ), "Kernel can't be bigger than matrix in terms of shape."

    h_out = (
        np.floor(
            (n + 2 * padding[0] - k[0] - (k[0] - 1) * (dilation[0] - 1)) / stride[0]
        ).astype(int)
        + 1
    )
    w_out = (
        np.floor(
            (m + 2 * padding[1] - k[1] - (k[1] - 1) * (dilation[1] - 1)) / stride[1]
        ).astype(int)
        + 1
    )
    out_dimensions_are_correct = h_out > 0 and w_out > 0
    assert (
        out_dimensions_are_correct
    ), "Can't apply input parameters, one of resulting output dimension is non-positive."

    return matrix, kernel, k, h_out, w_out


import numpy as np


image = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])

# Define the Sobel kernels
Sx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])

Sy = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])

Gx = Conv2D(image, Sx)
Gy = Conv2D(image, Sy)

# Display the results
print("Gx (Gradient along x-axis):\n", Gx)
print("Gy (Gradient along y-axis):\n", Gy)
