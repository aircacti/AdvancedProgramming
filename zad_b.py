
def doMath1(nums ):
    newNums = []

    for num in nums:
        newNums.append(num*2)

    return newNums

def doMath2(nums):
    return [ num*2 for num in nums ]

input = [1,2,3,4,5]
print(doMath1(input))
print(doMath2(input))