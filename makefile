# Makefile for development purposes only

DOCDIR = docs
FFFLASHDIR = ffflash
TESTDIR = tests
HTMLCOVDIR = htmlcov

PYTEST = py.test
WATCH = watchmedo shell-command --recursive --patterns="*.py;*.rst" --command="$(MAKE) MKCMD"
BROWSE = python3 -c "import webbrowser; webbrowser.open_new_tab('URL')"

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
	$(subst MKCMD,all,$(WATCH))
cloop: call
	$(subst MKCMD,call,$(WATCH))


docs: .docs
cdocs: .rmdocs .docs
hdocs: docs
	$(subst URL,$(DOCDIR)/_build/html/index.html,$(BROWSE))
ldocs: docs
	$(subst MKCMD,docs,$(WATCH))
cldocs: cdocs
	$(subst MKCMD,cdocs,$(WATCH))

cov: .cov
ccov: .rmcov .cov
hcov: cov
	$(subst URL,$(HTMLCOVDIR)/index.html,$(BROWSE))
lcov: cov
	$(subst MKCMD,cov,$(WATCH))
clcov: ccov
	$(subst MKCMD,ccov,$(WATCH))

test:
	$(PYTEST) -vss $(TESTDIR) .
ltest: test
	$(subst MKCMD,test,$(WATCH))
