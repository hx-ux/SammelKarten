# SammelKarten -Linux Version
* check out the other branch for the windows version
more:
    * <a href="https://x0x0x0me.netlify.app/sammelkarten">See more results</a>

## Input image
![alt text](https://x0x0x0me.netlify.app/static/media/in.dd498c0e445738d7b27b.bmp)

## output image 
![alt text](https://x0x0x0me.netlify.app/static/media/7.e837ef6ab5b20689e16f.png)

![alt text](https://x0x0x0me.netlify.app/static/media/1.182c5db818598749ceda.png)


# How to install 
* tested with ubuntu 22.04

 
1. Install dependencies
```bash
sudo apt-get install libfftw3-double3 libgegl-0.4-0 libgimp2.0 libilmbase25 libopenexr25 libjpeg8 libopenexr25 libpng16-16 libqt5core5a libqt5gui5 libqt5widgets5 libtiff5
```

2. Download gmic .deb

```bash
wget https://gmic.eu/files/linux/gmic_3.1.4_ubuntu22-04_jammy_amd64.deb
sudo dpkg -i gmic_3.1.4_ubuntu22-04_jammy_amd64.deb
sudo apt-get install -f
```
3. Install requirements 

```python
pip install -r requirements.txt
```