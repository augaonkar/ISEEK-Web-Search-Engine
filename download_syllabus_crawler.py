import pycurl
from io import BytesIO
from xml.etree import cElementTree as ET

c = pycurl.Curl()
# Reading File Content.
f = open('syllabus-links.txt', "r")

output=f.readline()
filecounter=1

while output:
    buffer = BytesIO()
    output=output.strip()
    c.setopt(c.URL,output)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    body = buffer.getvalue()
    xmlstr = body.decode("iso-8859-1")
    root = ET.fromstring(xmlstr)
    #print(root)
    fileName = output.split("/")[-1].split('syl.xml')[0] + '.rtf'
    fp=open(fileName,"a")
    for course_name in list(root):
        # Taking Course NAme
        course = course_name.text
        fp.write(course)
        
    
    for weeks in list(root):
        topics=weeks.findall("week")
        for i in topics:
            topictext=i.find("topics")
            # Writing the content of the course 
            fp.writelines(topictext.text)
    
    fp.close()
    filecounter+=1
    output=f.readline()

c.close()
print("end")

