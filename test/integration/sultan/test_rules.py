import os
import shutil
import tempfile
import unittest

from sultan.rules import (discover_rules, run)

class RulesTestcase(unittest.TestCase):

    def setUp(self):

        self.test_dir = tempfile.mkdtemp()
        print self.test_dir
        with open(os.path.join(self.test_dir, 'Rulesfile'), 'w') as f:
            content = """
from sultan.rules import rule

@rule
def hello_world():
    print "Hello World"
            """
            f.write(content)

    def test_discovery(self):

        rules = discover_rules(cwd=self.test_dir)
        self.assertEqual(len(rules), 1)

    def tearDown(self):

        # if os.path.exists(self.test_dir):
        #     shutil.rmtree(self.test_dir)
        pass