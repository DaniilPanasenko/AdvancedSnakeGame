alphabet = {'A': '01110'
                 '10001'
                 '11111'
                 '10001'
                 '10001',
            'B': '1111010001111101000111110',
            'C': '0111010001100001000101110',
            'D': '1111010001100011000111110',
            'E': '1111110000111101000011111',
            'F': '1111110000111101000010000',
            'G': '0111110000101111000101111',
            'H': '1000110001111111000110001',
            'I': '111010010010111',
            'J': '0001100001000011000101110',
            'K': '1000110010111001001010001',
            'L': '10001000100010001111',
            'M': '1000111011101011000110001',
            'N': '1000111001101011001110001',
            'O': '0111010001100011000101110',
            'P': '1111010001111101000010000',
            'Q': '0110010010100101001001101',
            'R': '1111010001111101001010001',
            'S': '0111110000011100000111110',
            'T': '1111100100001000010000100',
            'U': '1000110001100011000101110',
            'V': '1000110001100010101000100',
            'W': '1010110101101011010101010',
            'X': '1000101010001000101010001',
            'Y': '1000101010001000010000100',
            'Z': '1111100010001000100011111',
            '1': '110010010010111',
            '2': '1111000001011111000011111',
            '3': '1111000001011100000111110',
            '4': '1000110001111110000100001',
            '5': '1111110000111100000111110',
            '6': '0111010000111101000101110',
            '7': '1111100001000010001000010',
            '8': '0111010001011101000101110',
            '9': '0111010001011110000101110',
            '0': '0111010001100011000101110',
            '!': '11101',
            '.': '00001',
            '?': '11100001011000000100',
            ':': '01010',
            ' ': '000000000000000'
            }


def translate(string):
    arr = [[], [], [], [], []]
    for char in string:
        letter = alphabet[char]
        length = int(len(letter) / 5)
        for i in range(5):
            for j in range(length):
                arr[i].append(int(letter[i * length + j]))
            arr[i].append(0)
    return arr


def translate_with_color(string, color):
    arr = translate(string)
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if arr[i][j] == 1:
                arr[i][j] = color
    return arr


def translate_with_zoom(string, color):
    arr = translate_with_color(string, color)
    new_arr = []
    for i in range(len(arr)):
        new_arr.append([])
        new_arr.append([])
        for j in range(len(arr[i])):
            new_arr[i * 2].append(arr[i][j])
            new_arr[i * 2].append(arr[i][j])
            new_arr[i * 2 + 1].append(arr[i][j])
            new_arr[i * 2 + 1].append(arr[i][j])
    return new_arr
