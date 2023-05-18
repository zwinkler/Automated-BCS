# Automated BCS

This is the repository for the Automatic Cattle Body Condition Scoring Project. Before starting, please refer to `Automatic_BCS.yml` or `Automatic_BCS.txt` files to recreate the environment.

## Data Usage

All relevent data is already collected and is available in both raw and processed formats here: (link to dryad). In the event that additional datasets need to be generated with different parameters, or if new data is gathered, `Bag_to_DGE.ipynb` should be used. Additional filtering and preprocessing operations can be applied to the raw `.bag` files should be done here. This file should be capable of selecting only images that fit the criteria for training outlined in PAPER. The file architecture should be in the format of `working_directory\bag_folder\classes\bag_files`and creates the output folder `working_directory\dataset_folder_processed\BCS_class\frame_number_DGE.tif`. It is highly recommended that the results are inspected manually. The resulting files should be seperated into training, validation, and testing folders manually.

Filter parameters can be easily tested using Intel's Realsense software and the supplied `.bag` files. This tool allows easy viewing of `.bag` files and filter effects in realtime.

## Training

Next, `BEiT_py_lightnining.ipynb` can be used for training a model. It relies on three seperate folders for training, validation, and testing, all with the same file architecture `Bag_to_DGE.ipynb` generates. All parameters used in PAPER should already be included in this notebook. Editing of training parameters can be done easily by modifying the trainer directly. Modifying the model itself is done by editing the ViTLightiningModule.

## Testing

`BEiT_py_lightning.ipynb` generates testing results for both exact matches and 'within one' matches. These results include confusion matrices, accuracy, precision, recall, F1 score and their weighted equivalents, as well as MSE for exact matches. If there are several models that need testing, this can be done quickly using the `Model_stats.ipynb` notebook. It takes every ViT model in a directory and generates a `.csv` file with the name and metrics associated with the model. This is useful when comparing results from different data sets or data set splits.

## Figures

`Figure_maker.ipynb` can be used to make figures related to the dataset. Each cell is independent of the others, and should work provided the filepath architecture is followed.

# Data set dosumentation

## Abstract

This dataset contains a collection of preclassified Criollo cow RGB+depth videos, as well as processed depth, grayscale, and edge images. The dataset was previously used to train convolutional neural networks and vision transformers to estimate body condition scores of cattle, and will be useful to other researchers in need a high quaility visual dataset that incorporates depth for the purposes of a three dimensional representations of cattle. The availability of compatible software and image processing packages makes this dataset very robust and applicable to other areas of both agricultural and machine learning research. This dataset has several features that make it a good test of machine learning algorithms such as low sample uniqueness and a slightly subjective metric.


## Methods

This dataset is composed of videos saved as Rosbag files recorded via an Intel Realsense D435i RGB+depth camera. Each video is unfiltered and unprocessed, and contains RGB and depth channels. These videos are easily processed using the `pyrealsense2` library, created by Intel. Filter parameter effects can be observed in realtime via the Intel Realsense Viewer software (hyperlink this). Most  videos are recorded at a resolution of 640x480, with several having 848x480. This mistake in resolution is easily recified in postprocessing. During recording, roughly a third the cows were allowed to stand in a lane, and the rest were allowed to walk through the lane unimpeded.

## Usage Notes


The easiest way to manipulate each `.bag` file is to use the `pyrealsense` library, as intel seems to have used their own conventions. Each depth image generated by the video is 16 bits deep, and special care should be taken when assigning data types so as to not truncate each value. Many image formats are incapable of 16-bit images, and some machine learning librarys will reject an image that is forced to have 16 bits of depth. Therefore, we encourage users to normalize each depth image before converting to an 8-bit data type so as to minimize data corruption.

In the article, each image was assumed to be unique, and this created some unwanted effects. If the application that this dataset will be used for requires unique images, use as few as possible from each cow. Images generated from videos should be temporally distant from each other so as to maximize uniqueness.
