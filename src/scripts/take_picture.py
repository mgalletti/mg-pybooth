import cv2
import datetime
import time
import urllib
import numpy as np
import os


def take_picture_2(url, img_name):
    """
    Takes a picture from a url. This is particularly useful if you have an IP webcam
    """

    # Example url='http://192.168.1.3:8080/photo.jpg'
    imgResp=urllib.request.urlopen(url)
    if not imgResp:
        raise Exception(f"couldn't acquire photo from URL: {url}")
    imgNp=np.array(bytearray(imgResp.read()), dtype=np.uint8)
    img=cv2.imdecode(imgNp, -1)
    cv2.imwrite(img_name, img)
    imgResp.close()

def take_picture(ip_web_cam_url: str, image_name: str = ""):
    """
    Takes a picture from an IP camera stream
    """
    try:
        camera = cv2.VideoCapture(ip_web_cam_url)
        if camera.isOpened() is False:
            raise IOError("Cannot open webcam")

        return_value, image = camera.read()
        if not return_value:
            print("Couldn't take a picture")
            return
        
        image_name = image_name or f"opencv_{datetime.datetime.today()}.png"
        cv2.imwrite(image_name, image)
    except:
        raise ValueError("Errors while taking pictures :(")
    finally:
        camera.release()
    
if __name__ == "__main__":

    os.system('say "ready?"')
    time.sleep(1)
    # "say" command makes you mac talking!
    os.system('say "go!"')
    for params in [
        ("rtsp://192.168.1.3:8080/h264.sdp",f"img_vid_{datetime.datetime.now()}.png"),
    ]:
        url, name = params
        take_picture(url, name)

    for par in [
        ('http://192.168.1.3:8080/photo.jpg', f"img_url_pic_{datetime.datetime.now()}.png", "first pic"),
        ('http://192.168.1.3:8080/photoaf.jpg', f"img_url_af_pic_{datetime.datetime.now()}.png", "second pic"),
    ]:
        url, name, say = par
        os.system(f'say "{say}."')
        take_picture_2(url, name)
    os.system('say "Beer time."')

    print('yay!')
