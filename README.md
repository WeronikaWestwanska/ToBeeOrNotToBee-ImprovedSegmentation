# Title:
ToBeeOrNotToBee-ImprovedSegmentation 

# Short description

This code is a supplement to the article by Weronika W. Westwańska and Jerzy S. Respondek titled:
"Improving Object Recognition and Segmentation using Single Point Loctaion Algorithm and U-Net Convolutional Neural Networks".

The goal of this work was to examine a novel method for segmentation of Object Of Interest (OOI) in colour digital images. To recognise OOI in an image we use a modern Deep Learning technique called U-Net Convolutional Neural Network (UNETCNN). Presented algoritm is based on our earlier work (ToBeeOrNotToBee -  https://github.com/WeronikaWestwanska/ToBeeOrNotToBee) and is improved according to segmentation of OOI.

The data comes from https://www.kaggle.com/jonathanbyrne/to-bee-or-not-to-bee. 

Details of this method are clearly described in the source code comments.


# Description of project contents:

- `data/labelled.train` - images used in training U-Net network,
- `data/labelled.validate` - all available images which may be used in calculation of relative bees counting error
- `data/testing.experiment` - images used in experiments described in "Improving Object Recognition and Segmentation using Single Point Loctaion Algorithm and U-Net Convolutional Neural Networks"
- `data/labels.train.db` - SQLite3 database with coordinates of bees images from data\labelled.train directory
- `data/labels.validate.db` - SQLite3 database with coordinates of bees images from data\labelled.validate directory
- `data/testing.experiment.db` - SQLite3 database with coordinates of bees images from data\testing.experiment
- `.editorconfig` - settings file for Visual Studio.
- `BeesDataGenerator.py` - routines used in modelling data generation,
- `BeesDataReader.py` - routines for reading SQLite3 database and its contents where bees coordinates are stored
- `BeesDataTester.py` - routines for calculating OOIs,
- `BeesHeatMap.py` - routines for OOI heatmap generation,
- `experiment.sh` - simple bash script to automate process of training,
- `FileTools.py` - routines for creating directory, 
- `Parameters.py` - parameters values used in training and segmentation,
- `readme.md` - this file,
- `RectangleSearcher.py` - searches for regions of interest,
- `ToBeeOrNotToBee.sln` - Visual Studio python project file,
- `ToBeeOrNotToBee.pyproj` - Visual Studio python project file,
- `ToBeeOrNotToBee.pyperf` - Visual Studio python project file,
- `Tools.py` - various routines for training, segmentation, saving data
- `Unet.py` - routines for U-Net modelling.


Note: Please bear in mind that what we call in the Python code as train set is an equivalent to modelling set in the article, and validate set is an equivalent to segmentation set in the article. This confusion is caused by naming conventions made at a time of starting the work, which was later clarified when summarising it in a form of the article.

# How to use

IMPORTANT! Please download from https://github.com/WeronikaWestwanska/ToBeeOrNotToBee:
- `data/labelled.train` 
- `data/labelled.validate` 
Those are not included in this repository as they are already stored on github. You need them to generate the model and train the network.

In order to perform a whole end-to-end process of data generation, training, segmentation and counting of OOIs the user needs to decide on values of `Parameters.py` (or leave them how they are by default) and then perform the following commands:
```
python Main.py --generate --train
python Main.py --segment --count
```

The first command will generate modelling data and train UNet network. The results will be stored by default in `data/train_r16` (depending on value of 'bee_radius').
The second command will use model stored in `data/train_r16` and create a new directory `data/segmented`. This bit can take at least 2 hours (depending on value of sliding_window_step in `Parameters.py`) as well as graphics card.

**Note**: Please ensure when training the U-Net network that the process is not stuck at the same validation accuracy (sometimes it can happen due to a bug in Keras). In such case, delete the contents of `data/train_r16` directory and start over. Typical validation accuracy should reach at least 94%.

To test the whole available database of images in Parameters.py file, choose:
- "labelled_validate_db"  : 'data/labels.validate.db',
- "labelled_validate_dir" : 'data/labelled.validate/',

To test a dataset of files chosen for experiments described in "Improving Object Recognition and Segmentation using Single Point Loctaion Algorithm and U-Net Convolutional Neural Networks", choose:
- "labelled_validate_db"  : 'data/testing.experiment.db',
- "labelled_validate_dir" : 'data/testing.experiment/',

**Last Modified**: 2020/03/14
