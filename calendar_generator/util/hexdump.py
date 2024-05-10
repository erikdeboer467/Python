import io


def hexdump(data, offset=0, length=-1, row=20, offsetInHex=True):    
    '''Hexdump is a utility that displays the contents of binary files in hexadecimal or ASCII. It's a utility for inspection and can be used for data recovery, reverse engineering, and programming.'''

    length = len(data) if length == -1 else min(offset+length, len(data))
    
    #line = ""
    for i in range(offset, length, row):
        sb = io.StringIO()
        sb.write(f"{offset:08X}: " if offsetInHex else f"{offset:010}: ")
        
        for j in range(i, min(i + row, len(data))):
            sb.write(f"{data[j]:02X} ")

        sb.write(" ")

        for j in range(i, min(i + row, len(data))):
            c = chr(data[j])
            sb.write(c if 32 <= ord(c) < 127 else '.')

        print(sb.getvalue())
        offset += row