string = '0-0-0-0-0-0-0;0-0-0-0-0-0-0;0-0-0-0-0-0-0;0-0-0-0-0-0-0;0-0-0-0-0-0-0;0-0-0-0-0-0-0;0-0-0-0-0-0-0;0-0-0-0-0-0-0;0-0-0-0-0-0-0;0-0-0-0-0-0-0;0-0-0-0-0-0-0;0-0-0-0-0-0-0'


def string_to_array(string):
    array = []
    tmp = string.split(';')
    for ele in tmp:
        tmp2 = ele.split('-')
        array.append(int(tmp2))
    print(array[0][2])


string_to_array(string)
