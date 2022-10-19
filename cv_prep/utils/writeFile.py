# Write rttm and uem files
def writeFile(content, outputName):
    f = open(outputName, "w")
    f.write(content)
    f.close()