# Definition for singly-linked list.
from typing import List, Optional
from hashlib import sha256
class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        if not nums:
            return []
        ret =[]
        nums = sorted(nums)
        n = len(nums)
        unique ={}
        for i in range(n-1):
            l = i + 1
            r = n - 1
            while l<r:
                if i!=l and i !=r and l!=r :
                    vali=nums[i]
                    valr=nums[r]
                    vall=nums[l]
                    sum = nums[i] + nums[l] + nums[r]
                    if sum == 0:
                        triplet =(nums[i], nums[l], nums[r])
                        if triplet not in unique:
                            unique[triplet]=1
                            ret.append(list(triplet))
                            l = l + 1
                            r = r - 1
                    if sum < 0:
                        l = l + 1
                    if sum >0:

                        r = r - 1
        return ret
nums=[-1,2,-1,-1,2,-1,5,-4,-1]
sol = Solution()
print(sol.threeSum(nums))