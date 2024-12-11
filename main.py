from flask import Flask, redirect, url_for, request, render_template
app = Flask(__name__)

@app.route("/successTest", methods=["POST","GET"])
def successTest():
    if request.method == "POST":
        file = request.files["file"]
        text = file.read(1)
        file.close()
        return text
    
    
@app.route("/",methods=["POST", "GET"])
def test():
    return render_template("uploadForm.html")
if __name__ == '__main__':
    app.run(debug=True)