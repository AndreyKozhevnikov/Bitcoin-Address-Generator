from Crypto.Hash import SHA256, RIPEMD160
import base58
import ecdsa
import bech32

class AddressSet:

    def __init__(self, priv,wif):
        self.priv = priv
        self.wif = wif
        self.adrs = []    # creates a new empty list for each dog
    def add_adr(self, adr):
        self.adrs.append(adr)
def generateSetAddressesFromString(st):
    mybytes=str.encode(st)
    sha256a = SHA256.new(mybytes).digest()

    test="".join(map(chr, sha256a))
    
    return generateSetAddressesFromBytes(sha256a)           
def generateSetAddressesFromHex(hex):
    privateBytes=bytes.fromhex(hex)
    return generateSetAddressesFromBytes(privateBytes)
def generateSetAddressesFromInt(intValue):
    privateBytes = int.to_bytes(intValue, length=32, byteorder='big', signed=False)
    return generateSetAddressesFromBytes(privateBytes)
def generateSetAddressesFromBytes(privateBytes):
    private_key=privateBytes
    fullkey = '80' + private_key.hex()+'01'
    #fullkey = '80' + 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'+'01'
    sha256a = SHA256.new(bytes.fromhex(fullkey)).hexdigest()
    sha256b = SHA256.new(bytes.fromhex(sha256a)).hexdigest()

    toDel=sha256b[:8]

    WIF = base58.b58encode(bytes.fromhex(fullkey + sha256b[:8]))

# Get public key
    sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    x = vk.pubkey.point.x()
    y = vk.pubkey.point.y()
    public_key = '04' + x.to_bytes(32, 'big').hex() + y.to_bytes(32, 'big').hex()

# Get compressed public key
    compressed_public_key = '02' if y % 2 == 0 else '03'
    compressed_public_key += x.to_bytes(32, 'big').hex()

    # Get P2PKH address
    hash160 = RIPEMD160.new()
    hash160.update(SHA256.new(bytes.fromhex(public_key)).digest())
    public_key_hash = '00' + hash160.hexdigest()
    checksum = SHA256.new(SHA256.new(bytes.fromhex(public_key_hash)).digest()).hexdigest()[:8]
    p2pkh_address = base58.b58encode(bytes.fromhex(public_key_hash + checksum))

    # Get compressed P2PKH address +
    hash160 = RIPEMD160.new()
    hash160.update(SHA256.new(bytes.fromhex(compressed_public_key)).digest())
    public_key_hash_clean =  hash160.hexdigest()
    public_key_hash = '00' + public_key_hash_clean
    checksum = SHA256.new(SHA256.new(bytes.fromhex(public_key_hash)).digest()).hexdigest()[:8]
    compressed_p2pkh_address = base58.b58encode(bytes.fromhex(public_key_hash + checksum))

    # Get P2SH address
    #redeem_script = '21' + compressed_public_key + 'ac'
    redeem_script = '0014' + public_key_hash[2:]
    p2sh_address2 = base58.b58encode(bytes.fromhex(redeem_script))
    hash160 = RIPEMD160.new()
    hash160.update(SHA256.new(bytes.fromhex(redeem_script)).digest())
    script_hash = '05' + hash160.hexdigest()
    checksum = SHA256.new(SHA256.new(bytes.fromhex(script_hash)).digest()).hexdigest()[:8]
    p2sh_address = base58.b58encode(bytes.fromhex(script_hash + checksum))

    # Get Bech32 address
    witprog = bytes.fromhex(public_key_hash_clean)
    witver = 0x00
    hrp = 'bc'
    bechaddress = bech32.encode(hrp, witver, witprog)

    #mytupleAdresses = (WIF.decode('ASCII'), compressed_p2pkh_address.decode('ASCII'), p2sh_address.decode('ASCII'),bechaddress)
    myAddres=AddressSet(private_key.hex(),WIF.decode('ASCII'))
    myAddres.add_adr(compressed_p2pkh_address.decode('ASCII'))
    #myAddres.add_adr(p2pkh_address.decode('ASCII'))
    myAddres.add_adr(p2sh_address.decode('ASCII'))
    myAddres.add_adr(bechaddress)
    return myAddres

#generateSetAddressesFromHex('5Kb8kLf9zgWQnogidDA76MzPL6TsZZY36hWXMssSzNydYXYB9KF')
res=generateSetAddressesFromString('enter credit long demand tortoise harsh frame path rifle news then trigger')
vl=36893488147419103228-1
res=generateSetAddressesFromInt(vl)
