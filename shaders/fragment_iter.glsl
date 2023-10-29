#version 400 core

// IN - Fragment coordinate
layout(pixel_center_integer ) in vec4 gl_FragCoord;

// IN - Fractal settings
uniform double pix_size;
uniform dvec2 range_x;
uniform dvec2 range_y;
uniform int num_iter;

// OUT - Number of iterations
out float iterations;


// FUNCITON - Compute physical coordinate of the pixel
dvec2 ComputePixelCoordinate(dvec2 range_x, dvec2 range_y, double pix_size)
{
    double x0 = range_x[0] + 0.5 * pix_size + gl_FragCoord.x * pix_size;
    double y0 = range_y[0] + 0.5 * pix_size + gl_FragCoord.y * pix_size;
    return dvec2(x0, y0);
}


// FUNCTION - Compute number of iterations
float ComputeIterationCountMandelbrotSet(dvec2 pix_coord, int max_iter)
{
    // Initialize variables
    double x = 0.0;
    double y = 0.0;
    double x2 = 0.0;
    double y2 = 0.0;
    int iter = 0;
    // Evaluate number of iterations
    while ((x2 + y2 <= 4.0) && (iter < num_iter))
    {
        y = 2 * x * y + pix_coord.y;
    	x = x2 - y2 + pix_coord.x;
    	x2 = x * x;
        y2 = y * y;
        iter += 1;
    }
    return float(iter);
}

// FUNCTION - Compute number of iterations
float ComputeIterationCountMandelbrotSet_smooth(dvec2 pix_coord, int max_iter)
{
    // Initialize variables
    double x = 0.0;
    double y = 0.0;
    double x2 = 0.0;
    double y2 = 0.0;
    int iter = 0;
    // Evaluate number of iterations
    while ((x2 + y2 <= 4.0) && (iter < num_iter))
    {
        y = 2 * x * y + pix_coord.y;
    	x = x2 - y2 + pix_coord.x;
    	x2 = x * x;
        y2 = y * y;
        iter += 1;
    }
    // Smooth coloring
    if (iter < num_iter)
    {
        float log_zn = log(float(x2 + y2)) / 2.0;
        float nu = log(log_zn / log(2.0)) / log(2.0);
        return float(iter) + 1.0 - nu;
    }
    else
    {
        return float(iter);
    }
}


// FUNCTION - Main function
void main()
{
    // Compute pixel coordinate
    dvec2 pixel_coordinate = ComputePixelCoordinate(range_x, range_y, pix_size);

    // Compute iteration count
    iterations = ComputeIterationCountMandelbrotSet_smooth(pixel_coordinate, num_iter);
}