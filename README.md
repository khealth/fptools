<div align="center">
    <img src="assets/logo.svg" height="140" alt="ftools logo">
</div>

<h1 align="center">ftools</h1>

Functional programming tools for Python inspired by Lodash FP and an extension
for Python standard functional libraries

```bash
pip install ftools
```

![Build Status](https://github.com/khealth/fptools/workflows/Python%20library/badge.svg)

### [Documentation](https://khealth.github.io/fptools/)

### Features

- Performant and lean
- Simple and pythonic
- Immutable

### Develop

```bash
poetry config settings.virtualenvs.in-project true;
poetry config settings.virtualenvs.path .venv;
poetry install;
```

#### Lint

```bash
poetry run pylint ftools;
```

#### Format

```bash
poetry run black .;
```

#### Test

```bash
poetry run pytest;
```

#### Publish new version

Contact @iddan
