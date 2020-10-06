import requests


def ssh_import_id(*, github=None, launchpad=None):
    "Returns a list of SSH keys imported from GitHub or Launchpad"
    if github is not None:
        url = 'https://github.com/{}.keys'.format(github)
        sep = '\n'
    elif launchpad is not None:
        url = 'https://launchpad.net/~{}/+sshkeys'.format(launchpad)
        sep = '\r\n\n'
    else:
        raise HostedPiException('github or launchpad ID must be provided')

    r = requests.get(url)
    if not r.ok:
        raise HostedPiException(
            'Error resolving {}, status code {}'.format(url, r.status_code)
        )
    return r.text.strip().split(sep)

def read_ssh_key(ssh_key_path):
    "Read the SSH key from the given path and return the file contents"
    with open(ssh_key_path) as f:
        return f.read()
