import pygame as pg

pg.init()

c1, c2, c3 = (None,) * 3
m1, m2, m3 = (None,) * 3

cannibals_left = [c1, c2, c3]
missionaries_left = [m1, m2, m3]

cannibals_right = []
missionaries_right = []

screen = pg.display.set_mode((1200, 700))
screen_rect = screen.get_rect()
shipsheet = pg.image.load('shipsheet.png').convert_alpha()
cannibalSheet = pg.image.load('sprites.png').convert_alpha()


def strip_from_sheet(sheet, start, size, columns, rows):
    frames = []
    for j in range(rows):
        for i in range(columns):
            location = (start[0] + size[0] * i, start[1] + size[1] * j)
            frames.append(sheet.subsurface(pg.Rect(location, size)))
    return frames


class Cannibal:
    def __init__(self, sheet, screen_rect):
        self.screen_rect = screen_rect
        self.all_frames = strip_from_sheet(sheet, (0, 0), (615 / 12, 573 / 8), 12, 8)
        self.setup_frames()
        self.direction = 'right'
        self.ani_delay = 100
        self.ani_timer = 0.0
        self.ani_index = 0
        self.image = self.frames[self.direction][self.ani_index]
        self.isWalking = False
        self.isDriving = False
        self.speed = 5
        self.rect = self.image.get_rect(center=self.screen_rect.center)
        self.animate()

    def setup_frames(self):
        self.frames = {
            'down': self.all_frames[9:],
            'left': self.all_frames[21:24],
            'right': self.all_frames[33:36],
            'up': self.all_frames[12:16]
        }

    def animate(self):
        if pg.time.get_ticks() - self.ani_timer > self.ani_delay:
            self.ani_timer = pg.time.get_ticks()
            self.image = self.frames[self.direction][self.ani_index]
            if self.isWalking and not self.isDriving:
                self.isWalking = False
                if self.ani_index == len(self.frames[self.direction]) - 1:
                    self.ani_index = 0
                else:
                    self.ani_index += 1

    def get_event(self, event):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Missionary:
    def __init__(self, sheet, screen_rect):
        self.frames = None
        self.screen_rect = screen_rect
        self.all_frames = strip_from_sheet(sheet, (0, 0), (615 / 12, 573 / 8), 12, 8)
        self.setup_frames()
        self.direction = 'right'
        self.ani_delay = 100
        self.ani_timer = 0.0
        self.ani_index = 0
        self.image = self.frames[self.direction][self.ani_index]
        self.isWalking = False
        self.isDriving = False
        self.speed = 5
        self.rect = self.image.get_rect(center=self.screen_rect.center)
        self.animate()

    def setup_frames(self):
        self.frames = {
            # 'down': self.all_frames[9:],
            'left': self.all_frames[60:63],
            'right': self.all_frames[72:75],
            'up': self.all_frames[72:75]
        }

    def animate(self):
        if pg.time.get_ticks() - self.ani_timer > self.ani_delay:
            self.ani_timer = pg.time.get_ticks()
            self.image = self.frames[self.direction][self.ani_index]
            if self.isWalking and not self.isDriving:
                self.isWalking = False
                if self.ani_index == len(self.frames[self.direction]) - 1:
                    self.ani_index = 0
                else:
                    self.ani_index += 1

    def get_event(self, event):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Ship:
    def __init__(self, sheet, screen_rect):
        self.frames = None
        self.screen_rect = screen_rect
        self.all_frames = strip_from_sheet(sheet, (0, 0), (122.5, 164.5), 4, 4)
        self.setup_frames()
        self.direction = 'right'
        self.isMoving = False
        self.ani_delay = 100
        self.ani_timer = 0.0
        self.ani_index = 0
        self.image = self.frames[self.direction][self.ani_index]

        self.speed = 5
        self.rect = self.image.get_rect(center=self.screen_rect.center)

    def setup_frames(self):
        self.frames = {
            'down': self.all_frames[:4],
            'left': self.all_frames[4:8],
            'right': self.all_frames[8:12],
            'up': self.all_frames[12:16]
        }

    def animate(self):
        if pg.time.get_ticks() - self.ani_timer > self.ani_delay:
            self.ani_timer = pg.time.get_ticks()
            self.image = self.frames[self.direction][self.ani_index]
            if self.isMoving:
                self.isMoving = False
                if self.ani_index == len(self.frames[self.direction]) - 1:
                    self.ani_index = 0
                else:
                    self.ani_index += 1

    def get_event(self, event):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)


done = False
clock = pg.time.Clock()
ship = Ship(shipsheet, screen_rect)
ship.rect.x = ship.screen_rect.width / 4

diff = 0
for i in range(len(cannibals_left)):
    cannibals_left[i] = Cannibal(cannibalSheet, screen_rect)
    cannibals_left[i].rect.x = ship.screen_rect.width / 4 - 100 - diff
    diff += 50

diff = 0
for i in range(len(missionaries_left)):
    missionaries_left[i] = Missionary(cannibalSheet, screen_rect)
    missionaries_left[i].rect.x = ship.screen_rect.width / 4 - 100 - diff
    missionaries_left[i].rect.y = ship.screen_rect.height / 2 + 70
    diff += 50

moved = 0
no_driver = True
index = 1
solution = [(3, 3, 1), (2, 2, 0), (3, 2, 1), (3, 0, 0), (3, 1, 1), (1, 1, 0), (2, 2, 1), (0, 2, 0), (0, 3, 1),
            (0, 1, 0), (1, 1, 1), (0, 0, 0)]
nb_m, nb_c, boat = (0,) * 3

drivers = []
start_driving = False
EOP = False
con1, con2, con3, con4 = (False,)*4
reiterate = False
gap = 50

while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        ship.get_event(event)

    # ship.update

    screen.fill((0, 0, 0))

    # pg.draw.rect(screen,(0,0,255), (screen_rect.x, screen_rect.y, screen_rect.width, screen_rect.height))
    ship.draw(screen)

    # display missionaries and cannibals on both sides
    for cannibal in cannibals_left:
        cannibal.animate()
        cannibal.draw(screen)

    for missionary in missionaries_left:
        missionary.animate()
        missionary.draw(screen)

    for cannibal in cannibals_right:
        cannibal.animate()
        cannibal.draw(screen)

    for missionary in missionaries_right:
        missionary.animate()
        missionary.draw(screen)

    if nb_m == 0 and nb_c == 0 and not EOP:
        nb_m = abs(len(missionaries_left) - solution[index][0])
        nb_c = abs(len(cannibals_left) - solution[index][1])
        boat = solution[index][2]

        if boat == 0:
            if nb_m != 0:
                if nb_m == 1:
                    drivers.append(missionaries_left[0])
                    if nb_c == 1:
                        drivers.append(cannibals_left[0])
                    else:
                        drivers.append(None)
                else:
                    drivers.append(missionaries_left[0])
                    drivers.append(missionaries_left[1])
            else:
                if nb_c == 1:
                    drivers.append(cannibals_left[0])
                    drivers.append(None)
                else:
                    drivers.append(cannibals_left[0])
                    drivers.append(cannibals_left[1])
        else:
            if(index == 6):

                print(solution[index])
                print(nb_m)
                print(nb_c)

            if nb_m != 0:
                if nb_m == 1:
                    drivers.append(missionaries_right[0])
                    if nb_c == 1:
                        drivers.append(cannibals_right[0])
                    else:
                        drivers.append(None)
                else:
                    drivers.append(missionaries_right[0])
                    drivers.append(missionaries_right[1])
            else:
                if nb_c == 1:
                    drivers.append(cannibals_right[0])
                    drivers.append(None)
                else:
                    drivers.append(cannibals_right[0])
                    drivers.append(cannibals_right[1])

        # here
    driver1, driver2 = drivers
    if nb_m != 0 or nb_c != 0 and not EOP:

        # boat is on the will go to the right side
        if boat == 0:
            if driver1.rect.x <= ship.rect.x + 10:
                driver1.isWalking = True
                driver1.animate()
                driver1.direction = 'right'
                driver1.rect.clamp_ip(driver1.screen_rect)
                driver1.rect.x += driver1.speed
            else:
                con1 = True

            if driver2 is not None:
                if driver2.rect.x <= ship.rect.x + 10:
                    driver2.isWalking = True
                    driver2.direction = 'right'
                    driver2.animate()
                    driver2.rect.clamp_ip(driver2.screen_rect)
                    driver2.rect.x += driver2.speed
                else:
                    con2 = True
            else:
                con2 = True

            if driver1.rect.y > ship.rect.y + 40:
                driver1.isWalking = True
                driver1.direction = 'up'
                driver1.animate()
                driver1.rect.clamp_ip(driver1.screen_rect)
                driver1.rect.y -= driver1.speed
            else:
                con3 = True

            if driver2 is not None:
                if driver2.rect.y > ship.rect.y + 40:
                    driver2.isWalking = True
                    driver1.direction = 'up'
                    driver2.animate()
                    driver2.rect.clamp_ip(driver2.screen_rect)
                    driver2.rect.y -= driver2.speed
                else:
                    con4 = True

            start_driving = con1 and con2 and con3 and con4

        else:
            if driver1.rect.x > ship.rect.x + 50:

                driver1.isWalking = True
                driver1.animate()
                driver1.direction = 'left'
                driver1.rect.clamp_ip(driver1.screen_rect)
                driver1.rect.x -= driver1.speed
            else:
                con1 = True

            if driver2 is not None:
                print(driver2.rect.x)
                print(ship.rect.x)
                if driver2.rect.x > ship.rect.x:

                    driver2.direction = 'left'
                    driver2.isWalking = True
                    driver2.animate()
                    driver2.rect.clamp_ip(driver2.screen_rect)
                    driver2.rect.x -= driver2.speed
                else:
                    con2 = True
                    pass
            else:
                con2 = True

            con3 = True
            con4 = True

            start_driving = con1 and con2 and con3 and con4

        if start_driving:
            no_driver = False
            driver1.isWalking = False
            driver1.isDriving = True

            if driver2 is not None:
                driver2.isWalking = False
                driver2.isDriving = True

            if moved < 80 and not no_driver:
                ship.isMoving = True
                ship.animate()
                ship.rect.clamp_ip(ship.screen_rect)
                if boat == 0:
                    ship.direction = 'right'
                    ship.rect.x += ship.speed
                else:
                    ship.direction = 'left'
                    ship.rect.x -= ship.speed
                moved += 1
            # ship is no longer moving
            else:
                ship.direction = 'left'
                ship.animate()
                if boat == 0:
                    if driver1.rect.x - 300 <= ship.rect.x:
                        driver1.isWalking = True
                        driver1.animate()
                        driver1.isDriving = False
                        driver1.rect.clamp_ip(driver1.screen_rect)
                        driver1.rect.x += driver1.speed
                    else:
                        reiterate = True
                        driver1.direction = 'left'
                        driver1.isWalking = False
                    if driver2 is not None:
                        reiterate = False
                        if driver2.rect.x - 200 <= ship.rect.x:
                            driver2.isWalking = True
                            driver2.isDriving = False
                            driver2.animate()
                            driver2.rect.clamp_ip(driver2.screen_rect)
                            driver2.rect.x += driver2.speed
                        else:
                            reiterate = True
                            driver2.direction = 'left'
                            driver2.isWalking = False

                else:

                    if driver1.rect.x >= ship.rect.x - 150 - gap:
                        driver1.isWalking = True
                        driver1.animate()
                        driver1.isDriving = False
                        driver1.rect.clamp_ip(driver1.screen_rect)
                        driver1.rect.x -= driver1.speed

                    else:
                        gap = - (gap + 20)
                        reiterate = True
                        driver1.direction = 'right'
                        driver1.isWalking = False
                    if driver2 is not None:
                        reiterate = False
                        if driver2.rect.x >= ship.rect.x - 200 - gap:
                            driver2.isWalking = True
                            driver2.isDriving = False
                            driver2.animate()
                            driver2.rect.clamp_ip(driver2.screen_rect)
                            driver2.rect.x -= driver2.speed
                        else:
                            gap = - (gap - 20)
                            reiterate = True
                            driver2.direction = 'right'
                            driver2.isWalking = False

                if reiterate:
                    if index < len(solution) - 1:
                        index += 1
                        start_driving = False
                        nb_m, nb_c = (0,)*2
                        moved = 0
                        con1, con2, con3, con4 = (False,)*4

                        if boat == 0:
                            if isinstance(driver1, Missionary):
                                missionaries_right.append(driver1)
                                missionaries_left.remove(driver1)
                            else:
                                cannibals_right.append(driver1)
                                cannibals_left.remove(driver1)

                            if driver2 is not None:
                                if isinstance(driver2, Missionary):
                                    missionaries_right.append(driver2)
                                    missionaries_left.remove(driver2)
                                else:
                                    cannibals_right.append(driver2)
                                    cannibals_left.remove(driver2)
                        else:
                            if isinstance(driver1, Missionary):
                                missionaries_left.append(driver1)
                                missionaries_right.remove(driver1)
                            else:
                                cannibals_left.append(driver1)
                                cannibals_right.remove(driver1)
                            if driver2 is not None:
                                if isinstance(driver2, Missionary):
                                    missionaries_left.append(driver2)
                                    missionaries_right.remove(driver2)
                                else:
                                    cannibals_left.append(driver2)
                                    cannibals_right.remove(driver2)
                        drivers.clear()
                        reiterate = False
                    else:
                        print('heeeeeeeeeeeeey')
                        EOP = True
        else:
            if index >= len(solution) - 1:
                EOP = True

    pg.display.update()
    clock.tick(40)


    """
                if driver1.rect.y >= ship.rect.y + 40:
                driver1.isWalking = True
                driver1.direction = 'up'
                driver1.animate()
                driver1.rect.clamp_ip(driver1.screen_rect)
                driver1.rect.y -= driver1.speed
            else:
                con3 = True

            if driver2 is not None:
                if driver2.rect.y >= ship.rect.y + 40:
                    driver2.isWalking = True
                    driver1.direction = 'up'
                    driver2.animate()
                    driver2.rect.clamp_ip(driver2.screen_rect)
                    driver2.rect.y -= driver2.speed
                else:"""
