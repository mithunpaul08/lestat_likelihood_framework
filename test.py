
from heapq import *


class MedianFinder(object):

    def __init__(self):
        self.maxheap = []
        self.minheap = []

    def addNum(self, num):
        """
        :type num: int
        :rtype: None
        """
        heappush(self.maxheap, -1 * num)

        if self.maxheap and self.minheap and (-1 * self.maxheap[0] > self.minheap[0]):
            val = -1 * heappop(self.maxheap)
            heappush(self.minheap, val)



        if len(self.maxheap) > len(self.minheap) + 1:
            val = -1 * heappop(self.maxheap)
            heappush(self.minheap, val)

        if len(self.minheap) > len(self.maxheap) + 1:
            val = heappop(self.minheap)
            heappush(self.maxheap, -1 * val)

    def findMedian(self):
        """
        :rtype: float
        """
        if len(self.maxheap) > len(self.minheap):
            return -1 * self.maxheap[0]

        if len(self.minheap) > len(self.maxheap):
            return self.minheap[0]

        return (-1 * self.maxheap[0] + self.minheap[0]) / 2

# Your MedianFinder object will be instantiated and called as such:
# obj = MedianFinder()
# obj.addNum(num)
# param_2 = obj.findMedian()

mf= MedianFinder()
mf.addNum(1)
mf.addNum(2)
print(mf.findMedian())
mf.addNum(3)

>>>>>>> c36e9fb0c295fb05601cc055a8edfafc12430ce6
