def showEven(nums):
    for num in nums:
        if num % 2 == 0:
            print(num)


nums = []
for i in range(10):
    nums.append(i)
showEven(nums)

