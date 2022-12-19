# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.2]
### Added
- N/A

### Changed
- Add support for Python 3.11 and Django 4.1 [#226]
- Replace 'safety' package with 'pip-audit' [#230]
- Add docker support to locally test with Postgres [#233]

### Removed
- Add support for Python 3.6 and Django 2.2 and 3.1 [#226]

## [1.1.1]
### Added
- N/A

### Changed
- Remove requirements to have "psycopg2" installed for testing using sqlite [#194]
- Testing Support for Django4 and django-filter 2.3 and 2.4 [#206]
- Add tests and documentation for filter order [#211]

### Removed
- N/A

## [1.1.0]
### Added
- N/A

### Changed
- Limit the number of max sql parameters used for sqlite to 999 [#177]
- Fixed various Filters using user defined choices not working correctly with Boolean choices [#185]

### Removed
- N/A
