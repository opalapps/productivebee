import argparse
parser = argparse.ArgumentParser(
	description = 	"ProductiveBee v0.0.1 "
		"code snippets generator by OpalApps: www.opalapps.com")

parser.add_argument('command', type=str, nargs='?', 
	choices = ["class", "project", "unittest"],
	default = None, help="Command to be performed") 
parser.add_argument('-d', type=str, nargs='?', metavar = "targetDir",
	default = None, help="Target directory for generated files")
parser.add_argument('-l', type=str, nargs='?', metavar = "progLang",
	default = None, help = "Language the code should be generated in")
parser.add_argument('-n', type=str, nargs='?', metavar = "className",
	default = "GeneratedClass", 
	help = "a class and eventualy a file name to be generated")

import sys
sys.exit(1)

if not command:
	parser.print_help
	sys.exit(-1)	

settings = { 
	"-d" 				: "",
	"--usage-info" : False,
	"--class-files": "",
	"--makefile"	: "Makefile"
}

import sys

if targetDir:
	settings[ "-d" ] = sys.argv[ sys.argv.index("-d") + 1]

if "--usage-info" in sys.argv:
	settings[ "--usage-info" ] = True

if "--class-files" in sys.argv:
	settings[ "--class-files"] = sys.argv[ sys.argv.index("--class-files") + 1 ]

if "--makefile" in sys.argv:
	settings[ "--makefile"] = sys.argv[ sys.argv.index("--makefile") + 1 ]

if "--class-files" in sys.argv:
	settings[ "--class-files"] = sys.argv[ sys.argv.index("--class-files") +1 ]

testName = sys.argv[ len(sys.argv) - 1]

className = None
if settings.has_key("--class-files"): 
	className = settings["--class-files"]
	print "DBG: className=\"%s\"" % (className)

mainProgramTemplate = '''#include <iostream>

int main(int argc, char**argv) 
{
	std::cout << "Hello from %%TEST_NAME%%" << std::endl;
	
	return 0;	
}
'''

makefileTemplate = '''BINARY_NAME=%%TEST_NAME%%
SRC=%%TEST_NAME%%.cpp
CC=g++
IFLAGS=
CFLAGS=-o $(BINARY_NAME)
LIBS=

all:
	$(CC) $(CFLAGS) $(IFLAGS) $(LIBS) $(SRC)

'''

classHeaderFileTemplate = '''#ifndef %%CLASS_NAME_GUARD%%_HEADER_FILE
#define %%CLASS_NAME_GUARD%%_HEADR_FILE

class %%CLASS_NAME%% {
public:
	%%CLASS_NAME%%();
	~%%CLASS_NAME%%();
};

#endif /* %%CLASS_NAME_GUARD%%_HEADER_FILE */
'''

classSourceFileTemplate = '''#include "%%CLASS_NAME%%.h"

%%CLASS_NAME%%::%%CLASS_NAME%%()
{
}

%%CLASS_NAME%%::~%%CLASS_NAME%%()
{
}

'''

replacements = {
	"%%TEST_NAME%%": testName,
	"%%CLASS_NAME%%" : className,
	"%%CLASS_NAME_GUARD%%" : className.upper()
}

generatedMakefile = None
generatedMainProgram = None

for pattern in replacements:
	print "DBG: processing replacement pattern: \"%s\" ..." % (pattern) 

	generatedMainProgram = mainProgramTemplate.replace( pattern, 
		replacements[ pattern]
	)
	
	generatedMakefile = makefileTemplate.replace( pattern,
		replacements[ pattern]
	)

	classHeaderFileTemplate = classHeaderFileTemplate.replace( pattern,
		replacements[ pattern]
	)

	classSourceFileTemplate = classSourceFileTemplate.replace( pattern,
		replacements[ pattern]
	)

if not generatedMainProgram:
	print("ERROR: Can't generate MainProgram")
	sys.exit(-1)


if not generatedMakefile:
	print("ERROR: Can't generate Makefile")
	sys.exit(-1)

import os

# Create an output directory
if not os.path.exists( settings["-d"]):
	os.makedirs( settings["-d"], 0o777)
else:
	print("Warning! Directory exists: \"%s\"" % settings["-d"])
	sys.exit(-1)

if settings.has_key( "--class-files"):
	print "INFO: Generating class files for class: \"%s\" ..." % (className)
	fileClassHeader = open( "%s/%s" % ( settings["-d"], className+".h"), 'w' )
	fileClassHeader.write( classHeaderFileTemplate)
	fileClassHeader.close()

	fileClassSource = open( "%s/%s" % ( settings["-d"], className+".cpp"), 'w' )
	fileClassSource.write( classSourceFileTemplate)
	fileClassSource.close()

	sys.exit(1)

fileMainProgram = open( "%s/%s" % ( settings["-d"], testName+".cpp"), 'w')
fileMainProgram.write( generatedMainProgram)
fileMainProgram.close()

fileMakefile = open( "%s/%s" % (settings["-d"], "Makefile"), 'w')
fileMakefile.write( generatedMakefile)
fileMakefile.close()

