PYTHON ?= python
top_srcdir := `pwd`
PYTHONPATH ?= $(top_srcdir)
SUBDIRS = \
	$(top_srcdir)/doc \
	$(top_srcdir)/test \
    $(top_srcdir)/test/util \
	$(top_srcdir)/examples

all: clean build

dist: clean docs
	@echo "Creating dist..."
	@$(PYTHON) setup.py sdist --format gztar
	@$(PYTHON) setup.py sdist --format zip

bdist: clean docs
	@echo "Creating bdist..."
	@$(PYTHON) setup.py bdist

build:
	@echo "Running build"
	@$(PYTHON) setup.py build
	@echo "Build finished, invoke 'make install' to install."


install:
	@echo "Installing..."
	@$(PYTHON) setup.py install

clean:
	@echo "Cleaning up in $(top_srcdir)/ ..."
	@rm -f *.cache *.core *~ MANIFEST *.pyc *.orig
	@rm -rf __pycache__
	@rm -rf build dist doc/html

	@for dir in $(SUBDIRS); do \
		if test -f $$dir/Makefile; then \
			make -C $$dir clean; \
		else \
			cd $$dir; \
			echo "Cleaning up in $$dir..."; \
			rm -f *~ *.cache *.core *.pyc *.orig *py.class; \
			rm -rf __pycache__; \
		fi \
	done

docs:
	@echo "Creating docs package"
	@rm -rf doc/html
	@cd doc && make html
	@mv doc/_build/html doc/html
	@rm -rf doc/_build
	@cd doc && make clean

release: dist
runtest:
	@PYTHONPATH=$(PYTHONPATH) $(PYTHON) -B -m test.util.runtests

# Do not run these in production environments! They are for testing
# purposes only!

buildall: clean
	@python2.7 setup.py build
	@python3.1 setup.py build
	@python3.2 setup.py build
	@python3.3 setup.py build
	@pypy1.9 setup.py build


installall:
	@python2.7 setup.py install
	@python3.1 setup.py install
	@python3.2 setup.py install
	@python3.3 setup.py install
	@pypy1.9 setup.py install

testall:
	@-PYTHONPATH=$(PYTHONPATH) python2.7 -B -m test.util.runtests
	@-PYTHONPATH=$(PYTHONPATH) python3.1 -B -m test.util.runtests
	@-PYTHONPATH=$(PYTHONPATH) python3.2 -B -m test.util.runtests
	@-PYTHONPATH=$(PYTHONPATH) python3.3 -B -m test.util.runtests
	@-PYTHONPATH=$(PYTHONPATH) pypy1.9 -B -m test.util.runtests

purge_installs:
	rm -rf /usr/local/lib/python2.7/site-packages/openal*
	rm -rf /usr/local/lib/python3.1/site-packages/openal*
	rm -rf /usr/local/lib/python3.2/site-packages/openal*
	rm -rf /usr/local/lib/python3.3/site-packages/openal*
	rm -rf /usr/local/lib/pypy-1.9/site-packages/openal*
