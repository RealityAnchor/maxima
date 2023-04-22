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
    self.ocean_colour = (0, 0, 50)
    self.region_colour = (0,200,0)
    self.path_colour = (50, 50, 255)
    self.circle_radius = 4
    self.pi = 3.14159265358979324
    self.mouse_pressed = False
    self.total_regions = 256
    self.points = []
    self.min_x = self.max_x = self.min_y = self.max_y = 0
    self.connect_ratio = 4     # low = even spacing between regions (min 2)
    self.island_angularity = 8 # low = rounder island shape (min 1)
    self.max_path_length = float()
    self.longest_side = float()
    self.closest_points = []
    self.background_image = None
    self.generate_points()

  def distance(self, p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

  def generate_points(self):
    self.points = [(0,0)]
    while len(self.points) < self.total_regions:
      magnitude = 1 + random.random()*(self.connect_ratio-1)
      direction = random.random()*2*self.pi # in radians
      prev_point = random.choice(self.points[-1 - int(len(self.points)/self.island_angularity):]) # increase an offset var by 1 per failed loop to prevent getting stuck
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
      self.points[i] = (round(height_factor*(p[0] - self.min_x + x_offset) + self.circle_radius + 0.5*(self.screen_width - self.screen_height)),
                        round(height_factor*(p[1] - self.min_y + y_offset) + self.circle_radius))
    self.good_paths, self.bad_paths = self.calc_valid_paths()

  def calc_cosines(self, triangle):
    return ((-triangle[0]**2 + triangle[1]**2 + triangle[2]**2) / (2 * triangle[1] * triangle[2]),
            (-triangle[1]**2 + triangle[0]**2 + triangle[2]**2) / (2 * triangle[0] * triangle[2]),
            (-triangle[2]**2 + triangle[0]**2 + triangle[1]**2) / (2 * triangle[0] * triangle[1]))

  def calc_valid_paths(self):
    triangulation = Delaunay(self.points)
    good_paths = []
    bad_paths = []
    self.max_path_length = self.connect_ratio / self.longest_side * self.screen_height
    for p in triangulation.simplices:
      triangle_paths = [(p[0], p[1]), (p[0], p[2]), (p[1], p[2])]
      path_lengths = [self.distance(self.points[path[0]], self.points[path[1]]) for path in triangle_paths]
      for j, path in enumerate(triangle_paths):
        if not any(path == p for p in good_paths):
          if path_lengths[j] < self.max_path_length:
            good_paths.append(sorted((self.points[path[0]], self.points[path[1]])))
    for t in self.get_triangles(good_paths):
      cosines = self.calc_cosines((self.distance(t[0], t[1]), self.distance(t[0], t[2]), self.distance(t[1], t[2])))
      t_paths = [(t[0], t[1]), (t[0], t[2]), (t[1], t[2])]
      for n,c in enumerate(cosines):
        path = sorted(t_paths[n])
        if c <= -0.7:
          if not any(path == p for p in bad_paths):
            bad_paths.append(path)
          if any(path == p for p in good_paths):
            good_paths = [p for p in good_paths if p != path]
    return good_paths, bad_paths

  def get_triangles(self, good_paths):
      point_dict = {}
      for a, b in good_paths:
          if a not in point_dict:
              point_dict[a] = []
          if b not in point_dict:
              point_dict[b] = []
          if b not in point_dict[a]:
              point_dict[a].append(b)
          if a not in point_dict[b]:
              point_dict[b].append(a)
      triangle_list = []
      for p1 in point_dict:
          for p2 in point_dict[p1]:
              for p3 in point_dict[p2]:
                  if p3 in point_dict[p1]:
                      triangle = tuple(sorted([(p1[0], p1[1]), (p2[0], p2[1]), (p3[0], p3[1])]))
                      if triangle not in triangle_list:
                        triangle_list.append(triangle)
      return sorted(triangle_list)

  def render_background(self):
    if self.background_image:
      self.screen.blit(self.background_image, (0, 0))
    else:
      self.screen.fill((0,0,0))
      side_length = self.screen.get_height()
      border = pygame.Rect(0.5*(self.screen_width - self.screen_height), 0, side_length, side_length)
      ocean = pygame.Rect(0.5*(self.screen_width - self.screen_height), 0, side_length, side_length)
      pygame.draw.rect(self.screen, self.ocean_colour, ocean)
      terrain_colour = (0,50,0)
      for e in self.good_paths:
        pygame.draw.line(self.screen, terrain_colour, e[0], e[1], int(self.max_path_length))
        pygame.draw.circle(self.screen, terrain_colour, e[0], int(self.max_path_length/2))
        pygame.draw.circle(self.screen, terrain_colour, e[1], int(self.max_path_length/2))
      for e in self.bad_paths:
        pygame.draw.aaline(self.screen, (255,0,0), e[0], e[1])
      for e in self.good_paths:
        pygame.draw.aaline(self.screen, self.path_colour, e[0], e[1])
      pygame.draw.rect(self.screen, self.path_colour, border, 1)
      self.background_image = self.screen.copy()

  def render_points(self):
    for i, point in enumerate(self.points):
      if point in self.closest_points:
        if self.mouse_pressed:
          extra = 10
        else:
          extra = 5
        pygame.draw.circle(self.screen, self.region_colour, point, self.circle_radius+extra, 1)
        pygame.draw.aaline(self.screen, self.region_colour, point, pygame.mouse.get_pos())
      pygame.draw.circle(self.screen, self.region_colour, point, self.circle_radius)

  def handle_events(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.quit_game()
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          self.quit_game()
        elif event.key == pygame.K_SPACE:
          self.background_image = None
          self.generate_points()
          self.update_screen()
      elif event.type == pygame.MOUSEMOTION:
        mouse_xy = pygame.mouse.get_pos()
        closest_distances = sorted([self.distance(p, mouse_xy) for p in self.points])[:6]
        self.closest_points = [p for p in self.points if self.distance(p, mouse_xy) in closest_distances]
        self.update_screen()
      elif event.type == pygame.MOUSEBUTTONDOWN:
        self.mouse_pressed = True
        self.update_screen()
      elif event.type == pygame.MOUSEBUTTONUP:
        self.mouse_pressed = False
        self.update_screen()
          
  def update_screen(self):
    self.render_background()
    self.render_points()
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