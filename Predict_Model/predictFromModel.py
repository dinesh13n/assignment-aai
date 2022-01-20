import pandas
from file_operations import file_methods
#from data_preprocessing import preprocessing
#from data_ingestion import data_loader_prediction
from application_logging import logger
#from Prediction_Raw_Data_Validation.predictionDataValidation import Prediction_Data_validation
from application_logging.logger import AppLog


class prediction:

    def __init__(self,execType='Prediction'):
        self.execType = execType
        self.applog = AppLog(self.execType)
        self.log = self.applog.log("sLogger")

    def predictionFromModel(self, data, datacol, VIF_Rem_Col):

        try:

            self.log.info('Start of Prediction')
            status=0
            prediction_data = data.copy()
            #self.log.info('Start of Prediction---{}'.format(data.drop(VIF_Rem_Col,axis=1).head(5)))
            file_loader=file_methods.File_Operation(self.log)
            kmeans=file_loader.load_model('KMeans')
            datacol.append('Prediction')


            clusters=kmeans.predict(data.drop(columns=VIF_Rem_Col,axis=1))
            data['clusters']=clusters
            #prediction_data['clusters']=clusters
            clusters=data['clusters'].unique()
            header = True # First time header would be true, while creating csv result file
            for i in clusters:
                cluster_data = data[data['clusters']==i]
                prediction_data = cluster_data
                cluster_data = cluster_data.drop(['clusters'],axis=1)
                #self.log.info('cluster_data---\n{}'.format(cluster_data.shape))

                cluster_data=cluster_data.drop(columns=VIF_Rem_Col,axis=1)
                model_name = file_loader.find_correct_model_file(i)
                model = file_loader.load_model(model_name)
                result=model.predict(cluster_data)
                #self.log.info('prediction_data---\n{}'.format(prediction_data.shape))
                #self.log.info('Prediction Results---\n{}'.format(len(result)))

                #result = pandas.DataFrame(zip(prediction_data,result),columns=datacol)
                prediction_data['Prediction']=result
                path="Prediction_Output_File/Predictions.csv"
                if header :
                    prediction_data.to_csv("Prediction_Output_File/Predictions.csv",header=header,mode='a+') #appends result to prediction file
                    header = False
                else:
                    prediction_data.to_csv("Prediction_Output_File/Predictions.csv",header=header,mode='a+') #appends result to prediction file
            status=1
            self.log.info('End of Prediction')
        except Exception as ex:
            self.log.info('Error occured while running the prediction!! Error:: %s' % ex)
            status=0
            raise ex
        return status




