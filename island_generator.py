import pygame
import random
import math
from scipy.spatial import Delaunay

class IslandGenerator:
  def __init__(self):
    self.screen_width = 1366
    self.screen_height = 768
    self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
    self.background_color = (0, 0, 0)
    self.circle_color = (255, 255, 255)
    self.circle_radius = 3
    self.pi = 3.14159265358979324
    self.max_points = 256
    self.points = [(0,0)]
    self.min_x = self.max_x = self.min_y = self.max_y = 0
    self.connect_ratio = 5
    self.longest_side = None
    self.regenerate_points()

  def distance(self, p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

  def regenerate_points(self):
    self.points = [(0,0)]
    while len(self.points) < self.max_points:
      magnitude = 1 + random.random()*(self.connect_ratio-1)
      direction = random.random()*2*self.pi # in radians
      prev_point = random.choice(self.points[-int(len(self.points)/3):]) # from the most recent 1/3 points
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

  def find_edges(self):
    # Compute Delaunay triangulation
    triangulation = Delaunay(self.points)
    # Extract edges from triangulation
    edges = []
    for v in triangulation.simplices:
      triangle = [(v[0], v[1]), (v[0], v[2]), (v[1], v[2])]
      for edge in triangle:
        if sorted(edge) not in edges:
          if round(self.distance(self.points[edge[0]], self.points[edge[1]])) < self.connect_ratio / self.longest_side * self.screen_height:
            edges.append(edge)
    return edges

  def update_screen(self):
    self.screen.fill(self.background_color)
    delaunay_edges = self.find_edges()
    for e in delaunay_edges:
      pygame.draw.line(self.screen, '#7777ff', self.points[e[0]], self.points[e[1]])
    for i, point in enumerate(self.points):
      pygame.draw.circle(self.screen, self.circle_color, point, self.circle_radius)
    pygame.draw.rect(self.screen, "#ffffff", pygame.Rect(0.5*(self.screen_width - self.screen_height), 0, self.screen_height, self.screen_height), 1)
    pygame.display.flip()

  def run(self):
    running = True
    while running:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
          self.regenerate_points()
      self.update_screen()

if __name__ == '__main__':
  pygame.init()
  generator = IslandGenerator()
  generator.run()