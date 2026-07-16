import heapq
import pygame
import time

# ================= STATE =================
class State:    #State lưu vị trí agent và box, so sánh và hash, => key trong dictionary để theo dõi state đã đi và chi phí 
    
    def __init__(self, agent, boxes):   # constructor khởi tạo state
        self.agent = agent
        self.boxes = tuple(sorted(boxes))

    def __eq__(self, other):
        return self.agent == other.agent and self.boxes == other.boxes

    def __hash__(self):
        return hash((self.agent, self.boxes))
 
# ================= SOKOBAN =================
class Sokoban:  # map, hàm liên quan map
    def __init__(self, grid):   #constructor nhận vào grid map, sau đó parse map để xác định vị trí tường, agent, box và goal
        self.grid = grid
        self.walls = set()
        self.goals = set()
        self.init_agent = None
        self.init_boxes = []
        self.parse_map()
    #tạo grid map
    def parse_map(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                cell = self.grid[i][j]
                if cell == '%':
                    self.walls.add((i, j))
                elif cell == 'A':
                    self.init_agent = (i, j)
                elif cell == 'B':
                    self.init_boxes.append((i, j))
                elif cell == 'D':
                    self.goals.add((i, j))
                elif cell == 'C':
                    self.goals.add((i, j))
                    self.init_boxes.append((i, j))

    def is_goal(self, state):       #check nếu tất cả box đã ở vị trí goal thì trả về True, ngược lại trả về False
        return all(g in state.boxes for g in self.goals)

    def valid(self, pos):   #check pos có đụng tường không, nếu đụng trả về False, ngược lại trả về True
        return pos not in self.walls

# ================= SOLVER (A*) =================
class AStarSolver:
    def __init__(self, problem):    #load map solver
        self.problem = problem

    def heuristic(self, state):   #heuristic đơn giản: đếm số box chưa ở vị trí goal, càng nhiều box chưa ở goal thì càng xa mục tiêu
        h = 0
        for b in state.boxes:
            if b not in self.problem.goals:
                h += 1
        return h

    def is_deadlock(self, pos): #deadlock check: box deadlock (góc tường hoặc giữa 4 tường) mà không phải goal
        x, y = pos
        if pos in self.problem.goals:
            return False

        walls = self.problem.walls
        return (
            ((x-1,y) in walls and (x,y-1) in walls) or
            ((x-1,y) in walls and (x,y+1) in walls) or
            ((x+1,y) in walls and (x,y-1) in walls) or
            ((x+1,y) in walls and (x,y+1) in walls)
        )

    def apply_action(self, state, action):  #di chuyển, check hướng di chuyển của agent và box
        directions = {
            "North": (-1, 0),
            "South": (1, 0),
            "West": (0, -1),
            "East": (0, 1)
        }
        #gán direction theo action(hướng đi), sau đó tính new_agent dựa trên direction
        dx, dy = directions[action]
        ax, ay = state.agent
        new_agent = (ax + dx, ay + dy)

        if not self.problem.valid(new_agent):   #valid check dòng 46 (agent không đụng tường)
            return None

        new_boxes = list(state.boxes)

        if new_agent in state.boxes:
            bx, by = new_agent
            new_box = (bx + dx, by + dy)

            if not self.problem.valid(new_box): return None #valid check dòng 46 (box không đụng tường)
            if new_box in state.boxes: return None  #check không đụng box khác

            new_boxes.remove((bx, by))
            new_boxes.append(new_box)

        return State(new_agent, new_boxes)  # return new state sau khi apply action thõa mãn

    def solve(self):
        start_time = time.time()    # timer của question 8
        start = State(self.problem.init_agent, self.problem.init_boxes) # input state ban đầu từ map

        open_list = []  # priority queue cho A*, lưu (f, g, counter, state, path), f = g + h
        counter = 0     # counter++ mỗi khi push vào open_list, đảm bảo thứ tự push vào được giữ nguyên khi f và g bằng nhau, tie-breaking khi f và g bằng nhau
        heapq.heappush(open_list, (0, 0, counter, start, []))   #push begin state 

        visited = {}    # dictionary theo dõi state đã đi và chi phí g(n) thấp nhất, key là state, value là g(n)
        nodes_expanded = 0  # đếm số node đã mở rộng
        max_frontier = 1    # đánh giá bộ nhớ

        while open_list:    
            f, g, _, state, path = heapq.heappop(open_list)     
            nodes_expanded += 1 

            if self.problem.is_goal(state): # check done => in kết quả
                elapsed = time.time() - start_time
                print("Time:", round(elapsed, 6))
                print("Nodes expanded:", nodes_expanded)
                print("Max frontier size:", max_frontier)
                print("Solution length:", len(path))
                return path

            if state in visited and visited[state] <= g:    # nếu state bị lặp lại với chi phí g(n) cao hơn hoặc bằng => bỏ qua
                continue

            visited[state] = g  # cập nhật chi phí g(n) thấp nhất cho state

            for action in ["North", "South", "West", "East"]:
                new_state = self.apply_action(state, action)
                if not new_state: continue

                if any(self.is_deadlock(b) for b in new_state.boxes):
                    continue

                new_g = g + 1
                new_f = new_g + self.heuristic(new_state)

                counter += 1
                heapq.heappush(open_list, (new_f, new_g, counter, new_state, path + [action]))  #push new state vào open_list với f, g, counter, state và path đã cập nhật

            max_frontier = max(max_frontier, len(open_list))

        print("No solution found")
        return []

# ================= GAME UI =================
class GameUI:
    def __init__(self, game):
        pygame.init()

        self.game = game
        self.state = State(game.init_agent, game.init_boxes)
        self.solver = AStarSolver(game)

        self.TILE = 50
        self.MAP_W = len(game.grid[0]) * self.TILE
        self.MAP_H = len(game.grid) * self.TILE
        self.SIDEBAR_W = 220

        self.screen = pygame.display.set_mode((self.MAP_W + self.SIDEBAR_W, self.MAP_H))
        self.font = pygame.font.SysFont(None, 30)

        self.load_assets()
        self.init_ui()

    def load_assets(self):
        self.agent_img = pygame.transform.scale(pygame.image.load("assets/agent.png"), (self.TILE, self.TILE))
        self.box_img = pygame.transform.scale(pygame.image.load("assets/box.png"), (self.TILE, self.TILE))
        self.box_goal_img = pygame.transform.scale(pygame.image.load("assets/box_on_goal.png"), (self.TILE, self.TILE))
        self.wall_img = pygame.transform.scale(pygame.image.load("assets/wall.png"), (self.TILE, self.TILE))
        self.goal_img = pygame.transform.scale(pygame.image.load("assets/goal.png"), (self.TILE, self.TILE))
        self.floor_img = pygame.transform.scale(pygame.image.load("assets/floor.png"), (self.MAP_W, self.MAP_H))

    def init_ui(self):
        self.auto_mode = False
        self.solution = []
        self.step_index = 0
        self.move_count = 0
        self.best_move = None
        self.show_popup = False
        self.last_step_time = 0
        self.step_delay = 200

        self.btn_reset = pygame.Rect(self.MAP_W + 20, 40, 180, 50)
        self.btn_mode = pygame.Rect(self.MAP_W + 20, 110, 180, 50)

        self.btn_quit = pygame.Rect(self.MAP_W//2 - 90, self.MAP_H//2 + 70, 180, 45)
        self.btn_popup_reset = pygame.Rect(self.MAP_W//2 - 90, self.MAP_H//2 + 130, 180, 45)

    def reset(self):
        self.state = State(self.game.init_agent, self.game.init_boxes)
        self.move_count = 0
        self.auto_mode = False
        self.show_popup = False
        self.solution = []
        self.step_index = 0

    def toggle_ai(self):
        # toggle ON/OFF instead of always ON
        if self.auto_mode:
            # turn OFF -> back to manual (keep current state)
            self.auto_mode = False
            self.solution = []
            self.step_index = 0
        else:
            # turn ON -> reset then run AI
            self.reset()
            self.auto_mode = True
            self.solution = self.solver.solve()
            self.step_index = 0

    def draw(self):
        self.screen.blit(self.floor_img, (0, 0))

        for i in range(len(self.game.grid)):
            for j in range(len(self.game.grid[i])):
                x, y = j*self.TILE, i*self.TILE

                if (i,j) in self.game.walls:
                    self.screen.blit(self.wall_img,(x,y)); continue

                if (i,j) in self.game.goals:
                    self.screen.blit(self.goal_img,(x,y))

                if (i,j) in self.state.boxes:
                    img = self.box_goal_img if (i,j) in self.game.goals else self.box_img
                    self.screen.blit(img,(x,y))

                if (i,j) == self.state.agent:
                    self.screen.blit(self.agent_img,(x,y))

    def draw_button(self, rect, text, color):
        pygame.draw.rect(self.screen, color, rect, border_radius=10)
        label = self.font.render(text, True, (0,0,0))
        self.screen.blit(label, label.get_rect(center=rect.center))

    def draw_sidebar(self):
        pygame.draw.rect(self.screen,(30,30,30),(self.MAP_W,0,self.SIDEBAR_W,self.MAP_H))

        self.draw_button(self.btn_reset, "RESET", (120,170,255))

        mode_color = (255,80,80) if self.auto_mode else (120,255,140)
        mode_text = "AI MODE" if self.auto_mode else "MANUAL"
        self.draw_button(self.btn_mode, mode_text, mode_color)

        self.screen.blit(self.font.render(f"Moves: {self.move_count}",True,(255,255,0)),(self.MAP_W+20,200))

        best_text = f"Best Move: {self.best_move}" if self.best_move else "Best Move: _"
        self.screen.blit(self.font.render(best_text,True,(0,255,255)),(self.MAP_W+20,240))

        self.screen.blit(self.font.render("use arrow keys",True,(255,255,255)),(self.MAP_W+20,280))
        self.screen.blit(self.font.render("to move",True,(255,255,255)),(self.MAP_W+20,300))
    def update(self):
        now = pygame.time.get_ticks()   # tạo tickrate

        if self.auto_mode and self.step_index < len(self.solution): # bật auto mode && còn action trong solution thì do/tickrate
            if now - self.last_step_time > self.step_delay: 
                action = self.solution[self.step_index] # lấy action tiếp theo trong solution
                new_state = self.solver.apply_action(self.state, action)
                if new_state:   # nếu action hợp lệ thì cập nhật state và move_count
                    self.state = new_state
                    self.move_count += 1
                self.step_index += 1    # tăng step_index để chuyển sang action tiếp theo trong solution
                self.last_step_time = now # cập nhật thời gian của step cuối cùng để tạo delay giữa các step, tránh chạy quá nhanh
        # UI
        if self.game.is_goal(self.state):
            self.show_popup = True
            if self.best_move is None or self.move_count < self.best_move:
                self.best_move = self.move_count

    def draw_popup(self):
        overlay = pygame.Surface((self.MAP_W, self.MAP_H))
        overlay.set_alpha(180)
        overlay.fill((0,0,0))
        self.screen.blit(overlay, (0,0))

        title = self.font.render("YOU WIN!", True, (255,255,255))
        score = self.font.render(f"Moves: {self.move_count}", True, (255,255,0))
        best = self.font.render(f"Best Move: {self.best_move}", True, (0,255,255))

        self.screen.blit(title, title.get_rect(center=(self.MAP_W//2, self.MAP_H//2 - 50)))
        self.screen.blit(score, score.get_rect(center=(self.MAP_W//2, self.MAP_H//2)))
        self.screen.blit(best, best.get_rect(center=(self.MAP_W//2, self.MAP_H//2 + 40)))

        self.draw_button(self.btn_quit, "QUIT", (255,80,80))
        self.draw_button(self.btn_popup_reset, "RESET", (120,200,255))

    def run(self): #main part
        clock = pygame.time.Clock() 
        running = True

        while running:  #main loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:    # check button 
                    if self.show_popup: # popup button
                        if self.btn_quit.collidepoint(event.pos):
                            running = False
                        if self.btn_popup_reset.collidepoint(event.pos):
                            self.reset()
                    else:
                        if self.btn_reset.collidepoint(event.pos):
                            self.reset()
                        if self.btn_mode.collidepoint(event.pos):
                            self.toggle_ai()

                if event.type == pygame.KEYDOWN and not self.auto_mode and not self.show_popup: # control
                    key_map = {
                        pygame.K_UP: "North",
                        pygame.K_DOWN: "South",
                        pygame.K_LEFT: "West",
                        pygame.K_RIGHT: "East"
                    }
                    if event.key in key_map:
                        new_state = self.solver.apply_action(self.state, key_map[event.key])
                        if new_state:
                            self.state = new_state
                            self.move_count += 1

            self.update() 
            #draw UI
            self.screen.fill((0,0,0))
            self.draw()
            self.draw_sidebar()

            if self.show_popup:
                self.draw_popup()

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

# ================= MAIN =================
def load_map(file):
    with open(file) as f:
        return [list(line.strip()) for line in f]

if __name__ == "__main__":
    grid = load_map("example_map.txt")
    game = Sokoban(grid)
    GameUI(game).run()
