import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Default ruleset used by all target nodes with data quality enabled
DEFAULT_DATA_QUALITY_RULESET = """
    Rules = [
        ColumnCount > 0
    ]
"""

# Script generated for node Step_Trainer_Trusted_S3
Step_Trainer_Trusted_S3_node1744830484816 = glueContext.create_dynamic_frame.from_options(format_options={"multiLine": "false"}, connection_type="s3", format="json", connection_options={"paths": ["s3://biswa-aws-spark-datalake/step_trainer/trusted/"], "recurse": True}, transformation_ctx="Step_Trainer_Trusted_S3_node1744830484816")

# Script generated for node Accelerometer_Trusted_S3
Accelerometer_Trusted_S3_node1744830486578 = glueContext.create_dynamic_frame.from_options(format_options={"multiLine": "false"}, connection_type="s3", format="json", connection_options={"paths": ["s3://biswa-aws-spark-datalake/accelerometer/trusted/"], "recurse": True}, transformation_ctx="Accelerometer_Trusted_S3_node1744830486578")

# Script generated for node ML Join
MLJoin_node1744830620353 = Join.apply(frame1=Accelerometer_Trusted_S3_node1744830486578, frame2=Step_Trainer_Trusted_S3_node1744830484816, keys1=["timestamp"], keys2=["right_sensorreadingtime"], transformation_ctx="MLJoin_node1744830620353")

# Script generated for node Amazon S3
EvaluateDataQuality().process_rows(frame=MLJoin_node1744830620353, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1744830415462", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AmazonS3_node1744831008540 = glueContext.write_dynamic_frame.from_options(frame=MLJoin_node1744830620353, connection_type="s3", format="json", connection_options={"path": "s3://biswa-aws-spark-datalake/Machine_Learning/ML_Curated/", "partitionKeys": []}, transformation_ctx="AmazonS3_node1744831008540")

job.commit()