# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.7.0](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/releases/tag/v0.7.0) - 2026-05-01

<small>[Compare with v0.6.0](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/compare/v0.6.0...v0.6.0)</small>

### Added

- Add the command line command `pretiac objects delete-host`

## [v0.6.0](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/releases/tag/v0.6.0) - 2026-03-26

<small>[Compare with v0.5.0](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/compare/v0.5.0...v0.6.0)</small>

### Added

- Add support for Python 3.14

### Changed

- Drop support for Python 3.10 and 3.11

## [v0.5.0](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/releases/tag/v0.5.0) - 2026-02-18

<small>[Compare with v0.4.1](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/compare/v0.4.1...v0.5.0)</small>

### Added

- Add support for Python 3.13

### Changed

- Drop support for Python 3.9
- Use `uv` instead of `poetry`

### Fixed

- Add new fields `messages_received_per_type` and `seconds_processing_messages` to Endpoint

## [v0.4.1](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/releases/tag/v0.4.1) - 2024-09-09

<small>[Compare with v0.4.0](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/compare/v0.4.0...v0.4.1)</small>

### Fixed

- Fix client setup with config_file=False.

## [v0.4.0](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/releases/tag/v0.4.0) - 2024-09-09

<small>[Compare with v0.3.0](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/compare/v0.3.0...v0.4.0)</small>

### Added

- Add test.
- Add some docs.
- Add some object types.
- Add more tests.
- Add typing.
- Add links.

### Fixed

- Fix tests.
- Fix config.
- Fix Timeperiod.
- Fix templates.
- Fix checks executor.

### Removed

- Remove duplicate object type names.

## [v0.3.0](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/releases/tag/v0.3.0) - 2024-09-04

<small>[Compare with v0.2.0](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/compare/v0.2.0...v0.3.0)</small>

### Added

- Add docstrings.
- Add tags to the object types.
- Add support for display names in the checks.
- Add display_name for services.
- Add logging support.
- Add check_executor.
- Add tag support.
- Add status to the cli.
- Add docs.
- Add some object types.
- Add types from https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_js.
- Add some docstrings.

### Fixed

- Fix checks.
- Fix execution_end.
- Fix readthedoc links.

### Removed

- Remove logging and and __future__ imports.

## [v0.2.0](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/releases/tag/v0.2.0) - 2024-08-23

<small>[Compare with v0.1.0](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/compare/v0.1.0...v0.2.0)</small>

### Added

- Add some tests.
- Add first root export.
- Add all submodules to the docs.

### Fixed

- Fix readthedocs badge.

## [v0.1.0](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/releases/tag/v0.1.0) - 2024-08-21

<small>[Compare with first commit](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/compare/eea590d9d60d1a591184ed933f3b78b3b9be7757...v0.1.0)</small>

### Added

- Add read the docs config.
- Add some types.
- Add first test.
- Add boilerplate files.
- Add configs from https://github.com/Josef-Friedrich/icinga2apic-stubs.
- Add resources from https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_js/tree/main/resources.
- Add py.typed.
- Add more types.
- add *.pyi.
- Add type hints.
- add/update icinga 2 api actions to reflect new action options ([f20120c](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/commit/f20120c888075e4e53481d8cb17c19b91c559336) by Ricardo Bartels).
- Add install requirements to setup.py ([0a4a6e3](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/commit/0a4a6e38cd87052a726702b32cf471b17503dd34) by Tobias von der Krone).
- Add keywords to setup.py ([3981156](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/commit/39811567aaf62262219ee6d6ae3ecdb12469a7b1) by Tobias von der Krone).
- Add link to Icinga 2 API filter documentation ([73377e6](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/commit/73377e6a28b2ae9691899e48dcfa22a3a67dd3cd) by Tobias von der Krone).
- Add link to fmnisme's github page ([edf5610](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/commit/edf5610ab5f85ff828fdbb90f6d5cdb5ee94f799) by Tobias von der Krone).
- Add support for 'filter_vars' ([3c1ff65](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/commit/3c1ff651e03369911be5261c3233e8e90e24f66b) by Tobias von der Krone).
- Add docstring to __init__.py ([33f104b](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/commit/33f104bb294c0e1c50ef453cdb9e5b33af5efce9) by Tobias von der Krone).
- Add documentation in markdown format ([ee6bdff](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/commit/ee6bdfff5e683a093474ab32d3247ad37362e1fe) by Tobias von der Krone).
- Add client usage with certificate and key to README ([41b46d5](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/commit/41b46d59cb0e7b04082a1458c334cced029b9d11) by Tobias von der Krone).
- Add more parameter checking ([7717349](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/commit/77173498f09278bbb75a4d608184bd68c4aaefd8) by Tobias von der Krone).
- Add objects.get() function ([5c11c7b](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/commit/5c11c7baa3b34795b3646d2a50d5a10c2ae5904a) by Tobias von der Krone).
- Add me to the setup.py file ([e28be16](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/commit/e28be1637493d424e4b3da09d7dfed9fc635313b) by Tobias von der Krone).
- Add possibility to get config from a file ([407ebf2](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/commit/407ebf29464fee98a19a74dab3688896abb841e8) by Tobias von der Krone).
- Add docstring to _request function ([bb49062](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/commit/bb49062505005dd3d274372b75749e4c59dffd06) by Tobias von der Krone).
- Add example for specifying "all_joins" for objects.list ([2aebc1e](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/commit/2aebc1e46b6c8d6307ad1fa4b6eba043b4640b5a) by Tobias von der Krone).
- Add all icinga 2 object types to objects.list function ([bec9b48](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/commit/bec9b48df55b675b8fe3b4333b5640c39dace9bf) by Tobias von der Krone).
- Add attribute "joins" to list function ([617c356](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/commit/617c3568596cc419f4f820647369ee4d70872ccc) by Tobias von der Krone).
- Add docstring to list function and use Icinga 2 object type names ([321088d](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/commit/321088d9b6b756766e1f1fcf99bcf732a359d267) by Tobias von der Krone).
- Add version attribute to Client and use it in HTTP header ([1c58e61](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/commit/1c58e616c41864dd5c7534f8a29d2ed29885772d) by Tobias von der Krone).
- Add possibility to show only specific attributes ([640a2ae](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/commit/640a2aee2e65f4aac0efec7e69a1d38c2ff97739) by Tobias von der Krone).
- Add docstrings to classes ([9858195](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/commit/985819506fe7ce3c72eecf2d31d085084577321c) by Tobias von der Krone).
- add example for Actions.restart_process ([536b527](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/commit/536b5278f1490cc69e5d634f4bf2ca51c03d8ceb) by fmnisme).

### Fixed

- Fix version mismatch between setup.py and setup.conf.
- fix(encoding): remove umlaut from name ([d964e1d](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/commit/d964e1d978e4c8d137edd501f4aa19040d10cb8e) by Christian Jonak).
- fix(actions): allow to remove comments based on filter ([a74120f](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/commit/a74120f9da026bf20383d644fdc88dc15b16b309) by Christian Jonak).
- Fixed 2 examples to use the correct function ([ea609a9](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/commit/ea609a9a0285c003d7f36122c051a9b8a7fe1634) by Matthew Garrett).
- Fix log message formatting ([875a867](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/commit/875a867350ad013b05520b2974996d4b3020592e) by Tobias von der Krone).
- Fix objects.get() ([207155a](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/commit/207155ac886387755b2d98907d975099766907fa) by Tobias von der Krone).
- Fix pylint: Final newline missing ([4480dba](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/commit/4480dba20a675fbcd22729b1931a612318d5fabc) by Tobias von der Krone).
- Fix objects.get() and objects.list() ([47dcc3b](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/commit/47dcc3bd8a1d691b5683cdd1dc5f298e2c4fa283) by Tobias von der Krone).
- Fix flake8: E501 line too long (83 > 79 characters) ([abd37f1](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/commit/abd37f1e7cf37b27c636969763b3ba8fdde1b516) by Tobias von der Krone).
- Fix flake8: E713 test for membership should be 'not in' ([87843ea](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/commit/87843eadd91bfefc409494aa76b45db8205c7f43) by Tobias von der Krone).
- Fix flake8: E265 block comment should start with '# ' ([da20c8b](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/commit/da20c8b82d1c30b78be91703619008a8177e8a0c) by Tobias von der Krone).
- Fix initialisation without configuration file ([700af72](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/commit/700af72e8802393a29a0bc42ef0add72ea3dbde6) by Tobias von der Krone).
- Fix typo in schedule_downtime examples ([d65a93f](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/commit/d65a93fbcda086d8f2d553f147f86e27be7055c1) by Tobias von der Krone).
- Fix typos ([31696fc](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/commit/31696fc2c8a779ff3e4b3bb020805a996837ab19) by Tobias von der Krone).
- Fix missing dot ([6487b65](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/commit/6487b6534da0737698b7da14bacd18ed0b6c3dfd) by Tobias von der Krone).

### Changed

- Change package name to "icinga2api" ([3a184e8](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/commit/3a184e8948d051e3a519737c0d422c7433514c08) by Tobias von der Krone).
- Change example to add a host in the README ([26fd358](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/commit/26fd358f19ba41c81081c419035259a97a19dd8d) by Tobias von der Krone).

### Removed

- Remove py.typed.
- Remove preceding / from path_prefix ([ba08fc6](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/commit/ba08fc6d2be320bb85b5f1d33eb59c0af1dec6a2) by David Gillies).
- Remove debugging print function calls ([56b70b8](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/commit/56b70b89eef94e177e2bc8fa7a4fb546fc3bfdf8) by Tobias von der Krone).
- Remove default values for parameters in _request function ([070a778](https://github.com/Josef-Friedrich/PREtty-Typed-Icinga2-Api-Client_py/commit/070a7785978a855b231df7c2776bfe4678efa7f3) by Tobias von der Krone).
