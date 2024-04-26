import numpy as np
import random
import glfw
from OpenGL.GL import *

# Global variables for window dimensions and particles
window_width, window_height = 800, 600
particles = []

def initialize_particles():
    bottle_radius = 0.5
    bottle_height = 1.5
    return [{'x': random.uniform(-bottle_radius, bottle_radius),
             'y': random.uniform(-bottle_height / 2, bottle_height / 2),
             'z': random.uniform(-bottle_radius, bottle_radius),
             'dx': 0, 'dy': -0.01, 'dz': 0} for _ in range(10000)]
def update_particles():
    global particles
    damping = 0.98  # Damping factor to simulate fluid viscosity
    bottle_radius = 0.5
    bottle_height = 1.5
    for particle in particles:
        # Apply gravity and damping
        particle['dy'] += -0.001
        particle['dx'] *= damping
        particle['dy'] *= damping
        particle['dz'] *= damping
        
        # Update position
        particle['x'] += particle['dx']
        particle['y'] += particle['dy']
        particle['z'] += particle['dz']

        # Collision and reflection
        if np.sqrt(particle['x']**2 + particle['z']**2) > bottle_radius:
            normal = np.array([particle['x'], 0, particle['z']])
            normal /= np.linalg.norm(normal)
            velocity = np.array([particle['dx'], particle['dy'], particle['dz']])
            reflection = velocity - 2 * np.dot(velocity, normal) * normal
            particle['dx'], particle['dz'] = reflection[0], reflection[2]
        if particle['y'] < -bottle_height / 2:
            particle['y'] = -bottle_height / 2
            particle['dy'] *= -0.5


def mouse_button_callback(window, button, action, mods):
    if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
        x, y = glfw.get_cursor_pos(window)
        increase_pressure_near(x, y)

def increase_pressure_near(x, y):
    # Convert screen coordinates to OpenGL coordinates
    opengl_x = (x / window_width) * 2 - 1
    opengl_y = 1 - (y / window_height) * 2

    # Parameters for interaction
    radius = 0.2  # Increased radius for a broader effect
    pressure_effect = 0.2  # Increase the effect to make it more noticeable

    # Interaction with particles
    global particles
    for particle in particles:
        dx, dy = particle['x'] - opengl_x, particle['y'] - opengl_y
        distance = np.sqrt(dx**2 + dy**2)
        if distance < radius:
            direction = np.array([dx, dy])
            direction /= np.linalg.norm(direction) if np.linalg.norm(direction) != 0 else 1
            # Apply the pressure effect inversely proportional to distance
            magnitude = (1 - distance / radius) * pressure_effect
            particle['dx'] -= direction[0] * magnitude
            particle['dy'] -= direction[1] * magnitude


def render_particles():
    global particles
    glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_POINTS)
    for particle in particles:
        glVertex3f(particle['x'], particle['y'], particle['z'])
    glEnd()

def main():
    global window_width, window_height, particles
    if not glfw.init():
        return
    window = glfw.create_window(window_width, window_height, "Fluid Simulation", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_mouse_button_callback(window, mouse_button_callback)
    particles = initialize_particles()
    while not glfw.window_should_close(window):
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        update_particles()
        render_particles()
        glfw.swap_buffers(window)
    glfw.terminate()

if __name__ == "__main__":
    main()
