# toolaudit

[![Build Status](https://travis-ci.org/jstutters/toolaudit.svg?branch=master)](https://travis-ci.org/jstutters/toolaudit)

Report on the tools used in your software pipeline.

## Purpose

`toolaudit` provides a way of monitoring a collection of software programs for
version changes and is also able test functionality.  It written to assist with
the auditing of software pipelines in neuroscience research.

## Usage

`toolaudit` uses [YAML](http://yaml.org/) to describe software collections.  A
simple example of one of these descriptions is:

```YAML
---
tools:
  - name: cat
    path: /bin/cat
    reader:
      name: command_line
      option: --version
      regex: "^cat\\s\\(GNU\\scoreutils\\)\\s([0-9\\.]*)$"
    test:
      name: stdout
      command: "{exe} {file1} {file2}"
      inputs:
        file1: foo.txt
        file2: bar.txt
```

A simple invocation of toolaudit is:
```bash
$ toolaudit example.yaml
```

For the above example this would return:

```YAML
---
tools:
- checksum: 9c3bb3efa8095f36aafd9bf3a698efe439505021
  name: cat
  output_checksum: 533fbb1dc1a426ecf19af2f8e4f01c59491e6f8f
  path: /bin/cat
  reader: {name: command_line, option: --version, regex: '^cat\s\(GNU\scoreutils\)\s([0-9\.]*)$'}
  tester:
    command: '{exe} {file1} {file2}'
    inputs: {file1: foo.txt, file2: bar.txt}
    name: stdout
  version: '8.4'
```

The checksum is a SHA1 hash of the file identified at *path*.  The output
checksum is a SHA1 hash of the what was printed to stdout.

## Documentation

Full documentation is at: [toolaudit.readthedocs.org](https://toolaudit.readthedocs.org/).


## Release History

0.0.3 - Added support for Python 3
0.0.2 - Initial public release


## License

`toolaudit` is licensed under [The MIT License](http://opensource.org/licenses/MIT).
