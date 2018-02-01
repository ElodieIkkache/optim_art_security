from math import sqrt


class Gallery:
    def __init__(self, file):
        context = self.create_context(file)
        self.small_camera_caracteristics = context[0]
        self.big_camera_caracteristics = context[1]
        self.art_pieces = context[2]
        self.cameras = []

    def create_context(self, file):
        lines = open(file, 'r').readlines()
        line1 = lines.pop(0).split(",")
        r1 = int(line1[0])
        r2 = int(line1[1][:-1])
        line2 = lines.pop(0).split(",")
        p1 = int(line2[0])
        p2 = int(line2[1][:-1])
        art_pieces = []
        for line in lines:
            line = line.split(",")
            x = int(line[0])
            y = int(line[1][:-1])
            art_pieces.append((x,y))
        return [(r1,p1), (r2,p2), art_pieces]

    def display_gallery(self):
        max_x = self.art_pieces[0][0]
        min_x = self.art_pieces[0][0]
        max_y = self.art_pieces[0][1]
        min_y = self.art_pieces[0][1]
        for piece in self.art_pieces:
            # détermination de la taille de la grille
            if piece[0]> max_x:
                max_x = piece[0]
            elif piece[0] < min_x:
                min_x = piece[0]
            if piece[1]> max_y:
                max_y = piece[1]
            elif piece[1] < min_y:
                min_y = piece[1]
        # salle vide
        gallery = [["#"]*(max_x - min_x + 3)]
        for i in range(min_y, max_y+1):
            line = ["#"]
            for j in range(min_x, max_x+1):
                line.append(" ")
            line.append("#")
            gallery.append(line)
        gallery.append(["#"] * (max_x - min_x + 3))
        #adding the cameras
        #TODO remove fake cameras
        self.cameras = [(1, 2, 3), (2, 6, 5), (1, 8, 8)]
        for cam in self.cameras:
            for (x,y) in self.get_area(cam):
                if x >= min_x and x <= max_x and y >= min_y and y <= max_y:
                    gallery[y + 1 - min_y][x + 1 - min_x] = "."  # if . then watched
        for cam in self.cameras:
            if cam[0] == 1: # small camera
                gallery[cam[2] + 1 -min_y][cam[1] + 1 - min_x] = "c" # small c for small camera
            else : # big camera
                gallery[cam[2] + 1 - min_y][cam[1] + 1 - min_x] = "C" # big C for big camera
        for art in self.art_pieces:
            if gallery[art[1] + 1 - min_y][art[0] + 1 - min_x] == ".":
                gallery[art[1] + 1 - min_y][art[0] + 1 - min_x] = "S" # S for secure
            else :
                gallery[art[1] + 1 - min_y][art[0] + 1 - min_x] = "D" # D for danger
        for l in gallery:
            chain = ""
            for c in l:
                chain += c + " "
            print(chain)

    def get_area(self, camera):
        if camera[0] == 1: # small
            r = self.small_camera_caracteristics[0]
        else: # big
            r = self.big_camera_caracteristics[0]
        area = []
        x_min = round(camera[1] - r)
        y_min = round(camera[2] - r)
        x_max = round(camera[1] + r)
        y_max = round(camera[2] + r)
        for x in range(x_min, x_max + 1):
            for y in range(y_min, y_max + 1):
                if dist((x,y),(camera[1],camera[2]))<= r:
                    area.append((x,y))
        return area


def dist(objet1, objet2):
    x = objet1[0] - objet2[0]
    y = objet1[1] - objet2[1]
    return sqrt(x**2 + y**2)



g = Gallery("small_input")
g.display_gallery()
