from binascii import hexlify, unhexlify
import struct
import hashlib
import sys

def sha256(data):
    ''' '''
    return hashlib.sha256(data).hexdigest()

def ripemd160(data):
    ''' '''
    #h = hashlib.new('ripemd160')
    h = hashlib.new('rmd160')
    h.update(data)
    return h.hexdigest()

def sig_digest(payload, chain_id=None, context_free_data=None) :
    ''' '''
    if chain_id :
        buf = bytearray.fromhex(chain_id)
    else :
        buf = bytearray(32)
    # already a bytearray
    buf.extend(payload)
    if context_free_data :
        #buf += sha256(context_free_data)
        pass
    else :
        # empty buffer
        buf.extend(bytearray(32))
    return sha256(buf)
    
def int_to_hex(i) :
    return '{:02x}'.format(i)

def hex_to_int(i) :
    return int(i, 16)
    
def str_to_hex(c) :
    return int(c.encode('hex'),16)

def char_subtraction(a, b, add) :
    x = str_to_hex(a)
    y = str_to_hex(b)
    ans = str((x - y) + add)
    if len(ans) % 2 == 1 :
        ans = '0' + ans
    return int(ans)

#static constexpr uint64_t char_to_symbol( char c ) {
#    if( c >= 'a' && c <= 'z' )
#       return (c - 'a') + 6;
#    if( c >= '1' && c <= '5' )
#        return (c - '1') + 1;
#    return 0;
#}
def char_to_symbol(c) :
    ''' '''
    if c >= 'a' and c <= 'z' :
        return char_subtraction(c, 'a', 6)
    if c >= '1' and c <= '5' :
        return char_subtraction(c, '1', 1)
    return 0
    
#// Each char of the string is encoded into 5-bit chunk and left-shifted
#// to its 5-bit slot starting with the highest slot for the first char.
#// The 13th char, if str is long enough, is encoded into 4-bit chunk
#// and placed in the lowest 4 bits. 64 = 12 * 5 + 4
#static constexpr uint64_t string_to_name( const char* str )
#{
#    uint64_t name = 0;
#    int i = 0;
#    for ( ; str[i] && i < 12; ++i) {
#            // NOTE: char_to_symbol() returns char type, and without this explicit
#            // expansion to uint64 type, the compilation fails at the point of usage
#            // of string_to_name(), where the usage requires constant (compile time) expression.
#            name |= (char_to_symbol(str[i]) & 0x1f) << (64 - 5 * (i + 1));
#    }
#    
#    // The for-loop encoded up to 60 high bits into uint64 'name' variable,
#    // if (strlen(str) > 12) then encode str[12] into the low (remaining)
#    // 4 bits of 'name'
#    if (i == 12)
#    name |= char_to_symbol(str[12]) & 0x0F;
#    return name;
#    }
def string_to_name(s) :
    ''' '''
    i = 0
    name = 0L
    while i < len(s) :
        sym = char_to_symbol(s[i])
        name += (char_to_symbol(s[i]) & 0x1F) << (64-5 * (i + 1))
        i += 1
    if i > 12 :
        name |= char_to_symbol(s[11]) & 0x0F
    return name

def name_to_string(n) :
    ''' '''
    pass


if sys.version > '3' :
    def _byte(b) :
        return bytes((b,))
else :
    def _byte(b) :
        return chr(b)

# temp
def varint_encode(number):
    ''' '''
    buffer = b''
    while True:
        towrite = number & 0x7f
        number >>= 7
        if number:
            buffer += _byte(towrite | 0x80)
        else:
            buffer += _byte(towrite)
            break
    return buffer
