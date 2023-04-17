import pygame
import random
import math
from scipy.spatial import Delaunay

class IslandGenerator:
  def __init__(self):
    pygame.display.set_caption('Maxima')
    self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    self.screen_width = self.screen.get_width()
    self.screen_height = self.screen.get_height()
    self.background_color = (0, 0, 0)
    self.circle_color = (255, 255, 255)
    self.edge_color = (50, 50, 255)
    self.circle_radius = 3
    self.pi = 3.14159265358979324
    self.max_points = 256
    self.points = [(0,0)]
    self.min_x = self.max_x = self.min_y = self.max_y = 0
    self.connect_ratio = 4     # low = even spacing between regions (min 2)
    self.island_angularity = 8 # low = rounder island shape (min 1)
    self.longest_side = None
    self.closest_points = []
    self.generate_points()

  def distance(self, p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

  def generate_points(self):
    self.points = [(0,0)]
    while len(self.points) < self.max_points:
      magnitude = 1 + random.random()*(self.connect_ratio-1)
      direction = random.random()*2*self.pi # in radians
      prev_point = random.choice(self.points[-1 - int(len(self.points)/self.island_angularity):])
      x = prev_point[0] + magnitude*math.cos(direction)
      y = prev_point[1] + magnitude*math.sin(direction)
      for p in self.points:
        if self.distance((x,y), p) < 1:
          break
      else:
        self.points.append((x,y))
    self.min_x = min([p[0] for p in self.points])
    self.max_x = max([p[0] for p in self.points])
    self.min_y = min([p[1] for p in self.points])
    self.max_y = max([p[1] for p in self.points])
    self.longest_side = max(abs(self.min_x-self.max_x), abs(self.min_y-self.max_y))
    x_offset = (self.longest_side - abs(self.min_x-self.max_x)) / 2
    y_offset = (self.longest_side - abs(self.min_y-self.max_y)) / 2
    height_factor = (self.screen_height - 2*self.circle_radius) / self.longest_side
    for i,p in enumerate(self.points):
      self.points[i] = (round(height_factor*(p[0] - self.min_x + x_offset)) + self.circle_radius + 0.5*(self.screen_width - self.screen_height),
                        round(height_factor*(p[1] - self.min_y + y_offset) + self.circle_radius))
    self.triangle_edges = self.calc_edges()

  def calc_cosines(self, sides):
    return [(-sides[0]**2 + sides[1]**2 + sides[2]**2) / (2 * sides[1] * sides[2])
          , (-sides[1]**2 + sides[0]**2 + sides[2]**2) / (2 * sides[0] * sides[2])
          , (-sides[2]**2 + sides[0]**2 + sides[1]**2) / (2 * sides[0] * sides[1])]

  def calc_edges(self):
    triangulation = Delaunay(self.points, incremental=True)
    edges = []
    for i, p in enumerate(triangulation.simplices):
      triangle_indices = [(p[0], p[1]), (p[0], p[2]), (p[1], p[2])]
      edge_lengths = [self.distance(self.points[edge[0]], self.points[edge[1]]) for edge in triangle_indices]
      # the two lines below should remove edges opposite very obtuse angles, but it's buggy
      # cosines = self.calc_cosines(edge_lengths)
      # triangle_indices = [edge for k,edge in enumerate(triangle_indices) if cosines[k] > -0.8]
      for j, edge in enumerate(triangle_indices):
        if sorted(edge) not in edges:
          max_length = self.connect_ratio / self.longest_side * self.screen_height
          if edge_lengths[j] <= max_length:
            edges.append(edge)
    return edges

  def render_points(self):
    for i, point in enumerate(self.points):
      if point in self.closest_points:
        color = (50, 255, 50)
        pygame.draw.circle(self.screen, color, point, self.circle_radius+5, 1)
        pygame.draw.line(self.screen, color, point, pygame.mouse.get_pos())
      else:
        color = self.circle_color
      pygame.draw.circle(self.screen, color, point, self.circle_radius)

  def render_edges(self):
    for e in self.triangle_edges:
      pygame.draw.line(self.screen, self.edge_color, self.points[e[0]], self.points[e[1]])

  def render_border(self):
    side_length = self.screen.get_height()
    border_rect = pygame.Rect(0.5*(self.screen_width - self.screen_height), 0, side_length, side_length)
    pygame.draw.rect(self.screen, '#ffffff', border_rect, 1)

  def handle_events(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.quit_game()
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          self.quit_game()
        elif event.key == pygame.K_SPACE:
          self.generate_points()
          self.update_screen()
      elif event.type == pygame.MOUSEMOTION:
        mouse_xy = pygame.mouse.get_pos()
        closest_distances = sorted([self.distance(p, mouse_xy) for p in self.points])[:3]
        self.closest_points = [p for p in self.points if self.distance(p, mouse_xy) in closest_distances]
        self.update_screen()
          
  def update_screen(self):
    self.screen.fill(self.background_color)
    self.render_edges()
    self.render_points()
    self.render_border()
    pygame.display.flip()

  def quit_game(self):
    pygame.quit()
    exit()

  def run(self):
    clock = pygame.time.Clock()
    self.update_screen()
    while True:
      self.handle_events()
      clock.tick(60)
      pygame.display.update()

if __name__ == '__main__':
  generator = IslandGenerator()
  generator.run()