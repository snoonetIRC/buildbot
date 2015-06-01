# buildbot
## An advanced build & deploy system for *nix systems.

BuildBot is a Python-based build and deploy system using package manifests called "snippets", which define the parameters for a piece of software to interact with BuildBot.

For more help, ``use ./botty.py -h``

#### Deploying a package

To deploy all default packages to all the servers in servers.json (or custom config as specified with ``-c``), simply run 
```
./botty.py
```

To deploy to specific servers within your default set, simply specify the names of each server (it will be matched automatically)

```
./botty.py server1 server2 anotherexample backupserver
```

To deploy to an specific set of ssh servers and a custom package (such as when they're not in the config or as part of a script) use ``-p`` and ``-s``

```
./botty.py -p inspircd-source.json example@127.0.0.1 example2@raw.example.com
```
