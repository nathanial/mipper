from __future__ import with_statement
import parser
from mipper.mips import Program, ProgramFactory
from unittest import TestSuite, TestLoader, TestResult, TestCase, TextTestRunner
from gnrl_tests import TestGeneralOperations
from bool_tests import TestBoolOperations
from math_tests import TestMathOperations
from pseudo_tests import TestPseudoOperations
from integration_tests import IntegrationTests

runner = TextTestRunner()

def run_suite(suite):
    result = TestResult()
    runner.run(suite)

def run_tests(klass):
    tests = TestLoader().loadTestsFromTestCase(klass)
    run_suite(tests)

def perform_test():
    run_tests(TestMathOperations)
    run_tests(TestBoolOperations)
    run_tests(TestPseudoOperations)
    run_tests(TestGeneralOperations)
    run_tests(IntegrationTests)

if __name__ == '__main__':
    perform_test()

