# Projekt eszközök beadandó
### Fejlesztői környezet kialakítása
**Szükséges szoftverek és könyvtárak:**

  * [Python 2.7.11](https://www.python.org/downloads/release/python-2711/)
  * [Numpy](https://sourceforge.net/projects/numpy/files/NumPy/)
  * [OpenCV 2.4.11 Windows](https://sourceforge.net/projects/opencvlibrary/files/opencv-win/2.4.11/)
  * [OpenCV 2.4.11 source](https://github.com/Itseez/opencv/archive/2.4.11.zip)
    
**Komponensek telepítése:**

***Windows***

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

***Ubuntu***

  1. Az újabb verziók már tartalmazzák a 2.7.11-es Python fordítót
  2. Csomagoljuk ki a letöltött openCV forrást, hozzunk létre benne egy release könyvtárat
  3. Nyissunk terminált és a következő parancsokat adjuk ki:
    *  sudo apt-get install build-essential
    *  sudo apt-get install cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
    *  sudo apt-get install python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev
    *  cd opencv_dir/release
    *  cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local ..
    *  make
    *  sudo make install
    *  python

        ```python
        >>> import numpy
        >>> import cv2
        >>> print cv2.__version__
        ```
  4. Ha nincs hibaüzenet, akkor a fejlesztői környezet használatra kész


