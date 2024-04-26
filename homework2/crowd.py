import glfw
from OpenGL.GL import *
from math import sin, cos, pi
import random
import numpy as np

# Parameters for fluid-like behavior
viscosity = 0.01
interaction_radius = 0.1
pressure_strength = 0.01
num_particles = 100

# Initialize particles
particles = [{'x': random.uniform(-1, 1), 'y': random.uniform(-1, 1), 'radius': 0.02,
              'dx': random.uniform(-0.01, 0.01), 'dy': random.uniform(-0.01, 0.01)}
             for _ in range(num_particles)]

def update_positions():
    global particles
    for particle in particles:
        # Apply basic motion physics
        particle['x'] += particle['dx']
        particle['y'] += particle['dy']

        # Boundary condition with wrapping
        if particle['x'] > 1.0: particle['x'] = -1.0
        if particle['x'] < -1.0: particle['x'] = 1.0
        if particle['y'] > 1.0: particle['y'] = -1.0
        if particle['y'] < -1.0: particle['y'] = 1.0

        # Reset velocities (for simplicity in demonstration)
        particle['dx'], particle['dy'] = 0, 0

    # Apply fluid dynamics
    apply_fluid_dynamics()

def apply_fluid_dynamics():
    global particles
    # Calculate forces based on interaction
    for i, particle in enumerate(particles):
        force_x, force_y = 0, 0
        for j, other in enumerate(particles):
            if i != j:
                dx, dy = other['x'] - particle['x'], other['y'] - particle['y']
                dist = np.sqrt(dx**2 + dy**2)
                if dist < interaction_radius:
                    # Apply simple pressure and viscosity
                    force_x += dx / dist * pressure_strength
                    force_y += dy / dist * pressure_strength

        # Update velocities based on computed forces
        particle['dx'] -= viscosity * force_x
        particle['dy'] -= viscosity * force_y

def draw_circle(x, y, radius, color):
    num_segments = 50
    glColor3fv(color)
    glBegin(GL_POLYGON)
    for i in range(num_segments):
        theta = 2.0 * pi * i / num_segments
        dx = radius * cos(theta)
        dy = radius * sin(theta)
        glVertex2f(x + dx, y + dy)
    glEnd()

def main():
    if not glfw.init():
        raise Exception("GLFW can't be initialized")

    window = glfw.create_window(640, 480, "Fluid Simulation", None, None)
    if not window:
        glfw.terminate()
        raise Exception("GLFW window can't be created")

    glfw.make_context_current(window)
    glClearColor(0.870, 0.905, 0.937, 1)  

    while not glfw.window_should_close(window):
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()

        update_positions()  

        for particle in particles:
            draw_circle(particle['x'], particle['y'], particle['radius'], (0.0, 0.0, 1.0))

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
