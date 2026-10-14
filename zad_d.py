def showEveryScnd(nums):
    for (i, num) in enumerate(nums):
        if i % 2 == 0:
            print(num)



nums = []
for i in range(10):
    nums.append(i)
showEveryScnd(nums)