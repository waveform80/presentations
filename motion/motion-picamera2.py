import picamera
import picamera.array
import numpy as np

class MotionAnalyser(picamera.array.PiMotionAnalysis):
    def analyse(self, a):
        a = np.sqrt(
            np.square(a['x'].astype(np.float)) +
            np.square(a['y'].astype(np.float))
            ).clip(0, 255).astype(np.uint8)
        print a.max()

with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)
    with MotionAnalyser(camera) as output:
        camera.start_recording('/dev/null', 'h264', motion_output=output)
        camera.wait_recording(10)
