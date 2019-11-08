# 位运算加法
def add(a, b):
    result = a
    carry = b
    while carry:
        tmp = result
        result = tmp ^ carry
        carry = (tmp & carry) << 1
    return result


# print(add(13, 17))
a = (4 | 6)
# a = add(~354523,1)
a = 9 >> 2

a = 2147483647
# a = (a >> 31) #| (~((~a + 1) >> 31) + 1)
a = 4 ^ 3 ^ 4


# print(a)


# a = 13
# print(bin(a))
# print(0b110)

# a = 3
# b = 4
# print("a = " + str(a) + ", b= " + str(b))
# a ^= b
# b ^= a
# a ^= b
# print("a = " + str(a) + ", b= " + str(b))
#

def test(a):
    tmp = a >> 31
    return (a ^ tmp) - tmp


# print(test(-11))
# print(2 ^ 1)
print(64<<3)
# print(~-10)
# print(-10 ^ -1 - (-1))