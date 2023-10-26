#version 400 core

// IN - Fragment coordinate
layout(pixel_center_integer ) in vec4 gl_FragCoord;

// IN - Fractal settings
uniform double pix_size;
uniform dvec2 range_x;
uniform dvec2 range_y;
uniform int max_iter;

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
    while ((x2 + y2 <= 4.0) && (iter < max_iter))
    {
        y = 2 * x * y + pix_coord.y;
    	x = x2 - y2 + pix_coord.x;
    	x2 = x * x;
        y2 = y * y;
        iter += 1;
    }
    // Return iterations
    return float(iter);
}


// FUNCTION - Main function
void main()
{
    // Compute pixel coordinate
    dvec2 pixel_coordinate = ComputePixelCoordinate(range_x, range_y, pix_size);

    // Compute iteration count
    iterations = ComputeIterationCountMandelbrotSet(pixel_coordinate, max_iter);
}