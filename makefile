# Makefile for development purposes only

DOCDIR = docs
FFFLASHDIR = ffflash
TESTDIR = tests
HTMLCOVDIR = htmlcov

PYTEST = py.test
WATCH = watchmedo shell-command --recursive --patterns="*.py;*.rst"


.rmdocs:
	$(MAKE) -C $(DOCDIR) clean
.docs:
	$(MAKE) -C $(DOCDIR) html


.rmcov:
	rm -rvf $(HTMLCOVDIR) .coverage
.cov:
	$(PYTEST) --cov-report=html --cov=$(FFFLASHDIR) $(TESTDIR)


all: .docs .cov
clean: .rmdocs .rmcov
	find . -name '__pycache__' -delete -print -o -name '*.pyc' -delete -print
call: clean all

loop: all
	$(WATCH) --command="$(MAKE) all"
cloop: call
	$(WATCH) --command="$(MAKE) call"


docs: .docs
cdocs: .rmdocs .docs
ldocs: docs
	$(WATCH) --command="$(MAKE) docs"
cldocs: cdocs
	$(WATCH) --command="$(MAKE) cdocs"

cov: .cov
ccov: .rmcov .cov
lcov: cov
	$(WATCH) --command="$(MAKE) cov"
clcov: ccov
	$(WATCH) --command="$(MAKE) ccov"

test:
	$(PYTEST) -vss $(TESTDIR) .
ltest: test
	$(WATCH) --command="$(MAKE) test"
