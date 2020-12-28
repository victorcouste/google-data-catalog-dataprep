
from google.cloud import datacatalog
from config import datacatalog_client
import config

# -----------------------------------------------------------------------------------------------------------------
# -------------GET DATAPREP TAG METADATA AND PROFILE TAG TEMPLATE NAMES ------------------------------
# ---------------------------------------------------------------------------------------------------

def get_dataprep_tag_templates():

	scope = datacatalog.SearchCatalogRequest.Scope()
	scope.include_project_ids.append(config.dataprep_tag_template_project)

	tag_templates = datacatalog_client.search_catalog(scope=scope, query='type=tag_template name:'+config.dataprep_metadata_tag_template_id)

	for tag_template in tag_templates:
		dataprep_metadata_tag_template_name=tag_template.relative_resource_name

	#print('Dataprep Metadata tag template name : {}'.format(dataprep_metadata_tag_template_name))

	tag_templates = datacatalog_client.search_catalog(scope=scope, query='type=tag_template name:'+config.dataprep_profile_tag_template_id)

	for tag_template in tag_templates:
		dataprep_profile_tag_template_name=tag_template.relative_resource_name

	#print('Dataprep Profile tag template name : {}'.format(dataprep_profile_tag_template_name))

	dataprep_tag_templates_names={"metadata":dataprep_metadata_tag_template_name,"profile":dataprep_profile_tag_template_name}

	return (dataprep_tag_templates_names)

# -----------------------------------------------------------------------------------------------------------------
# ------------- GET TABLE ENTRY  -------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------

def get_table_entry_name(output_project,output_dataset,output_table):

	resource_name = '//bigquery.googleapis.com/projects/{}/datasets/{}/tables/{}'.format(output_project,output_dataset,output_table)
	table_entry = datacatalog_client.lookup_entry(request={"linked_resource": resource_name})

	#print('Output table entry name : {}'.format(table_entry.name))

	return (table_entry.name)

#------------------------------------------------------------------------------------------------------------
#----------- FUNCTION TO UPDATE OR CREATE TAG ON A COLUMN ---------------------------------------------------
#------------------------------------------------------------------------------------------------------------

def upsert_column_tag(column_name,column_profile,profile_nbtotal,table_entry_name,dataprep_profile_tag_template_name):

	tag = datacatalog.Tag()
	tag.column=column_name

	# -----------------------------------------------------------------------
	# ------------- CREATE TAG FOR THE 3 PROFILE TYPES  ----------------------

	for profile_type in ["INVALID","VALID","EMPTY"]:
		
		profile_field = datacatalog.TagField()
		profile_found = [profile['count'] for profile in column_profile if profile['key']==profile_type]
		
		if not profile_found:
			profile_field.double_value = 0
		else:
			profile_field.double_value = profile_found[0]
			profile_nbtotal[profile_type]=profile_nbtotal[profile_type]+profile_found[0]

		tag.fields[profile_type] = profile_field

	# -----------------------------------------------------------------------
	# ------------- SEARCH IF TAG EXISTS ON THE COLUMN ----------------------

	column_tag_notfound=True
	for entry_tag in datacatalog_client.list_tags(parent=table_entry_name):

		#print("Entry tag list: {}".format(entry_tag))

		if entry_tag.template==dataprep_profile_tag_template_name and entry_tag.column==column_name:

			# ------------- UPDATE A EXISTING TAG ON THE COLUMN ----------------------

			tag.name=entry_tag.name
			tag = datacatalog_client.update_tag(tag=tag)
			#print("Tag Update : {}".format(tag))
			column_tag_notfound=False

	if column_tag_notfound:

		# ------------- CREATE A NEW TAG ON THE COLUMN  ----------------------

		tag.template = dataprep_profile_tag_template_name
		tag=datacatalog_client.create_tag(parent=table_entry_name, tag=tag)
		#print("Tag Create : {}".format(tag))