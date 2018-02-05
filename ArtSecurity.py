from math import sqrt
from pyscipopt import Model, quicksum


class Gallery:
    def __init__(self, file):
        context = self.create_context(file)
        self.small_camera_caracteristics = context[0]
        self.big_camera_caracteristics = context[1]
        self.art_pieces = context[2]
        self.gallery_x = context[3]
        self.gallery_y = context[4]
        self.cameras = []

    def create_context(self, file):
        """ transform file into usable data
        :return: camera1 specs, cam2 specs, artwork coordinates, gallery length (min_x,max_x), gallery width (min_y,max_y)
        """
        lines = open(file, 'r').readlines()
        
        r1, r2 = map(int, lines.pop(0).split(","))
        p1, p2 = map(int, lines.pop(0).split(","))

        art_pieces = []
        max_x, max_y = map(int, lines[0].split(","))
        min_x, min_y = map(int, lines[0].split(","))
        for line in lines:
            x, y = map(int, line.split(","))
            if x > max_x:
                max_x = x
            elif x < min_x:
                min_x = x
            if y > max_y:
                max_y = y
            elif y < min_y:
                min_y = y
            art_pieces.append((x,y))
        return (r1,p1), (r2,p2), art_pieces, (min_x,max_x), (min_y,max_y)

    def solve(self, taille_grain=1):
        model = Model("gallery")

        z = { (i,j): model.addVar("z({}, {})".format(i,j)) \
                    for i in range(self.gallery_x[0], self.gallery_x[1] +1, taille_grain) \
                    for j in range(self.gallery_y[0], self.gallery_y[1] +1, taille_grain)}

        # chaque oeuvre est couverte par une caméra 
        # <=> il y a au moins une caméra de type 2 dans un rayon 8 ou cam1 dans un rayon de 4
        for artwork in self.art_pieces: 
            # tous les points dans le disque de rayon max = 8
            # on prend d'abord un carré de longueur 8 autour du point et on élage les points pas dans le cercle
            possible4 = [(artwork[0]+i, artwork[1]+j) for i in range(-4, 5) for j in range(-4, 5) if \
                            dist(artwork, (artwork[0]+i, artwork[1]+j)) <= 4**2 \
                            and self.gallery_x[0] <= artwork[0]+i <= self.gallery_x[1] \
                            and self.gallery_y[0] <= artwork[1]+j <= self.gallery_y[1]]
            # somme de tous les points autour de l'oeuvre >= 1
            model.addCons( quicksum(z[(i,j)] for i,j in possible4) >=1  , "protege")

        # minimiser sum((x,y)) correspondant au coût d'une caméra (0, 1, 2)
        model.setObjective( quicksum(z[(i,j)] \
                    for i in range(self.gallery_x[0], self.gallery_x[1], taille_grain) \
                    for j in range(self.gallery_y[0], self.gallery_y[1], taille_grain)) , "minimize")
        
        model.optimize()

        if model.getStatus() != 'optimal':
            print('LP is not feasible!')
        else:
            print("Optimal value: {}".format(model.getObjVal()))

def dist(objet1, objet2):
    x = objet1[0] - objet2[0]
    y = objet1[1] - objet2[1]
    return x**2 + y**2


if __name__ == '__main__':

    g = Gallery("input_9.txt")
    print(len(g.art_pieces), " oeuvres d'art")
    print("min_x,max_x :", g.gallery_x)
    print("min_y,max_y :", g.gallery_y)
    g.solve()
