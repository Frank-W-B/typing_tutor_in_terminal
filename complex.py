import pickle

class Complex(object):
    def __init__(self, user, realpart, imagpart):
        self.user = user
        self.r = realpart
        self.i = imagpart

    def save(self, fname):
        with open(fname, 'wb') as f:
            pickle.dump(self, f)

if __name__ == '__main__':
    x = Complex('user1', 3.0, -4.5)
    print("x")
    print(x.user)
    print(x.r)
    print(x.i)
    fname = 'complex.pkl'
    with open(fname, 'wb') as f:
        pickle.dump(x, f)
    with open(fname, 'rb') as f:
        x2 = pickle.load(f)
    print("x2")
    print(x2.user)
    print(x2.r)
    print(x2.i)
    
    fname2 = ''.join([x.user, '.pkl'])
    x.save(fname2)
    with open(fname2, 'rb') as f2:
        x3 = pickle.load(f2)
    print("x3")
    print(x3.user)
    print(x3.r)
    print(x3.i)


