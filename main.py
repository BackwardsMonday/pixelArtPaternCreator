from flask import Flask, redirect, url_for, request, render_template, flash
import imageHandling as imHand
from PIL import Image
from PIL import ImageDraw 
from PIL import ImageFont
from werkzeug.utils import secure_filename
import os
app = Flask(__name__)

IMAGE_FILES = ["png", "jpg", "jpeg"]
UPLOAD_FOLDER = "./fileUploads"

palette = [253,217,181,
        0,0,0,
        0,139,139,
        31,117,254,
        13,152,186,
        115,102,189,
        180,103,77,
        255,170,204,
        29,172,214,
        253,219,109,
        149,145,140,
        28,172,120,
        240,232,145,
        93,118,203,
        255,117,56,
        238,32,77,
        255,83,73,
        192,68,143,
        252,40,71,
        146,110,174,
        247,83,148,
        255,255,255,
        252,232,131,
        197,227,132,
        255,174,66,
        255,255,255]

#TODO: user input should detirm palette
imPalette = Image.new("P", (24,24), 0)
imPalette.putpalette(palette)

@app.route("/fileHandeling", methods=["POST","GET"])
def fileHandeling():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part"
        file = request.files["file"]
        filename = file.filename
        if filename == "":
            return "Plese select a file"
        if filename.rsplit(".", 1)[1].lower() not in IMAGE_FILES:
            return "File must be image"
        
        filename = secure_filename(filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        file.close()
        
        with Image.open(filename) as imFile:
            palettedIm = imHand.quantizeToPalette(imFile, imPalette)
            pixeledIm = imHand.pixilizeImage(palettedIm)
            pixeledIm.save("outputs/webTest.png")
        return "secssues"
        
        
    
    
@app.route("/",methods=["POST", "GET"])
def mainPage():
    return render_template("uploadForm.html")
if __name__ == '__main__':
    app.run(debug=True)