### Yolov5
+ Yolo.ipynb
    + Yolov5s
    + 1024x1024 / train 80% val 20% / --img 832 --batch 16 --epochs 30 / --img 640 --conf 0.15 --iou 0.5 / 0.024
+ Yolo2.ipynb
    + Yolov5l
    + 1024x1024 / train 80% val 20% / --img 640 --batch 16 --epochs 200 / --img 640 --conf 0.15 --iou 0.4 / 0.048

+ Yolo3.ipynb
    + Yolov5s
    + 5-Fold 방식
    + 1024x1024 / 5-Fold train 80% val 20% / --img 640 --batch 16 --epochs 40 X5 / --img 640 --conf 0.15 --iou 0.4 / 0.098 

+ Yolov4.ipynb
    + Yolov5s
    + 5-Fold 방식
    + 1024x1024 / 5-Fold train 80% val 20% / --img 832 --batch 16 --epochs 40 X5 / --img 832 --conf 0.2 --iou 0.4 / 0.126
    + 1024x1024 / 5-Fold train 80% val 20% / --img 832 --batch 16 --epochs 40 X5 / --img 832 --conf 0.4 --iou 0.4 / 0.113
    + 1024x1024 / 5-Fold train 80% val 20% / --img 832 --batch 16 --epochs 40 X5 / --img 832 --conf 0.15 --iou 0.4 / 0.13


+ Yolo5.ipynb
    + Yolov5m
    + 1024x1024 / train 80% val 20% / --img 1024 --batch 16 --epochs 50 / --img 1024 --conf 0.15 --iou 0.4 / 0.135
    + 1024x1024 / train 80% val 20% / --img 1024 --batch 16 --epochs 50 / --img 1024 --conf 0.2 --iou 0.5 / 0.133
    + 1024x1024 / train 80% val 20% / --img 1024 --batch 16 --epochs 50 / --img 1024 --conf 0.1 --iou 0.5 / 0.133
    + 1024x1024 / train 80% val 20% / --img 1024 --batch 16 --epochs 50 / --img 1024 --conf 0.15 --iou 0.7 / 0.137
    + test 시간 4분 29초

+ Yolo6.ipynb
    + Yolo5 + 2-class Efficientnet
    + 최고치 0.185



+ 진행한 Yolo parameter
    + 이미지 / 전처리 / train / detect / result
    + 1024x1024 / train 80% val 20% / --img 832 --batch 16 --epochs 30 / --img 640 --conf 0.15 --iou 0.5 / 0.024
    + 1024x1024 / train 80% val 20% / --img 640 --batch 16 --epochs 200 / --img 640 --conf 0.15 --iou 0.4 / 0.048
    + 1024x1024 / 5-Fold train 80% val 20% / --img 640 --batch 16 --epochs 40 X5 / --img 640 --conf 0.15 --iou 0.4 / 0.098 
    + 1024x1024 / 5-Fold train 80% val 20% / --img 832 --batch 16 --epochs 40 X5 / --img 832 --conf 0.2 --iou 0.4 / 0.126
    + 1024x1024 / 5-Fold train 80% val 20% / --img 832 --batch 16 --epochs 40 X5 / --img 832 --conf 0.4 --iou 0.4 / 0.113
    + 1024x1024 / 5-Fold train 80% val 20% / --img 832 --batch 16 --epochs 40 X5 / --img 832 --conf 0.15 --iou 0.4 / 0.13
    + 1024x1024 / train 80% val 20% / --img 1024 --batch 16 --epochs 50 / --img 1024 --conf 0.15 --iou 0.4 / 0.135
    + 1024x1024 / train 80% val 20% / --img 1024 --batch 16 --epochs 50 / --img 1024 --conf 0.2 --iou 0.5 / 0.133
    + 1024x1024 / train 80% val 20% / --img 1024 --batch 16 --epochs 50 / --img 1024 --conf 0.1 --iou 0.5 / 0.133
    + 1024x1024 / train 80% val 20% / --img 1024 --batch 16 --epochs 50 / --img 1024 --conf 0.15 --iou 0.7 / 0.137

### 2_class Efficientnet 

+ classes-2.ipynb
    + Efficientnet
    + Accuracy : 0.9