import utlis.jbf.exif as exif

file = "E:\\Dropbox\\Biz\\_Inbox\\tagging\\2024-03-13_03-14-14_4665\\2024-03-13_03-14-14_4665_up2_up2.png"
# file = 'E:\\Dropbox\\Camera Uploads\\2022-12-22 11.31.31.jpg'
file = "E:\\Dropbox\\Biz\\_Inbox\\tagging\\2023-12-14_14-33-23_3526\\2023-12-14_14-33-23_3526_up2_up2.png"


exif.print_image_exif(file)
exif.update_image_exif(file)
exif.print_image_exif(file)

# d = {
#     "Creator": "Jane Smith",
#     "Credit": "Jane Smith, Smith Photography Ltd",
#     "Rights": "Copyright Smith Photography Ltd 2023",
#     "Web": "http://smithphotography.com/licensing/",
#     "Licensor": "http://www.mypictureagency.com/obtain-licence/"
# }

# test = lambda item : f"{item[0]}: {item[1]}"

# for item in d.items():
#     print(test(item))


# print(', '.join(list(map(lambda item: f'"{item[0]}: {item[1]}"', d.items()))))
