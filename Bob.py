import socket  
import sys  
import pickle


class Bob:
    def getCiphertext(self, pkTom):
        plaintext = 'something1'
        stringToXorWith = 'WeAgreedOnThisString'

        plaintextHex = plaintext.encode("hex")
        stringToXorWithHex = stringToXorWith.encode("hex")

        plaintextBits = bin(int(plaintextHex, 16))[2:]
        stringToXorWithBits = bin(int(stringToXorWithHex, 16))[2:]

        xoredPlaintext = (int(plaintextBits,2) ^ int(stringToXorWithBits,2))

        ciphertext = pkTom.encrypt(xoredPlaintext,32)
        return ciphertext   

def main():

    bob = Bob()

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print 'Failed to create socket'
        sys.exit()  
     
    host = socket.gethostname()
    port = 23254
     
    try:
        remote_ip = socket.gethostbyname( host )
     
    except socket.gaierror:
        #could not resolve
        print 'Hostname could not be resolved. Exiting'
        sys.exit()
     
    #Connect to remote server
    s.connect((remote_ip , port))
     
    #receive & unpickle tom_pk
    tom_pk = s.recv(4096)
    tom_pk_unpickled = pickle.loads(tom_pk)
    #-------------#

    #pickle & send ciphertext
    ciphertext = bob.getCiphertext(tom_pk_unpickled)

    ciphertext_pickled = pickle.dumps(ciphertext)

    try :
        s.sendall(ciphertext_pickled)
    except socket.error:
        print 'Send failed'
        sys.exit()
    #-------------#

    #receive compare result
    compare_result = s.recv(4096)
    print 'bob received ' + compare_result
    #-------------#


if __name__ == '__main__':
    main()
