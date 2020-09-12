from flask_cors import CORS
from gcloud import storage
from flask import Flask, request
from gov_lookup import lookup_company, lookup_officers
from oauth2client.service_account import ServiceAccountCredentials
from google.cloud import documentai_v1beta2 as documentai

client = storage.Client()
bucket = client.get_bucket('document-ai-test-0123')
bucket_uri = 'gs://document-ai-test-0123'
project_id = 'round-core-288409'

app = Flask(__name__)
CORS(app)

def parse_file(input_uri):
    client = documentai.DocumentUnderstandingServiceClient()
    gcs_source = documentai.types.GcsSource(uri=input_uri)

    input_config = documentai.types.InputConfig(gcs_source=gcs_source, mime_type='application/pdf')
    parent = 'projects/{}/locations/us'.format(project_id)
    request = documentai.types.ProcessDocumentRequest(
        parent=parent,
        input_config=input_config)
    document = client.process_document(request=request)

    print(document.entities)

    return [entity.mention_text for entity in document.entities]


@app.route('/document', methods = ['POST'])
def document():
    file = request.files['file']
    blob = bucket.blob(file.filename)
    blob.upload_from_string(file.read(), content_type=file.content_type)
    uri = "/".join([bucket_uri, file.filename])
    extracted = parse_file(uri)

    return { "data": extracted }

@app.route('/lookup', methods = ['GET'])
def lookup():
    company_number = request.args.get('company_number')
    company_number = str(company_number).rjust(8, '0')
    co_name, co_data = lookup_company(company_number)
    officers = lookup_officers(company_number)

    return { 
        "officers": officers, 
        "company_name": co_name, 
        "company_data": co_data}

if __name__ == "__main__":
    app.run(debug=True)
