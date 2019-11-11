def odd():
    print('step 1')
    yield 1
    print('step 2')
    yield(3)
    print('step 3')
    yield(5)

def printGenerator():
    o = odd()
    print("do next")
    print(next(o))
    print("do next")
    print(next(o))
    print("do next")
    print(next(o))
    print("do next")
    print(next(o))

def triangles():
    '''生成杨辉三角列表'''
    # 0=0 1=0+1 2=1+2 n=n+(n-1) 
    list = [1]
    while 1:
        yield list
        tmplist = list.copy()
        for i in range(len(list)):
            if i-1<0:
                tmplist[i] = list[i]
            else:
                tmplist[i] = list[i]+list[i-1]
            if i == (len(list)-1):
                tmplist.append(list[i])
        list = tmplist.copy()


if __name__ == "__main__":
    # printGenerator()
    
    gen = triangles()
    for l in range(10):
        print(next(gen))
    