SRC_FILE = '/home/axlireza/Projects/ENIGMA/Reservatron/classdiagram.drawio'
DEST_FILE = '/home/axlireza/Projects/ENIGMA/Reservatron/classes.ts'
DEST_XML_FILE = '/home/axlireza/Projects/ENIGMA/Reservatron/classes.xml'

# %%
import xml.etree.ElementTree as ET

def convert():
    print("convert")
    # 1. Read the Draw.io file
    with open(SRC_FILE, "r") as file:
        drawio_data = file.read()

    # 2. Extract the XML data
    start_tag = "<diagram"
    end_tag = "</diagram>"
    start_index = drawio_data.find(start_tag)
    end_index = drawio_data.find(end_tag) + len(end_tag)
    xml_data = drawio_data[start_index:end_index]
    # print(xml_data)
    with open(DEST_XML_FILE, "w") as file: file.writelines(xml_data)
    
    # 3. Process the XML data
    root = ET.fromstring(xml_data)

    class_definitions = []
    firstclasscaptured = False
    inclass = False
    intype = False
    firstitemoftype = True
    with open(DEST_FILE, "w") as file:
        
        for mx_cell in root.findall(".//mxCell"):
            vertex = mx_cell.get("vertex", '')
            edge = mx_cell.get("edge", '')
            value = mx_cell.get("value", '')

            if value.find("dtype") >= 0:
                if inclass == True: file.writelines("}\n")
                inclass = False
                intype = True
                firstclasscaptured = False
                file.writelines("\ntype "+value.replace("dtype ", "")+" = ")
                firstitemoftype = True
            elif value.find("class") >= 0:
                if intype == True: file.writelines("\n")
                inclass = True
                intype = False
                if firstclasscaptured == True: file.writelines("}\n")
                else: firstclasscaptured = True
                file.writelines(value+" {\n")
            elif intype == True:
                file.writelines("\""+value+"\"") if firstitemoftype else file.writelines(" | \""+value+"\"")
                firstitemoftype = False
            elif inclass == True and value.find("+") >= 0:
                for line in value.replace("+", "public").replace("#", "private").split("\n"):
                    if len(line) > 0: file.writelines("\t"+line+";\n")
        if firstclasscaptured == True: file.writelines("}")



# %%
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Define the function to be executed when a change occurs
def on_file_change():
    print("File changed!")

# Define the event handler class
class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # Call the function when a modification event occurs
        convert()

# Create an observer and attach the event handler
observer = Observer()
observer.schedule(FileChangeHandler(), path=SRC_FILE, recursive=False)

# Start the observer
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    # Stop the observer if interrupted
    observer.stop()

# Wait until the observer thread completes its execution
observer.join()



