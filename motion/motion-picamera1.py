import picamera
import picamera.array

class MotionAnalyser(picamera.array.PiMotionAnalysis):
    def analyse(self, a):
        print a

with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)
    with MotionAnalyser(camera) as output:
        camera.start_recording('/dev/null', 'h264', motion_output=output)
        camera.wait_recording(10)
