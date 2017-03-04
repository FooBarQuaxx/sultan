import click
import os
from six import print_
from functools import wraps

RULES = {}

class rule(object):

    def __init__(self, name=None, description=None, env=None):
        
        self.name = name
        self.description = description if description else "Not Provided"
        self.env = env.lower() if env else 'production'

    def __call__(self, function):

        # get the name of the function 
        if self.name == None:
            self.name = function.__name__

        # setup the rules
        RULES[self.name] = {
            'description': self.description,
            'env': self.env,
            'function': function
        }


def discover_rules():

    for root, dirs, files in os.walk(os.getcwd()):

        if 'Rulesfile' not in files:
            continue

        # determine the path to the 
        abs_path = os.path.join(root, 'Rulesfile')
        with open(abs_path) as f:
            contents = f.read()
            exec(contents, globals())
    return RULES

def run(name):

    if name in RULES:
        function = RULES[name]['function'] 
        results = function()
        if results:
            print_(results)
    else:
        click.secho("'%s' is not found in your Rulesfiles. Please check and try again." % name, fg='red')
        click.secho("Run 'rules show' to list all the rules that were found.", fg='red')