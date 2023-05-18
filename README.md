# Automated BCS

This is the repository for the Automatic Cattle Body Condition Scoring Project. Before starting, please refer to "Automatic_BCS.yml" or 'Automatic_BCS.txt' files to recreate the environment. te sada

## Data Usage

All relevent data is already collected and is available in both raw and processed formats. In the event that additional datasets need to be generated with different parameters, or if new data is gathered, 'BAG_to_DGE.ipynb' should be used. Additional filtering and preprocessing operations can be applied to the raw '.bag' files should be done here. This file should be capable of selecting only images that fit the criteria for training outlined in PAPER. The file architecture should be in the format of 'working_directory\bag_folder\classes\bag_files' and creates the output folder 'working_directory\dataset_folder_processed\BCS_class\frame_number_DGE.tif'. It is highly recommended that the results are inspected manually. The resulting files should be seperated into training, validation, and testing folders manually.

## Training

Next, 'BEiT_py_lightning.ipynb' can be used for training a model. It relies on three seperate folders for training, validation, and testing. All parameters used in PAPER should already be included in this notebook.

## Testing

If there are several models that need testing, this can be done quickly using the 'model_stats.ipynb' notebook. It takes every ViT model in a directory and generates a .csv file with the name and metrics associated with the model.

## Figures

'Figure_maker.ipynb' can be used ot make figures related to the dataset. Each cell is independent of the others, and should work provided the filepath architecture is followed.
