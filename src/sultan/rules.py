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


def discover_rules(cwd=None):

    if cwd == None:
        cwd = os.getcwd()

    discovered = []
    for root, dirs, files in os.walk(cwd):

        if ('Rulesfile' not in files) and ('Rulefile' not in files):
            continue

        # determine the path to the 
        abs_path = os.path.join(root, 'Rulesfile')
        if not os.path.exists(abs_path):
            abs_path = os.path.join(root, 'Rulefile')

        discovered.append(abs_path)
        with open(abs_path) as f:
            contents = f.read()
            exec(contents, globals())

    if len(discovered) > 0:
        return RULES
    else:
        click.secho("There are no 'Rulesfile' files. Please create a new 'Rulesfile'", fg='red')
        return {}

def run(name):

    if name in RULES:
        function = RULES[name]['function'] 
        results = function()
        if results:
            print_(results)
    else:
        click.secho("'%s' is not found in your Rulesfiles. Please check and try again." % name, fg='red')
        click.secho("Run 'rules show' to list all the rules that were found.", fg='red')