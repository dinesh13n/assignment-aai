import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from application_logging.logger import AppLog
from sklearn.preprocessing import StandardScaler
from statsmodels.stats.outliers_influence import variance_inflation_factor
from Data_Preprocessing import clustering



class Preprocessor:
    """
    This class shall  be used to clean and transform the data before training.

    Written By: Dinesh Naik
    Version: 1.0
    Revisions: None

    """

    def __init__(self,execType='Training'):
        self.execType = execType
        self.applog = AppLog(self.execType)
        self.log = self.applog.log("sLogger")

    def impute_missing_values(self, data):
        """
                                        Method Name: impute_missing_values
                                        Description: This method replaces all the missing values in the Dataframe using KNN Imputer.
                                        Output: A Dataframe which has all the missing values imputed.
                                        On Failure: Raise Exception

                                        Written By: Dinesh Naik
                                        Version: 1.0
                                        Revisions: None
                     """
        self.log.info('Entered the impute_missing_values method of the Preprocessor class')
        self.data= data
        try:
            imputer=KNNImputer(n_neighbors=3, weights='uniform',missing_values=np.nan)
            self.new_array=imputer.fit_transform(self.data) # impute the missing values
            # convert the nd-array returned in the step above to a Dataframe
            self.new_data=pd.DataFrame(data=self.new_array, columns=self.data.columns)
            self.log.info('Imputing missing values Successful. Exited the impute_missing_values method of the Preprocessor class')
            return self.new_data
        except Exception as e:
            self.log.info('Exception occured in impute_missing_values method of the Preprocessor class. Exception message:  ' + str(e))
            self.log.info('Imputing missing values failed. Exited the impute_missing_values method of the Preprocessor class')
            raise Exception()

    def standard_scale_data(self, data, datacol):
        """
                                        Method Name: Standard Scale Data
                                        Description: This method make all the column in same scale.
                                        Output: A Dataframe which has all the column value would be in same scale.
                                        On Failure: Raise Exception

                                        Written By: Dinesh Naik
                                        Version: 1.0
                                        Revisions: None
                     """
        self.log.info('Entered the standard_scate_data method of the Preprocessor class')
        self.data= data
        self.datacol = datacol
        try:
            scaler = StandardScaler()
            self.new_data = pd.DataFrame(scaler.fit_transform(self.data[self.datacol]),columns=self.datacol)
            self.log.info('Data scalling Successful. Exited the standard_scale_data method of the Preprocessor class')
            return self.new_data
        except Exception as e:
            self.log.info('Exception occured in standard_scale_data method of the Preprocessor class. Exception message: ' + str(e))
            self.log.info('Data scalling failed. Exited the standard_scale_data method of the Preprocessor class')
            raise Exception()

    def vif_data(self, data, datacol):
        """
                                        Method Name: vif_data
                                        Description: VIF method pick each feature and regress it against all of the other features.
                                        Output: A Dataframe which has the feature and there collinearity index.
                                        On Failure: Raise Exception

                                        Written By: Dinesh Naik
                                        Version: 1.0
                                        Revisions: None
                     """
        self.log.info('Entered the vif_data method of the Preprocessor class')
        self.data= data
        self.datacol = datacol
        try:
            # VIF dataframe
            self.new_data = pd.DataFrame()
            self.new_data['feature'] = self.data[datacol].columns

            # calculating VIF for each feature
            self.new_data["VIF"] = [variance_inflation_factor(self.data.values, i) for i in range(len(self.data[datacol].columns))]
            
            self.log.info('feature VIF calculation Successful. Exited the vif_data method of the Preprocessor class')
            return self.new_data
        except Exception as e:
            self.log.info('Exception occured in vif_data method of the Preprocessor class. Exception message: ' + str(e))
            self.log.info('VIF calculation failed. Exited the standard_scale_data method of the Preprocessor class')
            raise Exception()


    def clustering_kmeans(self, X, Y):
        """
                                        Method Name: clustering_kmeans
                                        Description: cluster the same charastristics of data
                                        Output: A Dataframe which has the feature and there collinearity index.
                                        On Failure: Raise Exception

                                        Written By: Dinesh Naik
                                        Version: 1.0
                                        Revisions: None
                     """
        self.log.info('Entered the kmeans clustering method of the Preprocessor class')

        try:
            """ Applying the clustering approach"""

            kmeans=clustering.KMeansClustering(self.execType) # object initialization.
            number_of_clusters=kmeans.elbow_plot(X)  #  using the elbow plot to find the number of optimum clusters

            # Divide the data into clusters
            X=kmeans.create_clusters(X,number_of_clusters)

            #create a new column in the dataset consisting of the corresponding cluster assignments.
            X['Y']=Y

            # getting the unique clusters from our dataset
            list_of_clusters=X['Cluster'].unique()

            return X, list_of_clusters

        except Exception as e:
            self.log.info('Exception occured in clustering_kmeans method of the Preprocessor class. Exception message: ' + str(e))
            self.log.info('clustering_kmeans failed. Exited the standard_scale_data method of the Preprocessor class')
            raise Exception()

