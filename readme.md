<!-- markdownlint-configure-file {
  "MD013": {
    "code_blocks": false,
    "tables": false
  },
  "MD033": false,
  "MD041": false
} -->

# Server Manager Tool

![Downloads][downloads-badge]
![Downloads][python-badge]

This tool was develop to help my team to perform daily or manualy activities in
ours servers. The idea is to provide a tool that will make thinks easier,
such as:

- Start, stop, restart windows service (local and remote)
- Copy files and folders to remote servers
- Other features comming soon


## Getting Started

```bash
    manager --help
```

```bash
Usage: manager [OPTIONS] COMMAND [ARGS]...

  main cli function

Options:
  -v, --version                   Show the application's version and exit.
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.

Commands:
  file-manager
  windows-service
```


[downloads-badge]: https://img.shields.io/github/downloads/guibuenorodrigues/server-manager-tool/total?style=flat-square
[python-badge]: https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=yellow