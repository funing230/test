import lizard
import scale
import argparse
import os
import sys

# i=lizard.get_all_source_files("D:\\1110\\8db6c32",exclude_patterns=None,lans='java');
#
a=lizard.analyze_file.analyze_source_code("D:\\1110\\8db6c32\\8db6c32 HandledContributionItem.java")

# a=lizard.analyze("D:\\1110\\8db6c32",lans='java')

for func in a.function_list:
	print(func.name)



def printMetrics(srcFiles, pathName):
    totSlocFolder = 0
    numFiles = 0

    newPath = convertPath(pathName)

    lizard.analyze_file.processors.insert(0, lizard.CPreExtension)

    # Insert file metrics as well as metrics for file's functions
    for currFile in srcFiles:
        totSloc = 0
        totParams = 0
        totTokens = 0
        totComplexity = 0

        fileMetrics = lizard.analyze_file(currFile)
        numFuncs = len(fileMetrics.function_list)

        fileName = getNewFileName(newPath, fileMetrics.filename)

        for func in fileMetrics.function_list:
            fields = [func.name, func.length, func.nloc, fileName,
                      "", func.cyclomatic_complexity, "",
                      func.parameter_count, "", "", "", func.token_count,
                      "", func.start_line, func.end_line]
            scale.Write_Fields(map(lambda x: str(x), fields))
            totSloc += func.nloc
            totParams += func.parameter_count
            totTokens += func.token_count
            totComplexity += func.cyclomatic_complexity

        if numFuncs != 0:
            avgSloc = round((float(totSloc) / numFuncs), 2)
            avgParams = round((float(totParams) / numFuncs), 2)
            avgTokens = round((float(totTokens) / numFuncs), 2)
            avgComplexity = round((float(totComplexity) / numFuncs), 2)
            fields = [fileName, "", fileMetrics.nloc, "",
                      numFuncs, "", avgComplexity, "", avgSloc,
                      avgParams, "", "", avgTokens, "", ""]
        else:
            fields = [fileName, "", fileMetrics.nloc, "",
                      0, "", 0, "", 0, 0, "", "", 0, "", ""]
        scale.Write_Fields(map(lambda x: str(x), fields))

        totSlocFolder += fileMetrics.nloc
        numFiles += 1

    if numFiles != 0:
        fields = [newPath, "", totSlocFolder,
                  "", "", "", "", "", "", "", "",
                  float(totSlocFolder) / numFiles,
                  "", "", "", ""]
        scale.Write_Fields(map(lambda x: str(x), fields))