# Used to solve the "chessboard problem" see OEIS A253315

def A(n):
  v = 0
  i = 2
  while n > 0:
    if (n & 1):
      v = v ^ i
    i = i + 1
    n = n >> 1
  return v

def decode(x):
	v = 0
	i = 0
	while x > 0:
		if (x & 1):
			v = v ^ i
		i = i + 1
		x = x >> 1
	return v

def encode(x, vp, n):
	v = decode(x, n)
	d = v ^ vp
	return x ^ (1 << d)

#for x in xrange(0b11111111):
#	for vp in xrange(8):
#		print (str(encode(x, vp)) + ","),
#	print


for x in xrange(200):
	print str(A(x)) + ",",
	#print str(x) + " " + str(A(x))
