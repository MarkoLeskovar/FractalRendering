import numba
import numpy as np

# TODO : Add edge case if max number of iterations has been reached and assign it number "0.0"

# Mandelbrot set fractal
@numba.njit(cache=True)
def iterations_mandelbrot_set(img_iterations, bounds_x, bounds_y, max_iter):

	# Get physical dimensions of the image
	img_size = img_iterations.shape[::-1]
	pix_size_x = (bounds_x[1] - bounds_x[0]) / img_size[0]
	pix_size_y = (bounds_y[1] - bounds_y[0]) / img_size[1]

	# Loop over each image pixel
	for i in range(img_size[1]):
		y0 = bounds_y[0] + 0.5 * pix_size_y + i * pix_size_y
		for j in range(img_size[0]):
			x0 = bounds_x[0] + 0.5 * pix_size_x + j * pix_size_x

			# Evaluate number of iterations
			x = 0.0
			y = 0.0
			x2 = 0.0
			y2 = 0.0
			num_iter = 0
			while (x2 + y2 <= 4.0) and (num_iter < max_iter):
				y = 2 * x * y + y0
				x = x2 - y2 + x0
				x2 = x * x
				y2 = y * y
				num_iter += 1

			# Assign iterations to correct pixel
			img_iterations[i, j] = float(num_iter)


# Mandelbrot set fractal - parallel
@numba.njit(cache=True, parallel=True)
def iterations_mandelbrot_set_parallel(img_iterations, bounds_x, bounds_y, max_iter):

	# Get physical dimensions of the image
	img_size = img_iterations.shape[::-1]
	pix_size_x = (bounds_x[1] - bounds_x[0]) / img_size[0]
	pix_size_y = (bounds_y[1] - bounds_y[0]) / img_size[1]

	# Loop over each image pixel
	for i in numba.prange(img_size[1]):
		y0 = bounds_y[0] + 0.5 * pix_size_y + i * pix_size_y
		for j in range(img_size[0]):
			x0 = bounds_x[0] + 0.5 * pix_size_x + j * pix_size_x

			# Evaluate number of iterations
			x = 0.0
			y = 0.0
			x2 = 0.0
			y2 = 0.0
			num_iter = 0
			while (x2 + y2 <= 4.0) and (num_iter < max_iter):
				y = 2 * x * y + y0
				x = x2 - y2 + x0
				x2 = x * x
				y2 = y * y
				num_iter += 1

			# Assign iterations to correct pixel
			img_iterations[i, j] = float(num_iter)


# Wrapper function for Mandelbrot set fractal
def IterationsMandelbrotSet(img_size, bounds_x, bounds_y, max_iter):
	# Convert the input to numpy arrays
	img_size = np.asarray(img_size).astype('int')
	bounds_x = np.asarray(bounds_x).astype('float')
	bounds_y = np.asarray(bounds_y).astype('float')
	# Compute the iterations
	img_iterations = np.empty(shape=img_size[::-1], dtype='float')
	iterations_mandelbrot_set(img_iterations, bounds_x, bounds_y, int(max_iter))
	# Return results
	return img_iterations


# Wrapper function for Mandelbrot set fractal - parallel
def IterationsMandelbrotSet_parallel(img_size, bounds_x, bounds_y, max_iter):
	# Convert the input to numpy arrays
	img_size = np.asarray(img_size).astype('int')
	bounds_x = np.asarray(bounds_x).astype('float')
	bounds_y = np.asarray(bounds_y).astype('float')
	# Compute the iterations
	img_iterations = np.empty(shape=img_size[::-1], dtype='float')
	iterations_mandelbrot_set_parallel(img_iterations, bounds_x, bounds_y, int(max_iter))
	# Return results
	return img_iterations
