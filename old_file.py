
# for code analysis
import lizard
import pandas as pd
import numpy as np
# for directory / file traversing
import os
from os import makedirs
from os.path import isfile, join, splitext, basename, exists
from os import walk
import math


TreesToAnalyze = [
    "..\..\Modules", # modules root
    "..\..\src", # app layer
    # "D:\\1110",
    "D:\\test\\research\\SourceFile"

]

ExtensionsToAnalyze = [
    ".java",
    # ".h"
]

ResultDir = "./Reports/"
SummaryReport = "__SummaryByFile.csv"
CommitSummaryReport = "__CommitSummaryByFile.csv"


Result_List = []
LogFile = None

def AnalyzeFile(filename):
    # takes a path to a file and analyzes it.  We currently only analyze *.h and *.c files, so this will check that
    # and do nothing if the extension doesn't match
    file_name, file_extension = splitext(filename)

    if( file_extension in ExtensionsToAnalyze ):
        i = lizard.analyze_file(filename)
        Result_List.append(i.function_list)
        print(filename + " has been analyzed")

def AnalyzeDirectory(dir,commitNo):
    # takes a directory path to analyze and looks at each *.c file inside
    # recursively calls itself anytime it finds a directory inside.
    print( dir + " is being analyzed")
    for root, dirs, files in walk(dir, topdown=True):
        for fname in files:
            if(fname.__contains__(commitNo)):
                AnalyzeFile( join(root, fname) )
        #for dname in dirs:
        #    AnalyzeDirectory( join(root, dname) )

#
# def DumpModuleReport( func_list ):
#     f = None
#     idx = 0
#     for func in func_list:
#         #increment function index, this may already be in the dictionary too...
#         idx += 1
#
#         if f is None:
#             # get name for log and open it if it doesn't exist yet (None)
#             full_fname = func.filename
#             logname = basename(full_fname)
#             logname += ".csv"
#             f = open(ResultDir + logname, "w")
#             f.write("Function Number, Cyclomatic complexity, Lines of code\n")
#
#         #write the data
#         f.write(str(idx) + "," +
#                 str(func.cyclomatic_complexity) + "," +
#                 str(func.nloc) +
#                 "\n")
#
#     if f is not None:
#         f.close()

def DumpResultsToCSV( list ):
    # this is a list of lizard function_list objects
    # function list has many fields, examples:
    #   cyclomatic_complexity
    #   token_count
    #   name (without arguments)
    #   parameter_count
    #   nloc
    #   long_name (prototype)
    #   start_line

    # we want a few things from our CSV files:
    #   module_name.c, total complexity, total nloc
    #
    #
    f = open(ResultDir + SummaryReport, "w")
    f.write( "Filename, Number of Functions, total cyclomatic complexity, total lines of code,token_count,parameters\n" )

    commit_complexity = 0
    commit_total_nloc = 0
    commit_num_funcs = 0
    commit_token_count = 0
    commit_parameters = 0

    for module_func_list in list:

        if len(module_func_list) > 0:
            # calc total complexity and nloc
            total_complexity = 0
            total_nloc = 0
            num_funcs = 0
            token_count=0
            parameters=0

            for func in module_func_list:
                full_fname = func.filename
                total_complexity += func.cyclomatic_complexity
                total_nloc += func.nloc

                token_count+=func.token_count
                parameters+=len(func.parameters)

                num_funcs += 1

            # only report the filename without extension
            fname = basename(full_fname)

            # output the data and move on to the next module.
            f.write(fname + "," + str(num_funcs) + "," + str(total_complexity) + "," + str(total_nloc) + "," + str(token_count) + "," + str(parameters) + "\n")

    f.close()

    # next, we also want to create defailts for each module
    #   let's assume we will use modulename_report.csv
    # for module_func_list in list:
    #     DumpModuleReport( module_func_list )

def DumpCommitResultsToCSV(commit, list ):
    # this is a list of lizard function_list objects
    # function list has many fields, examples:
    #   cyclomatic_complexity
    #   token_count
    #   name (without arguments)
    #   parameter_count
    #   nloc
    #   long_name (prototype)
    #   start_line

    # we want a few things from our CSV files:
    #   module_name.c, total complexity, total nloc
    #
    #


    f = open(ResultDir + CommitSummaryReport, "a+")
    # f.write( "Bug_id, Commit Number of Functions, Commit total cyclomatic complexity, Commit total lines of code,Commit token_count,Commit parameters\n" )
    if os.path.getsize(ResultDir + CommitSummaryReport):
        print()
    else:
        f.write( "Bug_id, Commit Number of Functions, Commit total cyclomatic complexity, Commit total lines of code,Commit token_count,Commit parameters\n" )

    commit_complexity = 0
    commit_total_nloc = 0
    commit_num_funcs = 0
    commit_token_count = 0
    commit_parameters = 0

    for module_func_list in list:

        if len(module_func_list) > 0:
            # calc total complexity and nloc
            total_complexity = 0
            total_nloc = 0
            num_funcs = 0
            token_count=0
            parameters=0

            for func in module_func_list:
                full_fname = str(commit)
                total_complexity += func.cyclomatic_complexity
                total_nloc += func.nloc

                token_count+=func.token_count
                parameters+=len(func.parameters)
                num_funcs += 1

        commit_complexity += total_complexity
        commit_total_nloc += total_nloc
        commit_num_funcs += num_funcs
        commit_token_count += token_count
        commit_parameters += parameters
        commit_length=len(list)

    # only report the filename without extension
    fname = basename(full_fname)

    # output the data and move on to the next module.    str(math.ceil(/commit_length))
    f.write(fname + "," + str(commit_num_funcs/commit_length) + "," + str(str(commit_complexity/commit_length) ) + "," + str(str(commit_total_nloc/commit_length) ) + "," + str(str(commit_token_count/commit_length) ) + "," + str(str(commit_parameters/commit_length)) + "\n")

    f.close()

def main():
    # main function called in script

    projectname = 'Eclipse_Platform_UI'
    Eclipse_Platform_UI = pd.read_excel('dataset/' + projectname + '.xlsx', engine='openpyxl')
    Eclipse_Platform_UI.rename(columns={'Unnamed: 10': 'result'}, inplace=True)

    # get bugid and commit
    df_id_commit = Eclipse_Platform_UI.iloc[:, [1, 7]]
    # df_id_commit.drop(df_id_commit.index[0])

    listCommit = df_id_commit['commit'].tolist()
    # create report directory if it does not exist
    if not exists(ResultDir):
        makedirs(ResultDir)

    # for dir in TreesToAnalyze:

    for row in df_id_commit.itertuples() :  #iterrows()
        # str=row['commit']
        # str=getattr(row, 'commit')
        # str1=getattr(row, 'bug_id')
        AnalyzeDirectory("D:\\test\\research\\SourceFile",getattr(row,'commit'))
        DumpCommitResultsToCSV(getattr(row,'bug_id'),Result_List)

if __name__ == '__main__':
    main()