# Makefile for development purposes only

DOCDIR = docs
FFFLASHDIR = ffflash
TESTDIR = tests
HTMLCOVDIR = htmlcov

PYTEST = py.test
WATCH = watchmedo shell-command --recursive --wait --patterns="*.py;*.rst" --command="$(MAKE) MKCMD"
BROWSE = python3 -c "import webbrowser; webbrowser.open_new_tab('URL')"

.rmdocs:
	$(MAKE) -C $(DOCDIR) clean
.docs:
	$(MAKE) -C $(DOCDIR) html

.rmcov:
	rm -rvf $(HTMLCOVDIR) .coverage
.cov:
	$(PYTEST) --cov-report=html --cov=$(FFFLASHDIR) $(TESTDIR)

.test:
	$(PYTEST) -vss $(TESTDIR)

all: .docs .cov
clean: .rmdocs .rmcov
	find . -name '__pycache__' -delete -print -o -name '*.pyc' -delete -print
new: clean all

loop: all
	$(subst MKCMD,all,$(WATCH))


test: .test
ltest: test
	$(subst MKCMD,test,$(WATCH))


docs: .docs
rmdocs: .rmdocs
newdocs: .rmdocs .docs
hdocs: .docs
	$(subst URL,$(DOCDIR)/_build/html/index.html,$(BROWSE))
ldocs: .docs
	$(subst MKCMD,docs,$(WATCH))


cov: .cov
rmcov: .rmcov
newcov: .rmcov .cov
hcov: .cov
	$(subst URL,$(HTMLCOVDIR)/index.html,$(BROWSE))
lcov: .cov
	$(subst MKCMD,cov,$(WATCH))

