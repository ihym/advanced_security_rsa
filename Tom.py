import socket
import sys
import pickle
from Crypto.PublicKey import RSA  

class Tom:
    def __init__(self):
    	self.key = RSA.generate(2048)
    	self.pk = self.key.publickey()
	
    def compare(self, ciphertext1, ciphertext2):
        if ciphertext1 == ciphertext2:
                print 'Y'
        else:
                print 'N'



def main():
	HOST = socket.gethostname()
	PORT = 23254

	tom = Tom()

	ciphertexts = []
	 
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	 
	try:
	    s.bind((HOST, PORT))
	except socket.error , msg:
	    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	    sys.exit()
	 
	s.listen(10)
	 
	#now keep talking with the client
	while 1:
	    #wait to accept a connection - blocking call
		conn, addr = s.accept()
	    
	    #pickle & send tom_pk 
		tom_pk_pickled = pickle.dumps(tom.pk)

		conn.sendall(tom_pk_pickled)
	    #-------------#


	    #receive & unpickle ciphertext
		ciphertext = conn.recv(1024)
		ciphertext_unpickled = pickle.loads(ciphertext)
		ciphertexts.append(ciphertext_unpickled)
	    #-------------#

		if len(ciphertexts) == 2:
			if sorted(ciphertexts[0]) == sorted(ciphertexts[1]):
				#send compare result
				compare_result = 'YES'

			else:
				compare_result = 'NO'

			conn.sendall(compare_result)
			#-------------#
 
	conn.close()
	s.close()


if __name__ == '__main__':
	main()
