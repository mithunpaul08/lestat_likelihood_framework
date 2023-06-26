import collections


def maxSubArray(nums, k):
    l = 0
    r = l+k-1
    summax=0
    subarray = nums[l:r + 1]
    count = collections.Counter(subarray)

    while r <len(nums):
        r = r+1
        if nums[r] in count and nums[r]==1:
        curr = sum(subarray)
        if
            summax= max(summax,curr)
        else:
            curr = curr + nums[r]
            curr =curr - nums[l]
        r = r + 1
        l = l + 1
    return summax

nums=[4,4,4]
l=0
r=2
print(nums[l:r])
k = 3
print(maxSubArray(nums,k))
