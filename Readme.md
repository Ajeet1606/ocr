## Folder Structure

```text
doc-intel/
├── backend/
│   ├── app.py                # entry point (later becomes web server)
│   ├── cv/
│   │   ├── load_image.py
│   │   ├── preprocess.py
│   │   └── deskew.py
│   ├── utils/
│   │   └── image_io.py
│   ├── output/
│   │   ├── gray.jpg
│   │   ├── blurred.jpg
│   │   ├── threshold.jpg
│   │   └── final.jpg
│   └── requirements.txt
└── samples/
	├── invoice.jpg
	└── handwritten.jpg
```
