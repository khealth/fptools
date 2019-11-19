<div align="center">
    <img src="assets/fptools.svg" height="140" alt="fptools logo">
</div>

<h1 align="center">fptools</h1>

Functional programming tools for Python inspired by Lodash FP and an extension
for Python standard functional libraries

```bash
poetry add --git git+https://github.com/kang-health/fptools.git#egg=fptools
```

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

### Test

```bash
poetry run pytest;
```
