# pip3 install flask tensorflow mediapipe opencv-contrib-python 

from flask import Flask, jsonify,render_template,request,Response,redirect,flash
import cv2
from werkzeug.utils import secure_filename
import recognise_gesture

########################################################################################
# video = cv2.VideoCapture(0)
app = Flask(__name__)
########################################################################################
@app.route('/',methods=["get","post"])
def start_app():
    if request.method=="GET":
        return render_template("start.html")
    else:
        data=request.data.decode('utf-8')
        print(data)
        return ""
@app.route('/main',methods=["get","post"])
def main_app():
    if request.method=="GET":
        return render_template("realTime.html")
    else:
        data=request.data.decode('utf-8')
        print(data)
        return ""
########################################################################################

def gen():
    global imLen
    cam=cv2.VideoCapture(0)
    cam.set(3,1080)
    cam.set(4,1024)
    while True:
        try:
            _,image=cam.read()
            image = cv2.flip(image, 1)
            if _:
                cv2.imwrite("live.png", image)
                print("Processing: live.png")
                image = recognise_gesture.detect(image_path = f"live.png")
                ret, jpeg = cv2.imencode('.jpg', image)
                frame = jpeg.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            # if cv2.waitKey(1)==ord('q'):
            #     break

        except Exception as e:
            print("Error : ",e)
########################################################################################
@app.route('/video_feed')
def video_feed():
    global video
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # webbrowser.open_new("http://127.0.0.1:5000")
    app.run( host='0.0.0.0',port=5000,debug=True) 