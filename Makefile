MODULE = $(notdir $(CURDIR))

CWD    = $(CURDIR)

VSCODE = .vscode/settings.json .vscode/tasks.json .vscode/extensions.json

P = config.py 
S = $(MODULE).py test_$(MODULE).py

FILES  = README.md Makefile .gitignore apt.txt 
FILES += $(VSCODE)
FILES += $(S) requirements.txt
files:
	touch $(FILES) $(P)

DIRS = .vscode doc bin tmp
dirs:
	mkdir -p $(DIRS)

install: dirs files

MERGE += $(FILES)
MERGE += $(DIRS)
