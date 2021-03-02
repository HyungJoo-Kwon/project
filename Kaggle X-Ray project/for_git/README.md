# VinBigData Chest X-ray abnormalitiy detection
***
## Contents
    + Total working environment: Kaggle Notebook, Google Colaboratory
    + Convert_Download
        - Period
            + Convert Dicom to PNG CODE (210215 ~ 210216)
            + All dataset download in local computer & Filter the file have lesion in patient & Upload, Deploy (210217)
        - Dicom (191.82 GB)
        - PNG (train dataset: 12.1 GB)
        - PNG (test dataset: 7.31 GB)
    + CutMix
        - Period: 210215 ~ 210217
        - Issue: GPU memory(Google Colab / Not working done), Epoch time(about 46.8 minutes)
    + DetectoRS (ing)
        - Period: 210218 ~ 210223
        - Look for paper, Training sample code in Kaggle(or Colab)
        - Log
            + 210218 : Examine the paper about DetectoRS & Run sample data.
            + 210219 ~ 210222 : Setting config files about VinBigData(Kaggle) and fix errors.
                + Error issue
                  1. error of DCN / solve: self.conv2 is None in DetectoRS_ResNet Model.
                  2. about coco dataset format / solve: fix parameters(num_classes)
                  3. --NotebookApp.iopub_data_rate_limit / solve: Expanding data rate limit in Jupyter Notebook using CMD
                  4. Json.dump (Need to change np.uint to class 'int') / solve: DataFrame.to_numpy().tolist()
