# will be used to install all dependencies, run tests, and remove from __pychache__ the bytecode
#, add the venv, pylint,


# using the venv python, not the computer version. If you want to use the computer python version,
# change the value to 'python'
PYTHON=venv/bin/python3

# TESTS
PY_VERBOSE_FLAG=-v
TEST_DIR=tests/unittests
TESTS:=$(wildcard $(TEST_DIR)/test_*.py)
#$(PYTHON) $(PY_MODULE_FLAG) $(TEST_SUITE) $(PY_VERBOSE_FLAG) $(test_cript)\

run_tests: $(TESTS)
	@echo "\n======================================================\n"
	@echo "STARTING THE RDP ALGORITHM PROJECT'S TEST_SUITE."
	@echo "\n======================================================\n"
	$(PYTHON) -m unittest $^
