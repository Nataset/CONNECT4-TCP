def parse_req(message):
    data = []
    tmp = message.split(':')
    for ele in tmp:

        ele = ele.strip()
        data.append(ele)

    return data


def array_to_string(array):
    string = []
    for n in array:
        string_ints = [str(int) for int in n]
        s = '-'
        s = s.join(string_ints)
        string.append(s)
    s = ';'
    string = s.join(string)
    return string


def string_to_array(string):
    array = []
    tmp = string.split(';')
    for ele in tmp:
        tmp2 = ele.split('-')
        array.append(tmp2)
    print(array)
