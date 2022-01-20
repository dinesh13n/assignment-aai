"""
This is the Entry point for Training the Machine Learning Model.

Written By: Dinesh Naik
Version: 1.0
Revisions: None

"""

# Doing the necessary imports
from sklearn.model_selection import train_test_split
from Train_Model import modelTuner
from file_operations import file_methods
from application_logging.logger import AppLog

#Creating the common Logging object


class trainModel:

    def __init__(self,execType="Training"):
        self.execType = execType
        self.applog = AppLog(self.execType)
        self.log = self.applog.log("sLogger")

    def trainingModel(self, X, list_of_clusters):
        # Logging the start of Training
        self.log.info('Start of Training')
        status = 0
        try:
            """parsing all the clusters and looking for the best ML algorithm to fit on individual cluster"""

            for i in list_of_clusters:
                cluster_data=X[X['Cluster']==i] # filter the data for one cluster

                # Prepare the feature and Label columns
                cluster_features=cluster_data.drop(['Y','Cluster'],axis=1)
                cluster_label= cluster_data['Y']

                # splitting the data into training and test set for each cluster one by one
                x_train, x_test, y_train, y_test = train_test_split(cluster_features, cluster_label, test_size=1 / 3, random_state=355)

                model_finder=modelTuner.Model_Finder(self.log,i) # object initialization

                #getting the best model for each of the clusters
                best_model_name,best_model=model_finder.get_best_model(x_train,y_train,x_test,y_test)

                #saving the best model to the directory.
                file_op = file_methods.File_Operation(self.log)
                save_model=file_op.save_model(best_model,best_model_name+str(i))

                # logging the successful Training
                self.log.info('Successful End of Training')
                status = 1

        except Exception as e:
            # logging the unsuccessful Training
            status=0
            self.log.info('Unsuccessful End of Training')
            raise Exception
        return status
