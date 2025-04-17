import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality
from awsglue import DynamicFrame

def sparkSqlQuery(glueContext, query, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)
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

# Script generated for node source_s3
source_s3_node1744773747045 = glueContext.create_dynamic_frame.from_options(format_options={"multiLine": "false"}, connection_type="s3", format="json", connection_options={"paths": ["s3://biswa-aws-spark-datalake/customer/landing/"], "recurse": True}, transformation_ctx="source_s3_node1744773747045")

# Script generated for node transformation_filtering
SqlQuery9842 = '''
select customername,
  email,
  phone,
  birthday,
  serialnumber,
  registrationdate,
  lastupdatedate,
  FROM_UNIXTIME(sharewithresearchasofdate / 1000e0) as sharewithresearchasofdate,
  sharewithpublicasofdate from myDataSource
  where sharewithresearchasofdate >0 or sharewithresearchasofdate!=null
'''
transformation_filtering_node1744773956318 = sparkSqlQuery(glueContext, query = SqlQuery9842, mapping = {"myDataSource":source_s3_node1744773747045}, transformation_ctx = "transformation_filtering_node1744773956318")

# Script generated for node target_s3
EvaluateDataQuality().process_rows(frame=transformation_filtering_node1744773956318, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1744773376992", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
target_s3_node1744774013628 = glueContext.write_dynamic_frame.from_options(frame=transformation_filtering_node1744773956318, connection_type="s3", format="json", connection_options={"path": "s3://biswa-aws-spark-datalake/customer/trusted/", "partitionKeys": []}, transformation_ctx="target_s3_node1744774013628")

job.commit()