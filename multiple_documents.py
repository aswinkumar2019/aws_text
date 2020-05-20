import boto3
import time
from trp import Document
from os import listdir
from os.path import isfile, join
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class LabelWindow(Gtk.Window):

 def __init__(self):
        Gtk.Window.__init__(self, title="Youcode Intelligence Solutions")
        vbox_first = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox_first.set_homogeneous(False)
        vbox_last = Gtk.Box(spacing=10)
        vbox_last.set_homogeneous(False)
        hbox_top = Gtk.Box(spacing=10)
        hbox_top.set_homogeneous(False)
        hbox_top.pack_start(vbox_first, False, True, 10)
        hbox_top.pack_start(vbox_last, False, True, 10)
        self.entry = Gtk.Entry()
        self.entry.set_text("Enter the location where the files are placed")
        vbox_first.pack_start(self.entry, False, True, 0)
        button = Gtk.Button.new_with_label("Start")
        button.connect("clicked", self.run)
        vbox_first.pack_start(button, False, True, 10)
        self.label1 = Gtk.Label("Status indicator")
        vbox_last.pack_start(self.label1, False, True, 20)
        self.add(hbox_top)


 def startJob(self,s3BucketName, objectName):
    response = None
    client = boto3.client('textract')
    response = client.start_document_analysis(
         DocumentLocation={
         'S3Object': {
            'Bucket': 'checkyoucode',
            'Name': self.file_name
        }
    },
    FeatureTypes=["TABLES"])

    return response["JobId"]

 def isJobComplete(self,jobId):
    time.sleep(5)
    client = boto3.client('textract')
    response = client.get_document_analysis(JobId=jobId)
    status = response["JobStatus"]
    print("Job status: {}".format(status))

    while(status == "IN_PROGRESS"):
        time.sleep(5)
        response = client.get_document_analysis(JobId=jobId)
        status = response["JobStatus"]
        print("Job status: {}".format(status))

    return status

 def getJobResults(self,jobId):

    pages = []

    time.sleep(5)

    client = boto3.client('textract')
    response = client.get_document_analysis(JobId=jobId)
    
    pages.append(response)
    print("Resultset page recieved: {}".format(len(pages)))
    nextToken = None
    if('NextToken' in response):
        nextToken = response['NextToken']

    while(nextToken):
        time.sleep(5)

        response = client.get_document_analysis(JobId=jobId, NextToken=nextToken)

        pages.append(response)
        print("Resultset page recieved: {}".format(len(pages)))
        nextToken = None
        if('NextToken' in response):
            nextToken = response['NextToken']

    return pages

# Document
 def run(self,button): 
    self.progress = ''
    s3BucketName = "checkyoucode"
    self.file_name = ''
    count = 0
    id_number = 0
    jobId = []
    s3 = boto3.resource('s3')
    location = self.entry.get_text()
    onlyfiles = [f for f in listdir(location) if isfile(join(location, f))]
    for self.file_name in onlyfiles:
         count = count + 1
         s3.meta.client.upload_file(join(location,self.file_name), 'checkyoucode', self.file_name)
         print('File number',count,'uploaded')
         print(self.file_name)
    print(onlyfiles)

    for self.file_name in onlyfiles:
         jobId.append(self.startJob(s3BucketName, self.file_name))
#print("Started job with id: {}".format(jobId))
    document_counts = 1
    for self.progress in jobId:
        print('Document count',document_counts,'with Id:',self.progress)
        if(self.isJobComplete(self.progress)):
          response = self.getJobResults(self.progress)
          doc = Document(response)
          table_value = []
          for page in doc.pages:
     # Print tables
             for table in page.tables: 
                table_value.append('next_page')
                for r, row in enumerate(table.rows):
                    table_value.append('next_row')
                    for c, cell in enumerate(row.cells):
                       table_value.append(cell.text)
             print(table_value)
        document_counts = document_counts + 1
    self.label1.set_text('Data has been pushed into the database') 
                   #  print("Table[{}][{}] = {}".format(r, c, cell.text))
window = LabelWindow()        
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()
