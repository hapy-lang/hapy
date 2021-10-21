# Change Log
All notable changes to this project will be documented in this file. Hopefully

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [0.2.0] - 2021-10-20

### Added
- Package `VERSION.txt` now included in a central place
- Well, this CHANGELOG is new :)

### Changed
- `hapy exec` command is now `hapy do`
- The default command is now `hapy repl`. Meaning, that running `hapy` alone activates the REPL

### Fixed
- smelling error because of clashing names when running the previous `hapy eval`
- Removed dict and list from list of keywords
