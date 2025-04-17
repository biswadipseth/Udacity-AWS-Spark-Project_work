import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality
from awsglue.dynamicframe import DynamicFrame
from awsglue import DynamicFrame
from pyspark.sql import functions as SqlFuncs

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

# Script generated for node accelerometer_trusted_s3
accelerometer_trusted_s3_node1744819682858 = glueContext.create_dynamic_frame.from_options(format_options={"multiLine": "false"}, connection_type="s3", format="json", connection_options={"paths": ["s3://biswa-aws-spark-datalake/accelerometer/trusted/"], "recurse": True}, transformation_ctx="accelerometer_trusted_s3_node1744819682858")

# Script generated for node customer_trusted_s3
customer_trusted_s3_node1744819679151 = glueContext.create_dynamic_frame.from_options(format_options={"multiLine": "false"}, connection_type="s3", format="json", connection_options={"paths": ["s3://biswa-aws-spark-datalake/customer/trusted/"], "recurse": True}, transformation_ctx="customer_trusted_s3_node1744819679151")

# Script generated for node Renamed keys for Join
RenamedkeysforJoin_node1744820035203 = ApplyMapping.apply(frame=customer_trusted_s3_node1744819679151, mappings=[("customername", "string", "right_customername", "string"), ("email", "string", "right_email", "string"), ("phone", "string", "right_phone", "string"), ("serialnumber", "string", "right_serialnumber", "string"), ("registrationdate", "long", "right_registrationdate", "long"), ("lastupdatedate", "long", "right_lastupdatedate", "long"), ("sharewithresearchasofdate", "string", "right_sharewithresearchasofdate", "string"), ("sharewithpublicasofdate", "long", "right_sharewithpublicasofdate", "long")], transformation_ctx="RenamedkeysforJoin_node1744820035203")

# Script generated for node Join
Join_node1744819800263 = Join.apply(frame1=accelerometer_trusted_s3_node1744819682858, frame2=RenamedkeysforJoin_node1744820035203, keys1=["user"], keys2=["right_email"], transformation_ctx="Join_node1744819800263")

# Script generated for node Drop Fields
DropFields_node1744820870090 = DropFields.apply(frame=Join_node1744819800263, paths=["z", "right_email", "right_sharewithpublicasofdate", "right_sharewithresearchasofdate", "right_phone", "right_serialnumber", "user", "y", "right_registrationdate", "x", "timestamp", "right_customername", "right_lastupdatedate"], transformation_ctx="DropFields_node1744820870090")

# Script generated for node Drop Duplicates
DropDuplicates_node1744820001759 =  DynamicFrame.fromDF(DropFields_node1744820870090.toDF().dropDuplicates(), glueContext, "DropDuplicates_node1744820001759")

# Script generated for node Rearrange_Columns_Order
SqlQuery9435 = '''
SELECT 
    customername,
    email,
    phone,
    serialnumber,
    registrationdate,
    lastupdatedate,
    sharewithpublicasofdate,
    sharewithresearchasofdate
FROM  myDataSource

'''
Rearrange_Columns_Order_node1744821589431 = sparkSqlQuery(glueContext, query = SqlQuery9435, mapping = {"myDataSource":DropDuplicates_node1744820001759}, transformation_ctx = "Rearrange_Columns_Order_node1744821589431")

# Script generated for node Customer_Curated_S3
EvaluateDataQuality().process_rows(frame=Rearrange_Columns_Order_node1744821589431, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1744819588442", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
Customer_Curated_S3_node1744820158894 = glueContext.write_dynamic_frame.from_options(frame=Rearrange_Columns_Order_node1744821589431, connection_type="s3", format="json", connection_options={"path": "s3://biswa-aws-spark-datalake/customer/curated/", "partitionKeys": []}, transformation_ctx="Customer_Curated_S3_node1744820158894")

job.commit()