def squareArr(arr):
    l = 0
    r = len(arr) - 1
    ret = []
    while l <= r:
        lsquare = arr[l] * arr[l]
        rsquare = arr[r] * arr[r]
        if lsquare > rsquare:
            ret.append(lsquare)
            l = l+1
        else:
            ret.append(rsquare)
            r = r-1
    return ret[::-1]

arr=[1,2,3,4]
# arr=[-1,-2,3,4]
#arr=[]
#arr=[-1,-1,-1]
print(squareArr(arr))
