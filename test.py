# import copy
# a=[1,2,3,[1,2,3]]
# b=a.copy()
# c=copy.deepcopy(a)
# a.append(4)
# a[3].append(4)
# a[3].append(5)
#
# print(a)
# print(b)
# print(c)

# import os
#
# def dir_base(*fileName: str):
#     print(os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), *fileName))
#
# dir_base('config/yaml')
#
# for i in range(10):
#     print('asda_%s' % i)


# def maxSubArray(nums):
#     """
#     :type nums: List[int]
#     :rtype: int
#      """
#     for i in range(1, len(nums)):
#         nums[i] = nums[i] + max(nums[i - 1], 0)
#     return max(nums)
#
# a=[-2,-1,-8,-2,-8,-2,-1,-5,-4]
# print(maxSubArray(a))
# print(a)


# import base64
# import re
# import time
#
# a='base64`kaifangg`'
# for e in re.findall('base64`(.*)`', a):
#     b=a.replace(f'base64`{e}`', str(base64.b64encode(e.encode("utf-8"))))
#     print(b)
#
# content='eval`12+1`'
# for e in re.findall('eval`(.*)`', content):
#     content = content.replace(f'eval`{e}`', str(eval(e)))
#     print(content)
#
#
# print(str(int(time.time()+50000)))

print(5*2+5*20*3+5*20*10*4+5*20*10*10*4)
print(5*2+5*25*3+5*25*15*4+5*25*15*15*4)
print(5*2+5*22*3+5*22*13*4+5*22*13*13*4)