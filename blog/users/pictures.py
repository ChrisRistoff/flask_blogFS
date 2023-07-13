import os
from PIL import Image
from flask import url_for, current_app

def add_picture(pic_upload, username):
    #get the filename of the uploaded file
    filename = pic_upload.filename

    #get the file extension .jpg, .png, etc
    ext_type = filename.split('.')[-1]

    #"username" . "ext_type" = "username.jpg"
    storage_filename = str(username) + '.' + ext_type

    #get the path to the static folder
    filepath = os.path.join(current_app.root_path, 'static/profile_picture',
                            storage_filename)

    #resize the image
    output_size = (125, 125)

    #open the image
    pic = Image.open(pic_upload)

    #resize the image
    pic.thumbnail(output_size)

    #save the image
    pic.save(filepath)


    return storage_filename
