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

# Script generated for node Accelerometer_Landing_S3
Accelerometer_Landing_S3_node1744778607567 = glueContext.create_dynamic_frame.from_options(format_options={"multiLine": "false"}, connection_type="s3", format="json", connection_options={"paths": ["s3://biswa-aws-spark-datalake/accelerometer/landing/"], "recurse": True}, transformation_ctx="Accelerometer_Landing_S3_node1744778607567")

# Script generated for node Customer_Trusted_S3
Customer_Trusted_S3_node1744778607794 = glueContext.create_dynamic_frame.from_options(format_options={"multiLine": "false"}, connection_type="s3", format="json", connection_options={"paths": ["s3://biswa-aws-spark-datalake/customer/trusted/"], "recurse": True}, transformation_ctx="Customer_Trusted_S3_node1744778607794")

# Script generated for node Join
Join_node1744778914439 = Join.apply(frame1=Customer_Trusted_S3_node1744778607794, frame2=Accelerometer_Landing_S3_node1744778607567, keys1=["email"], keys2=["user"], transformation_ctx="Join_node1744778914439")

# Script generated for node Accelerometer_Trusted_S3
EvaluateDataQuality().process_rows(frame=Join_node1744778914439, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1744778536434", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
Accelerometer_Trusted_S3_node1744779556560 = glueContext.write_dynamic_frame.from_options(frame=Join_node1744778914439, connection_type="s3", format="json", connection_options={"path": "s3://biswa-aws-spark-datalake/accelerometer/trusted/", "partitionKeys": []}, transformation_ctx="Accelerometer_Trusted_S3_node1744779556560")

job.commit()