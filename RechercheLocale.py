

class Gallery:
    def __init__(self, file):
        context = self.create_context(file)
        self.petit_carac = context[0]  # rayon, prix
        self.grand_carac = context[1]
        self.art_pieces = context[2]
        self.gallery_x = context[3]
        self.gallery_y = context[4]
        self.cameras = []
        print("initialisé")

    def create_context(self, file):
        """ transforme le fichier en données utilisables
        :return: camera1 specs, cam2 specs, coordonnées des oeuvres, longueur de la gallerie (min_x,max_x), largeur de la gallerie (min_y,max_y)
        """
        f = open(file, 'r')
        lines = f.readlines()
        f.close()
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
            art_pieces.append((x, y))
        return (r1, p1), (r2, p2), art_pieces, (min_x, max_x), (min_y, max_y)

    def solve(self, config = 1):
        """
        Le principe de la recherche locale est de partir d'une solution, et de se déplacer itérativement vers des
        solutions proches plus optimales.
        :return:
        """
        cameras = {}
        if config == 1:
            for art in self.art_pieces:
                # une solution qui marche forcément est de placer une grande caméra sur chaque oeuvre d'art
                cameras[(2, art[0], art[1])] = []
        else:
            for i in range(self.gallery_x[0], self.gallery_x[1] + 1, 5):
                    for j in range(self.gallery_y[0], self.gallery_y[1] +1, 5):
                        cameras[(2, i, j)] = []
        print("caméras in place")
        delete = []
        for cam in cameras:
            if cam[0] == 1:
                r = self.petit_carac[0]
            else:
                r = self.grand_carac[0]
            for art in self.art_pieces:
                if dist(art, cam)<= r**2:
                    cameras[cam].append(art)
            if cameras[cam] == []:
                delete.append(cam)
        for cam in delete:
            del cameras[cam]
        print("cameras watching")

        # améliorons la solution
        Nb1 = len(cameras) + 1
        Nb2 = len(cameras)
        count_boucle_while = 0
        while Nb1>Nb2 and count_boucle_while<10:
            count_boucle_while += 1
            deletions = []
            for cam1, list_art1 in cameras.items():
                a = 0
                necessary = False
                suppressed = False
                while a < (len(list_art1)):
                    art = list_art1[a]
                    found = False
                    for cam2, list_art2 in cameras.items():
                        if suppressed:
                            pass
                        elif cam1 != cam2:
                            l1 = len(list_art1)
                            l2 = len(list_art2)
                            if art in list_art2:
                                if necessary:
                                    list_art2.remove(art)
                                    if list_art2 == []:
                                        deletions.append(cam2)

                                elif len(list_art2)>=len(list_art1):
                                    inclu = True
                                    for e in list_art1 :
                                        if not e in list_art2:
                                            inclu = False
                                    if inclu:
                                        deletions.append(cam1)
                                        cameras[cam1] = []
                                        suppressed = True
                                        found = True
                                    else:
                                        found = True

                                else:
                                    inclu = True
                                    for e in list_art2 :
                                        if not e in list_art1:
                                            inclu = False
                                    if inclu:
                                        deletions.append(cam2)
                                    else:
                                        found = True

                    if not found:
                        necessary = True
                    a += 1;

            for cam in deletions:
                try:
                    del cameras[cam]
                except:
                    pass
            Nb1 = Nb2
            Nb2 = len(cameras)
            print("nombre de caméra retirées à la boucle "+ str(count_boucle_while) + " : " + str(Nb1-Nb2))
        for cam, list_art1 in cameras.items():
            if cam[0] == 2:
                reduce = True
                for art in list_art1:
                    if dist(art,cam) > self.petit_carac[0]**2:
                        reduce = False
                if reduce:
                    del cameras[cam]
                    cameras[(1, cam[1], cam[2])] = []
        petites = 0
        grandes = 0
        for cam in cameras.keys():
            self.cameras.append(cam)
            if cam[0] == 1:
                petites += 1
            else:
                grandes += 1

        #self.display_gallery()

        print("le nombre total caméras est : " + str(len(cameras)))
        print("dont " + str(petites) + " petites caméras et " + str(grandes) + " grandes caméras")
        print("le prix total est : " + str(petites * self.petit_carac[1] + grandes * self.grand_carac[1]) + " €")






    def display_gallery(self):
        max_x = self.gallery_x[1]
        min_x = self.gallery_x[0]
        max_y = self.gallery_y[1]
        min_y = self.gallery_y[0]
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
            if gallery[art[1] + 1 - min_y][art[0] + 1 - min_x] in [".", "C", "c"]:
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
            r = self.petit_carac[0]
        else: # big
            r = self.grand_carac[0]
        area = []
        x_min = round(camera[1] - r)
        y_min = round(camera[2] - r)
        x_max = round(camera[1] + r)
        y_max = round(camera[2] + r)
        for x in range(x_min, x_max + 1):
            for y in range(y_min, y_max + 1):
                if dist((x,y),(camera[1],camera[2]))<= r**2:
                    area.append((x,y))
        return area


def dist(objet1, objet2):
    if len(objet1)== 3:
        if len(objet2) == 3:
            x = objet1[1] - objet2[1]
            y = objet1[2] - objet2[2]
        else:
            x = objet1[1] - objet2[0]
            y = objet1[2] - objet2[1]
    else:
        if len(objet2) == 3:
            x = objet1[0] - objet2[1]
            y = objet1[1] - objet2[2]
        else:
            x = objet1[0] - objet2[0]
            y = objet1[1] - objet2[1]
    return x ** 2 + y ** 2


if __name__ == '__main__':
    g = Gallery("input_9.txt")
    g.solve(2)
