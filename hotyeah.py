#!/usr/bin/env python3

## @author agalik

## hotyeah encoder/decoder for tweet-based steganography, inspired by https://themodernrogue.com
## uses a space between a sentence and its delimiter/punctuation for a binary 1, no space for 0
## make sure the carrier tweet/message contains no delimiters immediately following a space
## in the event the carrier is not long enough, the remainder of the secret can be stored in a file for later use

def get_delim():
    delimiters = input("enter delimiters, like .?! \n> ")

    # set up a set of delimiter characters
    delim = set()   # use a set for fast membership checks, probably unneccesary

    for c in delimiters:
        delim.add(c)
    
    return delim


def str_to_bitstring(string):
    message_bits = ""   # a bitstring representing the message

    for c in string:
        char_code = ord(c)  # get the code for this character, as an int
        bitstring = bin(char_code)[2:]  # get a bitstring for the character code, cut off the '0b' at the beginning
        bitstring = '0'*(8-len(bitstring)) + bitstring  # pad the left side with zeros if need be

        message_bits = message_bits + bitstring  # slap it on a big bitstring for later

    return message_bits


def encode():
    mode = input("continue a past transmission or start a new one? c/n \n> ")

    message_bits = ""   # a bitstring representing the message

    if mode == 'c':
        path = input("enter a filepath to read from \n> ")
        f = open(path, 'r')
        message_bits = f.readline() # i sure hope they choose the right file, no error handling here
        f.close()
    else:
        message = input("enter a message to encode (what you want to hide) \n> ")
        message_bits = str_to_bitstring(message)

    carrier = input("enter a carrier message (what you want to hide it in) \n> ")

    delim = get_delim()

    message_idx = 0
    carrier_idx = 0
    while carrier_idx < len(carrier):   # iterate through the carrier, looking for delims

        if message_idx == len(message_bits): # if we've encoded the whole message, we're done
            break

        carrier_c = carrier[carrier_idx]

        if carrier_c in delim:  # found delim, time to put one bit of the message down

            if message_bits[message_idx] == '1':
                carrier = carrier[:carrier_idx] + ' ' + carrier[carrier_idx:]
                carrier_idx += 1    # skip over that space we just added
            
            message_idx += 1    # move on to the next bit in the message
        
        carrier_idx += 1

    print()
    print(carrier)
    print()

    if message_idx != len(message_bits):
        print("message didn't fit")

        path = input("enter a filepath to store remainder of message, or ctrl+c to abort \n> ")
        
        f = open(path, 'w')
        f.write(message_bits[message_idx:])
        f.close()


def decode(carrier):
    delim = get_delim()

    message = []

    for carrier_idx in range( len(carrier) ):   # iterate through the carrier, looking for delims

        carrier_c = carrier[carrier_idx]

        if carrier_c in delim:  # found delim, time to put one bit of the message down

            if carrier[carrier_idx - 1] == ' ':
                message.append('1')
            else:
                message.append('0')
    
    return message


def bitstring_to_str(bits): # got lazy. https://stackoverflow.com/questions/10237926/convert-string-to-list-of-bits-and-viceversa
    num_bytes = int(len(bits) / 8)
    
    chars = []
    for b in range(num_bytes):
        byte = bits[b*8:(b+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)


m = input("encode or decode? e/d \n> ")

if m == 'e':
    encode()
else:
    carrier = input("enter a message to decode \n> ")
    
    bits = decode(carrier)
    message = bitstring_to_str(bits)

    print()
    print(message)