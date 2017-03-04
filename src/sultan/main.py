import click
from sultan.rules import (discover_rules, run)


@click.command()
@click.argument('command')
def rules(command):
    """
    Run 'rules help' to display help.
    """
    if command in ('list', 'show'):
        show_rules()
        return

    if command in ('help'):
        help()
        return
    
    # if nothing else is provided
    discover_rules()
    run(command)

def help():
    """
    Displays help.
    """
    click.echo("Rules are defined in 'Rulesfile' in the parent or any child directories of ")
    click.echo("the project.")
    click.echo("")
    click.echo("     list:    Lists the different rules that you defined.")
    click.echo("     show:    Lists the different rules that you defined. (Alias to 'list')")
    click.echo("<command>:    Runs the command you want to run.")
    click.echo("")

def show_rules():
    """
    Discovers all the 'Rulefiles' and the rules defined in them,
    and lists them out.
    """
    def row(line):
        click.secho('| ' + line.ljust(79) + '|', fg='magenta')

    rules = discover_rules()
    total = len(rules)
    count = 0
    if total > 0:
        click.secho('+' + '-'*80 + '+', fg='magenta')
    for name, attributes in rules.items():
        description = attributes.get('description')
        env = attributes.get('env')

        row('Name: %s' % name)
        row('Description: %s' % description)
        row('Env: %s' % env)
        count += 1
        if count <= total:
            click.secho('+' + '-'*80 + '+', fg='magenta')