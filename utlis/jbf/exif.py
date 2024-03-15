# https://iptc.atlassian.net/wiki/spaces/PMD/pages/649592833/Reading+and+writing+IPTC+metadata+in+Python+using+pyexiftool
# https://smarnach.github.io/pyexiftool/
# python -m pip install -U pyexiftool


from exiftool import ExifToolHelper


def print_image_exif(file):
    try:
        with ExifToolHelper() as et:
            for d in et.get_metadata(file):
                for k, v in d.items():
                    print(f"{k} = {v}")
    except KeyError:
        raise


def update_image_exif(file):
    key1 = "-IPTC:Caption-Abstract=this is a description"  # ID-120
    key2 = "-IPTC:ObjectName=Driftwood on the Beach"  # 5
    key3 = "-IPTC:Keywords=beach, driftwood, ocean, storm, waves, wind, trees, nature, power, fury, contrast, dramatic, intense"  # 25
    with ExifToolHelper() as et:
        # et.execute("-XMP-dc:creator=Jane Smith","-XMP-photoshop:Credit=Jane Smith, Smith Photography Ltd","-XMP-dc:rights=Copyright Smith Photography Ltd 2023","-XMP-xmpRights:WebStatement=http://smithphotography.com/licensing/","-XMP-plus:LicensorURL=http://www.mypictureagency.com/obtain-licence/","test-image.jpg")
        et.execute(key1, key2, key3, file)
        print(key1)


# % exiftool -XMP-dc:creator -XMP-photoshop:Credit -XMP-dc:rights -XMP-xmpRights:WebStatement -XMP-plus:LicensorURL -XMP-iptcExt:DigitalSourceType  test-image.jpg
# Creator                         : Jane Smith
# Credit                          : Jane Smith, Smith Photography Ltd
# Rights                          : Copyright Smith Photography Ltd 2023
# Web Statement                   : http://smithphotography.com/licensing/
# Licensor URL                    : http://www.mypictureagency.com/obtain-licence/


# IPTC:Caption-Abstract
# IPTC:ObjectName
# IPTC:Keywords
