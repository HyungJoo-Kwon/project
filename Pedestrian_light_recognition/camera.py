#camera.py
import numpy as np
import cv2
import time

class VideoCamera(object):
    def __init__(self):

        self.video = cv2.VideoCapture(0)
        self.min_confidence = 0.5
        self.width = 640
        self.height = 0
        self.show_ratio = 1.0
        self.title_name = 'Custom Yolo'
        # Load Yolo
        self.net = cv2.dnn.readNet("data/custom-train-yolo_128pic.weights", "data/custom-train-yolo.cfg")
        self.classes = []
        with open("data/classes.names", "r") as f:
            self.classes = [line.strip() for line in f.readlines()]
        self.color_lists = np.random.uniform(0, 255, size=(len(self.classes), 3))

        self.layer_names = self.net.getLayerNames()
        self.output_layers = [self.layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
    
    def detectAndDisplay(self,image):
        h, w = image.shape[:2]
        self.height = int(h * self.width / w)
        img = cv2.resize(image, (self.width, self.height))

        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), swapRB=True, crop=False)

        self.net.setInput(blob)
        outs = self.net.forward(self.output_layers)
        
        confidences = []
        names = []
        boxes = []
        colors = []

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > self.min_confidence:
                    center_x = int(detection[0] * self.width)
                    center_y = int(detection[1] * self.height)
                    w = int(detection[2] * self.width)
                    h = int(detection[3] * self.height)

                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    names.append(self.classes[class_id])
                    colors.append(self.color_lists[class_id])

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, self.min_confidence, 0.4)
        print(indexes)
        font = cv2.FONT_HERSHEY_PLAIN
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = '{} {:,.2%}'.format(names[i], confidences[i])
                color = colors[i]
                print(i, label, x, y, w, h)
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                cv2.putText(img, label, (x, y - 10), font, 1, color, 2)
                if names[i] == "red_light":
                    cv2.putText(img, "STOP!", (20, 50), font, 4, (0,0,255), 3)
                else:
                    cv2.putText(img, "GO!", (20, 50), font, 4, (0,255,0), 3)
        return img# cv2.imshow(self.title_name, img)
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        image = self.detectAndDisplay(image)
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

