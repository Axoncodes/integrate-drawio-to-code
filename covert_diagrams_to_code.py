# %%
import xml.etree.ElementTree as ET

def convert():
    print("convert")
    # 1. Read the Draw.io file
    file_path = "classdiagram.drawio"
    with open(file_path, "r") as file:
        drawio_data = file.read()

    # 2. Extract the XML data
    start_tag = "<diagram"
    end_tag = "</diagram>"
    start_index = drawio_data.find(start_tag)
    end_index = drawio_data.find(end_tag) + len(end_tag)
    xml_data = drawio_data[start_index:end_index]
    # print(xml_data)
    
    # 3. Process the XML data
    root = ET.fromstring(xml_data)

    class_definitions = []
    firstclasscaptured = False
    with open("classes.ts", "w") as file:
        
        for mx_cell in root.findall(".//mxCell"):
            vertex = mx_cell.get("vertex", '')
            edge = mx_cell.get("edge", '')
            value = mx_cell.get("value", '')

            # Process vertices (classes)
            if value.find("class") >= 0:
                if firstclasscaptured == True: file.writelines("}\n")
                file.writelines(value+" {\n")
                firstclasscaptured = True
            if value.find("+") >= 0:
                for line in value.split("\n"):
                    file.writelines("\t"+line.replace("+", "public")+";\n")
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

# Define the path to the file you want to monitor
file_path = 'classdiagram.drawio'

# Create an observer and attach the event handler
observer = Observer()
observer.schedule(FileChangeHandler(), path=file_path, recursive=False)

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



