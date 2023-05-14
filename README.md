# Automated-BCS
Automated BCS

This is the repository for the Automatic Cattle Body Condition Scoring Project. Before starting, please refer the the included .yml of .txt files to recreate te environment.

In the event that more data is needed, please gather it according to the procedure outlined in the <PAPER>, then use BAG_to_DGE to extract the data. It should extract high quality data by itself provided the data gathering procedure is followed correctly. It is still recommended that the results are reviewed manually. It should output the resulting images to working_directory\dataset_folder_processed\BCS_class\frame_number_DGE.tif, and assumes the bag files are in this architecture: working directory (that this notebook is in)\dataset folder\BCS class each bagfile belongs to\bagfiles themselves.
  
  Next, BEiT_py_lightning can be used for training a model. It relies on three seperate folders for training, validation, and testing, as well as a csv containing the names and labels of all samples used for training.
  
  If there are several models that need testing, this can be done quickly using the model_stats notebook. It takes every model in a directory and generates a csv file with the name and metrics associated with the model.
