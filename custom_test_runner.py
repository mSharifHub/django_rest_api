import unittest
from django.test.runner import DiscoverRunner


class CustomTestResult(unittest.TextTestResult):
    def addSuccess(self, test):
        super().addSuccess(test)
        self.stream.write(f"Test Pass {self.getDescription(test)}\n")
        self.stream.flush()

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.stream.write(f"Test Fail {self.getDescription(test)}\n")
        self.stream.flush()

    def addError(self, test, err):
        super().addError(test, err)
        self.stream.write(f"Test Error {self.getDescription(test)}\n")
        self.stream.flush()


class CustomTestRunner(DiscoverRunner):
    def get_resultclass(self):
        return CustomTestResult


if __name__ == '__main__':
    unittest.main(testRunner=CustomTestRunner())
