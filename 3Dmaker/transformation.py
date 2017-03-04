import numpy

def translation(dispalcement):
	t =numpy.identity(4)
	t[0, 3] = dispalcement[0]
	t[1, 3] = dispalcement[1]
	t[2, 3] = dispalcement[2]
	return t

def scaling(scale):
    s = numpy.identity(4)
    s[0, 0] = scale[0]
    s[1, 1] = scale[1]
    s[2, 2] = scale[2]
    s[3, 3] = 1
    return s
