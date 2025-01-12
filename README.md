# pyH5_GUI
A GUI to visualize hierarchical h5 files. Primarily, the GUI is designed to show XPCS data generated by pyCHX developed at the CHX beamline.

## How to install
wget https://repo.anaconda.com/archive/Anaconda3-2019.03-Linux-x86_64.sh \
chmod +x Anaconda3-2019.03-Linux-x86_64.sh\
./Anaconda3-2019.03-Linux-x86_64.sh\
source ~/.bashrc\
conda create --name pyGUI python=3\
conda activate pyGUI\
pip install numpy   pyqt5 h5py  pyqtgraph  PyOpenGL  tables pandas\
conda install matplotlib

## How to use
source activate pyGUI\
python XSH5View.py

## How to uncompress the tar.gz file
tar -xvf test.tar.gz\
tar -xvf test.tar

## Screenshot

![GUI] (https://raw.github.com/yugangzhang/pyH5_GUI/master/images/browser.png "a screenshot for the gui")\
![GUI] (https://raw.github.com/yugangzhang/pyH5_GUI/master/images/compare_curves.png "compare curves")\
![GUI] (https://raw.github.com/yugangzhang/pyH5_GUI/master/images/img1.png "two-D image")\
![GUI] (https://raw.github.com/yugangzhang/pyH5_GUI/master/images/img2.png "two-D image") 
