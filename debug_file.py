import os
import time
import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colormaps
from PIL import Image, ImageDraw, ImageFont

# Import custom modules
import fractals.color as fract_color
import fractals.mandelbrot as fract_mandelbrot


# Define path to output folder and create it
path_to_output = os.path.join(os.path.expanduser("~"), 'Pictures', 'FractalRendering')
if not os.path.exists(path_to_output):
	os.makedirs(path_to_output)


# TODO : WORK ON THIS FILE !!!!
# TODO : Check if everything is implemented correctly (histogram, colormaps...). Make example scripts.
# TODO : Add cyclic colormapping option
# TODO : Add smooth-iteration count for fractal coloring
# TODO : Add Julia set fractal
# TODO : Add "HSV2RGB" a "RGB2HSV" functions


# Define main function
def main():

	# Fractal settings
	img_size = (1000, 1000)
	max_iter = 256
	# Default view
	range_x = (-1.5, 0.5)
	range_y = (-1.0, 1.0)

	# Compute number of fractal iterations
	iterations = fract_mandelbrot.IterationsMandelbrotSet_parallel(img_size, range_x, range_y, max_iter)

	# PLOT - Show iterations count
	extent = np.hstack((range_x, range_y))
	plt.imshow(np.flipud(iterations), extent=extent, origin='upper', interpolation='none', cmap='viridis')
	plt.title('Mandelbrot set iterations')
	plt.colorbar()
	plt.show()

	# Compute low-resolution version of iterations
	img_size_LR = (32, 32)
	iterations_LR = fract_mandelbrot.IterationsMandelbrotSet_parallel(img_size_LR, range_x, range_y, max_iter)

	# Compute image histograms
	hist = fract_color.IterationsHistogram(iterations, max_iter)
	hist_LR = fract_color.IterationsHistogram(iterations_LR, max_iter)

	# Compute histogram sums
	sum_hist = np.sum(hist)
	sum_hist_LR = np.sum(hist_LR)

	# PLOT - Show both histograms
	plt.plot(hist / sum_hist, 'b-', label=f'Image size = {img_size[0]}x{img_size[1]}')
	plt.plot(hist_LR / sum_hist_LR, 'r-', label=f'Image size = {img_size_LR[0]}x{img_size_LR[1]}')
	plt.title('Histogram of fractal iterations')
	plt.legend()
	plt.show()

	# Histogram coloring
	iterations_norm = fract_color.HistogramRecoloring(iterations, hist, sum_hist)
	iterations_norm_NEW = fract_color.HistogramRecoloring(iterations, hist_LR, sum_hist_LR)

	# PLOT - Show difference in High-Resolution (HR) and Low-Resolution (LR) histograms
	extent = np.hstack((range_x, range_y))
	img_difference = iterations_norm - iterations_norm_NEW
	plt.imshow(np.flipud(img_difference), extent=extent, origin='upper', interpolation='none', cmap='bwr',
			   vmin=-np.max(img_difference), vmax=np.max(img_difference))
	plt.title('Difference between Full-Res and Low-Res histogram recoloring')
	plt.colorbar()
	plt.show()

	# Get matplotlib colormap
	cmap = colormaps.get('ocean_r')
	cmap_array = cmap(range(cmap.N))[:, 0:3].astype('float32')
	# cmap_array = fract_color.cmap_wikipedia()

	# Apply colormap
	# iter = iterations / max_iter
	iter = iterations_norm

	# img_color = fract_color.ApplyColormap_nearest(iter, cmap_array)
	img_color = fract_color.ApplyColormap_linear(iter, cmap_array)
	# img_color = fract_color.ApplyColormap_cubic(iter, cmap_array)

	# Convert to floats to RGB
	img_color = (255 * img_color).astype('uint8')

	# PLOT - Show the image
	extent = np.hstack((range_x, range_y))
	plt.imshow(np.flipud(img_color), extent=extent, origin='upper', interpolation='none')
	plt.show()

	# Save the image to a folder
	add_text = True
	pil_image = Image.fromarray(np.flipud(img_color))
	draw = ImageDraw.Draw(pil_image)
	if add_text:
		font_size = int(img_size[1] / 30)
		fill_color = (255, 255, 255)
		font = ImageFont.truetype(f'C://Windows//Fonts//Arial.ttf', font_size)
		draw.text((0, 0            ), f'BOUNDS-X : {range_x}', font=font, fill=fill_color)
		draw.text((0, font_size    ), f'BOUNDS-Y : {range_y}', font=font, fill=fill_color)
		draw.text((0, font_size * 2), f'NUM ITER : {max_iter}', font=font, fill=fill_color)
	filename = f'{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.png'
	pil_image.save(os.path.join(path_to_output, filename))


# Run main function
if __name__ == "__main__":
	main()