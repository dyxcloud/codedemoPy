def odd():
    print('step 1')
    yield 1
    print('step 2')
    yield 3
    print('step 3')
    yield 5


def print_generator():
    o = odd()
    print("do next")
    print(next(o))
    print("do next")
    print(next(o))
    print("do next")
    print(next(o))
    print("do next")
    print(next(o))


'''生成杨辉三角列表'''


# 0=0 1=0+1 2=1+2 n=n+(n-1)

def triangles():
    a_list = [1]
    while 1:
        yield a_list
        tmp_list = a_list.copy()
        for i in range(len(a_list)):
            if i - 1 < 0:
                tmp_list[i] = a_list[i]
            else:
                tmp_list[i] = a_list[i] + a_list[i - 1]
            if i == (len(a_list) - 1):
                tmp_list.append(a_list[i])
        a_list = tmp_list.copy()


def triangles1():
    a_list = [1]
    while 1:
        yield a_list
        a_list = [0] + a_list + [0]
        a_list = [a_list[i] + a_list[i + 1] for i in range(len(a_list) - 1)]


def triangles2():
    a_list = [1]
    while True:
        yield a_list
        a_list = [1] + [a_list[i] + a_list[i + 1] for i in range(len(a_list) - 1)] + [1]


if __name__ == "__main__":
    # printGenerator()
    gen = triangles1()
    for length in range(10):
        print(next(gen))
