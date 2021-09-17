import struct
from struct import pack, unpack
from pyDes import triple_des, CBC

class Card:

    def __init__(self, debugstring = "CARD"):
        self.debugstring = debugstring
        self.cardNr = "6703010305045748"
        self.pin = "1111"
        self.masterkey = "3389522462037335"
        self.iv = "00000000"
        self.bitmask = 0x000000000000FFFF
        self.wrongPin = 3
        self.expiryDate = "12/24"
        self.cdol1 = {}
        self.cdol2 = {}
        self.issuerProprietaryBitmap = ""
        self.atc = "0006"
        self.fill_cdol()


    def fill_cdol(self):
        self.cdol1["AA"] = "000000000000" #Amount Authorized
        self.cdol1["AO"] = "000000000000" #amount Other
        self.cdol1["TCC"] = "0790"        #Terminal Country Code
        self.cdol1["TVR"] = "8000040000"  #Terminal Verification Results
        self.cdol1["TCUC"] = "0790"        #Terminal Currency Code
        self.cdol1["TD"] = "240321"       #Transaction Date
        self.cdol1["UN"] = "00000000"     #Unpredictable Number
        self.cdol1["AIP"] = "1C00"        #Application Interchange Profile
        self.cdol1["ATC"] = self.atc      #Application Transaction Counter
        
    def check_PIN(self, plainPIN):
        if(plainPIN == self.pin):
            return True
        else:
            self.wrongPin = self.wrongPin-1
            return False

    #PSN = Pan Sequence Number
    #ATC= Application Transaction Counter
    #ARQC
    #CDOL contains UN and AA --> 
    #Response is typically computed by applying Issuer Proprietary Bitmap
    #in the concatenation of the PSN, ATC, ARQC and IAD
    #result of applied bitmap is then converted to digits!

    #using generate_AC: terminal can ask card to compute cryptogram
    #arguments of the generate_AC tell the card which type of cryptogram to produce
    def generate_ac(self, specifier, UN=None, AA=None):
        if UN != None:
            self.cdol1["UN"] = UN
        if AA != None:
            self.cdol1["AA"] = AA

        print(self.debugstring + ": cryptograph: UN=" + str(self.cdol1["UN"]) + " AA=" + str(self.cdol1["AA"]))

        if specifier == "arqc":
            print(self.debugstring + ": cryptograph: start crafting ARQC....")
            arqc = self.generate_arqc()
            return arqc, self.atc
        elif specifier == "aac":
            aac = self.generate_aac()
            print("generating aac")
            return aac, self.atc

    
    def generate_arqc(self):
        concatenatedData = ""
        for key in self.cdol1:
            concatenatedData += str(self.cdol1[key])
        mac = self.generate_mac(concatenatedData, self.masterkey, self.iv)
        #arqc = triple_des(self.masterkey, CBC, bytes(self.iv, encoding='utf8')).encrypt(mac)[:-9:-1]
        arqc = triple_des(self.masterkey, CBC, bytes(self.iv, encoding='utf8')).encrypt(mac)[:-9:-1]
        print(self.debugstring + ": cryptograph: ARQC: perform 3DES on MAC")  
        return arqc

 
    def generate_aac(self):
        print("todo")
        return 0


    def generate_mac(self, data, key, iv, flip_key=False):
        # Data is first split into tuples of 8 character bytes, each
        # tuple then reversed and joined, finally all joined back to
        # one string that is then triple des encrypted with key and
        # initialization vector iv. If flip_key is True then the key
        # halfs will be exchanged (this is used to generate a mac for
        # write). The resulting mac is the last 8 bytes returned in
        # reversed order.

        print(self.debugstring + ": cryptograph: ARQC: generating MAC Message Authentication Code")

        assert len(data) % 8 == 0 and len(key) == 16 and len(iv) == 8
        key = bytes(key[8:] + key[:8], encoding='utf8') if flip_key else bytes(key, encoding='utf8')
        txt = b''.join([
            struct.pack("{}B".format(len(x)), *reversed(x))
            if isinstance(x[0], int)
            else b''.join(reversed(x))
            for x in zip(*[iter(bytes(data, encoding='utf8'))]*8)])
        return txt