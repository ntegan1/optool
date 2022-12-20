

ROOT=$(CURDIR)
OPDIR=$(ROOT)/../../
TESTDIR=$(ROOT)/test/


all:

runserver:
	export PYTHONPATH=$(OPDIR)
	test -f /TICI && $(ROOT)/server.py
	test -f /TICI || poetry run $(ROOT)/server.py

test0:
	-@export PYTHONPATH=$(OPDIR); poetry run $(TESTDIR)/0clientinit.py


