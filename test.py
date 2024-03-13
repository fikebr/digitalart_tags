file = 'imagefile.png'
ext = ['png', 'jpg']

if file.endswith(tuple(ext)):
    print("yes")
else:
    print("no")