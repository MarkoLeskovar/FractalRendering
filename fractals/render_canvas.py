import tripy
import numpy as np
from OpenGL.GL import *
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

# Import Python modules
from .canvas import Canvas
from .framebuffer import Framebuffer


# TODO : Add RenderCanvasManager class which should act as in interface between window and all canvases. It should also
#      : have a function that return the currently active canvas
# TODO : Add drawing area polygon creation to the class. Input should be in pixels and initialized with full window.
# TODO : Once this is done, merge the changes with the main branch before doing more work.

''' 
O------------------------------------------------------------------------------O
| RENDER CANVAS CLASS FOR ADVANCED WINDOW DRAWING AREA HANDLING                |
O------------------------------------------------------------------------------O
'''

class RenderCanvas(Canvas):

    def __init__(self, pos=(0, 0), win_size=(400, 300), range_x=(-1, 1), pix_scale=1.0, zoom_min=0.5, zoom_max=1.0e15, zoom_step=0.02):

        # Initialize empty variables
        self.framebuffers = {}
        self.polygon = None
        self.polygon_vao = None
        self.polygon_buffer = None
        self.polygon_buffer_n_indices = None

        # Derived class variables
        self.pos = np.asarray(pos).astype('int')
        self.win_size = np.asarray(win_size).astype('int')
        self.pix_scale = float(pix_scale)

        # Initialize base class
        size = (self.win_size / self.pix_scale).astype('int')
        super().__init__(size, range_x, zoom_min, zoom_max, zoom_step)

        # Initialize a textured polygon
        temp_points = np.asarray([[0, 0], [0, self.size[1]], self.size, [self.size[0], 0]])
        self._set_polygon_buffer(temp_points)


    def add_framebuffer(self, fbo_name, gl_internalformat, gl_format, gl_type):
        if fbo_name in self.framebuffers.keys():
            self.framebuffers[fbo_name].delete()
        else:
            self.framebuffers[fbo_name] = Framebuffer(self.size, gl_internalformat, gl_format, gl_type)


    def delete_framebuffer(self, fbo_name):
        fbo = self.framebuffers.pop(fbo_name)
        fbo.delete()


    def _set_polygon_buffer(self, points_s):
        points_gl = self.s2gl(np.asarray(points_s).T)
        self.polygon = Polygon(points_gl.T)
        # Create polygon buffer and assign number of indices
        polygon_buffer_array = self.create_polygon_buffer_array(points_s)
        self.polygon_buffer_n_indices = polygon_buffer_array.shape[0]
        # Set polygon VBO and VAO
        self.polygon_buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.polygon_buffer)
        glBufferData(GL_ARRAY_BUFFER, polygon_buffer_array.nbytes, polygon_buffer_array, GL_DYNAMIC_DRAW)
        self.polygon_vao = glGenVertexArrays(1)
        glBindVertexArray(self.polygon_vao)
        # Enable VAO attributes
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 16, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 16, ctypes.c_void_p(8))


    def update_polygon_buffer(self, points_s):
        points_gl = self.s2gl(np.asarray(points_s).T)
        self.polygon = Polygon(points_gl.T)
        # Create polygon buffer and assign number of indices
        polygon_buffer_array = self.create_polygon_buffer_array(points_s)
        self.polygon_buffer_n_indices = polygon_buffer_array.shape[0]
        # Update buffer
        glBindBuffer(GL_ARRAY_BUFFER, self.polygon_buffer)
        glBufferData(GL_ARRAY_BUFFER, polygon_buffer_array.nbytes, polygon_buffer_array, GL_DYNAMIC_DRAW)


    def create_polygon_buffer_array(self, points_s):
        # Polygon triangulation from points in screen coordinates
        points_s = np.asarray(points_s)
        triangle_vertices = np.asarray(tripy.earclip(points_s))
        triangle_vertices = np.squeeze(triangle_vertices.reshape((1, -1, 2)))
        # Create texture coordinates
        triangle_vertices_gl = self.s2gl(triangle_vertices.T).T
        triangle_texture_vertices = triangle_vertices / self.size
        triangle_texture_vertices[:, 1] = 1.0 - triangle_texture_vertices[:, 1]  # Flip texture along y-axis
        return np.hstack((triangle_vertices_gl, triangle_texture_vertices)).astype('float32')


    def is_active(self):
        return self.polygon.contains(Point(self.s2gl(self.mouse_pos)))


    def resize(self, win_size, pix_scale):
        self.win_size = np.asarray(win_size).astype('int')
        self.pix_scale = float(pix_scale)
        temp_mouse_w = self.s2w(self.mouse_pos)
        # Update base class
        size = (self.win_size / self.pix_scale).astype('int')
        super().resize(size)
        self.mouse_pos = self.w2s(temp_mouse_w)
        # Update framebuffers
        for fbo in self.framebuffers.values():
            fbo.size = self.size
            fbo.update()

        # # TODO : Check how the visible polygon changes depending on the window size
        # # DEBUG - Update visible polygon
        # temp_points = np.asarray([[50, 50], [50, self.size[1]-50], self.size-50, [self.size[0]-50, 50]])
        # self.update_polygon_buffer(temp_points)


    def set_mouse_pos(self, mouse_pos):
        temp_mp_s = (np.asarray(mouse_pos) - self.pos) / self.pix_scale
        super().set_mouse_pos(temp_mp_s)


    def delete(self):
        glDeleteBuffers(1, [self.polygon_buffer])
        glDeleteVertexArrays(1, [self.polygon_vao])
        # Remove framebuffers
        for fbo in self.framebuffers.values():
            fbo.delete()

