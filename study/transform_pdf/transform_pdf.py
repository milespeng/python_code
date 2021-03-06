#/usr/bin/python
from urllib.request import urlopen
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
from io import open

def readPDF(pdfFile):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)

    process_pdf(rsrcmgr, device, pdfFile)
    device.close()

    content = retstr.getvalue()
    retstr.close()
    return content

def read_local_PDF(filename):
    with open(filename,"r") as f:
        data=f.read()

    return data

#pdfFile = urlopen("http://pythonscraping.com/pages/warandpeace/chapter1.pdf")
pdfFile=read_local_PDF("/home/qa/miles/script/transform_pdf/python.pdf")
outputString = readPDF(pdfFile)
print(outputString)
pdfFile.close()