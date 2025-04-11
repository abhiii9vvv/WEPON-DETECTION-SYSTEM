# 🔫 Weapon Detection using YOLOv5

A real-time weapon detection system using the YOLOv5 object detection algorithm. This project uses a custom-trained model on a dataset of weapons (guns, knives) to identify potential threats in images, videos, or live webcam feeds.

---

## 📁 Project Structure

```
├── yolov5/                       # YOLOv5 repo
├── weapon-dataset/              # Custom dataset
│   ├── train/
│   ├── valid/
│   ├── test/
│   └── data.yaml
├── runs/                        # Training results
│   └── train/weapon_detector/
└── detect.py                    # Detection script
```

---

## 🚀 Features

- 🔍 Detects weapons (e.g., guns and knives) in real-time
- 🎥 Supports image, video, and webcam inputs
- 🧠 Custom-trained YOLOv5 model
- 📊 Tracks confidence, bounding boxes, and results

---

## 📦 Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

(Inside `yolov5/`)

---

## 📥 Dataset

The dataset was downloaded and customized using [Roboflow](https://universe.roboflow.com/).

Includes:
- Images with YOLOv5 TXT annotations
- Custom `data.yaml` with classes: `gun`, `knife`

---

## 🏋️‍♂️ Training

Run this command to train:

```bash
python train.py --img 640 --batch 16 --epochs 50 --data weapon-dataset/data.yaml --weights yolov5s.pt --name weapon_detector
```

---

## 🎯 Inference / Detection

Run detection on webcam, image, or video:

```bash
# Webcam
python detect.py --weights runs/train/weapon_detector/weights/best.pt --source 0

# Image
python detect.py --weights runs/train/weapon_detector/weights/best.pt --source path/to/image.jpg

# Video
python detect.py --weights runs/train/weapon_detector/weights/best.pt --source path/to/video.mp4
```

Detected results are saved in `runs/detect/`.

---

## 🧠 Classes Detected

- `gun`
- `knife`

(Modify in `data.yaml` as needed)

---

## 📊 Results

Training accuracy, loss, and mAP graphs are saved in `runs/train/weapon_detector/`.

You can visualize predictions in `runs/detect/`.

---

## 🛠 Future Improvements

- Add alert system (buzzer/email notification)
- Deploy on edge devices (e.g., Jetson Nano, Raspberry Pi)
- Train on more diverse dataset (other weapons, scenarios)

---

## 🙌 Acknowledgements

- [Ultralytics YOLOv5](https://github.com/ultralytics/yolov5)
- [Roboflow Datasets](https://universe.roboflow.com/)
- OpenCV, PyTorch, and the AI/ML community

---

## 📸 Demo

> *(Add screenshots or a short video/GIF here if you can)*

---

## 💬 License

This project is for educational/research purposes only. Use responsibly.
