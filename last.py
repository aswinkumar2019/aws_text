import json
import boto3
client = boto3.client('textract')
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

#s3 = boto3.resource('s3')
#file_name = input('Enter file name,the file must be in /home/pi/Downloads directory  ')
#s3.meta.client.upload_file('/home/pi/Downloads/' + file_name, 'youcode', 'w1.jpeg')
#print(file_name)
#print('response:',response['Blocks'])
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
        self.entry.set_text("Enter file name,Please place the file in the Downloads section")
        vbox_first.pack_start(self.entry, False, True, 0)
        button = Gtk.Button.new_with_label("Start")
        button.connect("clicked", self.run)
        vbox_first.pack_start(button, False, True, 10)
        self.label1 = Gtk.Label("Output will be displayed here")
        vbox_last.pack_start(self.label1, False, True, 20)
        self.add(hbox_top)



    def hasNumbers(self,inputString):
       return any(char.isdigit() for char in inputString)
    def run(self,button):
      output = ''
      s3 = boto3.resource('s3')
      file_name = self.entry.get_text()
      s3.meta.client.upload_file('/home/pi/Downloads/' + file_name, 'checkyoucode', 'hello.jpeg')
      response = client.detect_document_text(
    Document={
        'S3Object': {
            'Bucket': 'checkyoucode',
            'Name': 'hello.jpeg'
        }
    }
)

      count = 0
      for item in response['Blocks']:
         if(count == 1):
            output = output + item['Text'] + ' \n\n'
            print(item['Text'])
            print('')
            count = 0
         if(item['BlockType'] == 'LINE'):
              if(item['Text'].lower().find('number')>=0):
                 if(self.hasNumbers(item['Text'])):
                    output = output + item['Text'] + ' \n\n'
                    print(item['Text'])
                    print('')
                 else:           
                    output = output + item['Text']
                    print(item['Text'])
                    count = 1
      self.label1.set_text(output)
window = LabelWindow()        
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()
