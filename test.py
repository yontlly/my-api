import copy
a=[1,2,3,[1,2,3]]
b=a.copy()
c=copy.deepcopy(a)
a.append(4)
a[3].append(4)
a[3].append(5)

print(a)
print(b)
print(c)