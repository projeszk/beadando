# Projekt eszközök beadandó
### Fejlesztői környezet kialakítása
**Szükséges szoftverek és könyvtárak:**

  * [Python 2.7.11](https://www.python.org/downloads/release/python-2711/)
  * [Numpy](https://sourceforge.net/projects/numpy/files/NumPy/)
  * [OpenCV 2.4.1](https://sourceforge.net/projects/opencvlibrary/files/opencv-win/2.4.10/)
    
**Komponensek telepítése:**

  1. Python telepítése a default helyre, ez többnyire a **C:/Python27/** könyvtár.
  2. Numpy telepítése a default Python telepítési könyvtárába, ha nem változtattatok a mappán a Python telepítésénél, akkor autómatikusan felajánlja.
  3. Python IDLE: `>>> import numpy`, ha nincs modul error üzenet akkor minden oké.
  4. OpenCV telpítése, tetszőleges könyvtárba.
  5. A **opencv/build/python/2.7** mappából a **cv2.pyd** fájl másolása a **C:/Python27/lib/site-packeges** mappába.
  6. Python IDLE: 
  
      ```python
      >>> import cv2
      >>> print cv2.__version__
      ```
      , ha nincs hibaüzenet, akkor a fejlesztői környezet telepítése sikeres és használatra kész.
  7. [Tutorials](http://docs.opencv.org/2.4/doc/tutorials/tutorials.html)

