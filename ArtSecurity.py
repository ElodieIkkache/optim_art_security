
class Gallery:
    def __init__(self, file):
        context = self.create_context(file)
        self.small_camera = context[0]
        self.big_camera = context[1]
        self.art_pieces = context[2]

    def create_context(self, file):
        lines = open(file, 'r').readlines()
        line1 = lines.pop().split(",")
        r1 = int(line1[0])
        r2 = int(line1[1][:-1])
        line2 = lines.pop().split(",")
        p1 = int(line2[0])
        p2 = int(line2[1][:-1])
        art_pieces = []
        for line in lines:
            line = line.split(",")
            x = int(line[0])
            y = int(line[1][:-1])
            art_pieces.append((x,y))
        return [(r1,p1), (r2,p2), art_pieces]


g = Gallery("input_9.txt")
print(g.big_camera)
print(g.small_camera)
print(g.art_pieces)
