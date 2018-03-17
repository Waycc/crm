
# for index in range(len(nums)):
#     indexs = index-index
#     num1 = nums[indexs]
#     del nums[indexs]
#     if num1 in nums:
#         nums.remove(num1)
#     else:
#         print(num1)
#         break


import re
a = re.match('([asbcdf]+|[eg]+)$','e')
b = 'a   +   b'
print(a,b.strip('  '))
