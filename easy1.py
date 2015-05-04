import time

s = [16, 42, 28, 3, 26, 0, 31, 46, 27, 14, 49, 62, 37, 56, 23, 6, 40, 48, 53, 8, 20, 25, 3, 1, 2, 63, 15, 34, 55, 21, 39, 57, 54, 45, 47, 13, 7, 44, 61, 9, 60, 32, 22, 29, 52, 19, 12, 50, 5, 51, 11, 18, 59, 41, 36, 30, 17, 38, 10, 4, 58, 43, 35, 24]
 
p = [24, 5, 15, 23, 14, 32, 19, 18, 26, 17, 6, 12, 34, 9, 8, 20, 28, 0, 2, 21, 29, 11, 33, 22, 30, 31, 1, 25, 3, 35, 16, 13, 27, 7, 10, 4]
 
key = 0b111100001111000011111100001111000011
 
def sbox(x):
        #print '''S-box function'''
        return s[x]
 
def pbox(x):
	#print '''P-box function'''
        # if the texts are more than 32 bits,
        # then we have to use longs
        y = 0l
 
        # for each bit to be shuffled
        for i in range(len(p)):
 
                # if the original bit position
                # is a 1, then make the result
                # bit position have a 1
                if (x & (1l << i)) != 0:
                        y = y ^ (1l << p[i])
       
        return y
 
def demux(x):
        #print '''Demultiplex, takes in 36-bit to six 6-bit values'''
        y = []
        for i in range(0, 6):
                y.append((x >> (i * 6)) & 0x3f)
 
        return y
 
def mux(x):
        #print '''Multiplex, takes in six 6-bit to 36-bit values'''
        y = 0l
        for i in range(0, 6):
                y = y ^ (x[i] << (i * 6))
 
        return y
 
def mix(p, k):
        #print '''Key mixing'''
        v = []
        key = demux(k)
        for i in range(0, 6):
                v.append(p[i] ^ key[i])
 
        return v
 
def round(p, k):
        #print '''Round function'''
        u = []
 
        # Calculate the S-boxes
        for x in demux(p):
                u.append(sbox(x))
 
        # Run through the P-box
        v = demux(pbox(mux(u)))
 
        # XOR in the key
        w = mix(v, k)
 
        # Glue back together, return
        return mux(w)
 
def encrypt(p, rounds):
        #print '''Encryption'''
        x = p
        for i in range(rounds):
                x = round(x, key)
 
        return x
 
def apbox(x):
        y = 0l
        for i in range(len(p)):
                if (x & (1l << i)) != 0:
                        pval = p.index(i)
                        y = y ^ (1l << pval)
        return y
 
def asbox(x):
        return s.index(x)
 
def unround(c, k):
        #print '''Opposite of the round function'''
        x = demux(c)
        u = mix(x, k)
        v = demux(apbox(mux(u)))
        w = []
        for s in v:
                w.append(asbox(s))
 
        return mux(w)
 
def decrypt(c, rounds):
        #print '''Decryption function'''
        x = c
        for i in range(rounds):
                x = unround(x, key)
 
        return x
 
if __name__ == '__main__':
        #import pdb
        #pdb.set_trace()
        plaintext = 0b111100001111000011110000111100001111
		   #0xf0f0f0f0f
#	plaintext = int('This is a secret message', 2)
	
        ciphertext = encrypt(plaintext, 1)
        print 'plaintextA: ', plaintext
        print 'ciphertext: ', ciphertext
        print 'plaintextB: ', decrypt(ciphertext, 1)

	print 'Entering Linear Cryptanalysis segment'
	
	
