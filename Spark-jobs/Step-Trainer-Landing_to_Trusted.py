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

# Script generated for node Customer_Curated_s3
Customer_Curated_s3_node1744822147451 = glueContext.create_dynamic_frame.from_options(format_options={"multiLine": "false"}, connection_type="s3", format="json", connection_options={"paths": ["s3://biswa-aws-spark-datalake/customer/curated/"], "recurse": True}, transformation_ctx="Customer_Curated_s3_node1744822147451")

# Script generated for node Step_Trainer_Landing_S3
Step_Trainer_Landing_S3_node1744822145771 = glueContext.create_dynamic_frame.from_options(format_options={"multiLine": "false"}, connection_type="s3", format="json", connection_options={"paths": ["s3://biswa-aws-spark-datalake/step_trainer/landing/"], "recurse": True}, transformation_ctx="Step_Trainer_Landing_S3_node1744822145771")

# Script generated for node Renamed keys for Join
RenamedkeysforJoin_node1744822264092 = ApplyMapping.apply(frame=Step_Trainer_Landing_S3_node1744822145771, mappings=[("sensorreadingtime", "long", "right_sensorreadingtime", "long"), ("serialnumber", "string", "right_serialnumber", "string"), ("distancefromobject", "int", "right_distancefromobject", "int")], transformation_ctx="RenamedkeysforJoin_node1744822264092")

# Script generated for node Join
Join_node1744822253636 = Join.apply(frame1=Customer_Curated_s3_node1744822147451, frame2=RenamedkeysforJoin_node1744822264092, keys1=["serialnumber"], keys2=["right_serialnumber"], transformation_ctx="Join_node1744822253636")

# Script generated for node Step_Trainer_Trusted_s3
EvaluateDataQuality().process_rows(frame=Join_node1744822253636, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1744823061889", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
Step_Trainer_Trusted_s3_node1744825216330 = glueContext.write_dynamic_frame.from_options(frame=Join_node1744822253636, connection_type="s3", format="json", connection_options={"path": "s3://biswa-aws-spark-datalake/step_trainer/trusted/", "partitionKeys": []}, transformation_ctx="Step_Trainer_Trusted_s3_node1744825216330")

job.commit()
