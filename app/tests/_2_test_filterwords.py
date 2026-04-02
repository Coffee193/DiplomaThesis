aa = 'list All tAsks'
aa = aa.lower()
print(aa)
for i in ['any', 'all', 'list']:
    aa = aa.replace(i, '')
aa = aa.strip() # removes leading and trailing spaces
print(aa)