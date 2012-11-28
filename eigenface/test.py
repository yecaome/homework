import math
from struct import unpack, pack
from PIL import Image


def read_labels(fname):
    with open(fname) as f:
        magic, total = unpack('>2I', f.read(4*2))
        assert magic == 2049
        return unpack('%dB' % total, f.read(total))

def read_images(fname):
    with open(fname) as f:
        magic, total, rows, cols = unpack('>4I', f.read(4*4))
        assert magic == 2051
        pixels = rows * cols
        fmt = '%dB' % pixels
        return (rows, cols), [ unpack(fmt, f.read(pixels))
            for _ in xrange(total) ]

def create_image(data, size):
    fmt = '%dB' % len(data)
    data2 = [ (255-i) for i in data ]
    buf = pack(fmt, *data2)
    im = Image.fromstring('L', size, buf)
    return im

def guess_grid(n):
    sqrt = int(math.sqrt(n))
    if sqrt*sqrt == n:
        rows = cols = sqrt
    #TODO:
    return rows, cols

def array(images):
    n = len(images)
    assert n > 0
    rows, cols = guess_grid(n)
    mode = images[0].mode
    w, h = images[0].size # assume all images have the same size
    size = (h*cols, w*rows)
    im = Image.new(mode, size)
    for r in range(rows):
        for c in range(cols):
            i = r*cols+c
            if i >= n:
                break
            im.paste(images[i], (w*c, h*r))
    return im


def write_numbers(data):
    with open('numbers.txt', 'w') as f:
        for im in data:
            line = ' '.join([ str(p) for p in im ])
            f.write(line+'\n')

def test():
    n = 16
    labels = read_labels('MNIST/t10k-labels-idx1-ubyte')[:n]
    size, data = read_images('MNIST/t10k-images-idx3-ubyte')
    data = data[:n]

    if True:
        write_numbers(data)
    else:
        images = [ create_image(i, size) for i in data ]
        panel = array(images)

        print labels
        panel.show()



def test2():
    data = [int(float(line)) for line in open('mean.txt')]
    #im = create_image(data, (28,28))
    im = create_image(data, (320, 243))
    im.show()

def load_face(fname):
    im = Image.open(fname).convert('L')
    print im.size
    return im.getdata()


def test3():
    faces = [load_face('yalefaces/subject%02d.normal'%i) for i in range(1,16)]
    print len(faces[0])
    write_numbers(faces)


test2()
