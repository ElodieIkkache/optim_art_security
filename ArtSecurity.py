import numpy as np
from pyscipopt import Model, quicksum


class Gallery:
    def __init__(self, file):
        context = self.create_context(file)
        self.petit_carac = context[0] # rayon, prix
        self.grand_carac = context[1]
        self.art_pieces = context[2]
        self.gallery_x = context[3]
        self.gallery_y = context[4]

    def create_context(self, file):
        """ transforme le fichier en données utilisables
        :return: camera1 specs, cam2 specs, coordonnées des oeuvres, longueur de la gallerie (min_x,max_x), largeur de la gallerie (min_y,max_y)
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
        # modélisation d'une petite caméra par case
        p = { (i,j): model.addVar("p({}, {})".format(i,j), vtype="INTEGER") \
                    for i in np.arange(self.gallery_x[0], self.gallery_x[1] +1, taille_grain) \
                    for j in np.arange(self.gallery_y[0], self.gallery_y[1] +1, taille_grain)}
                        
        # modélisation d'une grande caméra par case
        g = { (i,j): model.addVar("g({}, {})".format(i,j), vtype="INTEGER") \
                    for i in np.arange(self.gallery_x[0], self.gallery_x[1] +1, taille_grain) \
                    for j in np.arange(self.gallery_y[0], self.gallery_y[1] +1, taille_grain)}

        # chaque oeuvre est couverte par une caméra 
        # <=> il y a une caméra de type 1 dans un rayon de 4
        #     ou au moins une caméra de type 2 dans un rayon 8 
        for artwork in self.art_pieces: 
            # Pour les petites caméras: on prend d'abord un carré de longueur 8 autour du point et on élague les points pas dans le cercle
            possible_petit = [(artwork[0]+i, artwork[1]+j) for i in range(-self.petit_carac[0], self.petit_carac[0]+1) \
                                                        for j in range(-self.petit_carac[0], self.petit_carac[0]+1) if \
                            dist(artwork, (artwork[0]+i, artwork[1]+j)) <= self.petit_carac[0] ** 2 \
                            and self.gallery_x[0] <= artwork[0]+i <= self.gallery_x[1] \
                            and self.gallery_y[0] <= artwork[1]+j <= self.gallery_y[1]]
            # Pour les grandes caméras: idem mais carré de longueur 16
            possible_grand = [(artwork[0]+i, artwork[1]+j) for i in range(-self.grand_carac[0], self.grand_carac[0]+1) \
                                                        for j in range(-self.grand_carac[0], self.grand_carac[0]+1) if \
                            dist(artwork, (artwork[0]+i, artwork[1]+j)) <= self.grand_carac[0] ** 2 \
                            and self.gallery_x[0] <= artwork[0]+i <= self.gallery_x[1] \
                            and self.gallery_y[0] <= artwork[1]+j <= self.gallery_y[1]]
            # somme de tous les points autour de l'oeuvre >= 1
            model.addCons( quicksum(p[(i,j)] for i,j in possible_petit) + quicksum(g[(i,j)] for i,j in possible_grand) >=1  , "protege")
            for i,j in possible_grand:
                model.addCons( 0 <= (p[(i,j)]+g[(i,j)] <=1)  , "une_seule_cam")
            # for i,j in possible_grand:
            #     model.addCons( 0 <= (g[(i,j)] <=1)  , "une_seule_cam")
                

        # minimiser sum(petite(x,y)+ 2*grande(x,y)) correspondant au coût de toutes les caméras dans la gallerie
        model.setObjective( self.petit_carac[1] * quicksum( p[(i,j)] \
                    for i in np.arange(self.gallery_x[0], self.gallery_x[1], taille_grain) \
                    for j in np.arange(self.gallery_y[0], self.gallery_y[1], taille_grain)) \
                         + self.grand_carac[1] * quicksum( g[(i,j)] \
                    for i in np.arange(self.gallery_x[0], self.gallery_x[1], taille_grain) \
                    for j in np.arange(self.gallery_y[0], self.gallery_y[1], taille_grain)) , "minimize")
        
        model.optimize()

        f = open("results.txt", "w")

        if model.getStatus() != 'optimal':
            print('LP is not feasible!')
        else:
            for key, value in p.items():
                if model.getVal(value) != 0:
                    f.write("{},{},{}\n".format(int(model.getVal(value)), key[0], key[1]))
            
            for key, value in g.items():
                if model.getVal(value) != 0:
                    f.write("{},{},{}\n".format(int( 2 * model.getVal(value)), key[0], key[1]))                    

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
    g.solve(1)
