def addr_range(input):

    list = []
    last_octet = input.split('.')[3]
    other_octets = f'''{input.split('.')[0]}.{input.split('.')[1]}.{input.split('.')[2]}.'''
    first_digit = int(last_octet.split("-")[0])
    second_digit = int(last_octet.split("-")[1])

    for addr in range(first_digit, second_digit+1):
        list.append(other_octets + str(addr))

    return list