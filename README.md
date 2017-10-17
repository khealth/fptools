# fptools

### Usage

```python
from fptools import Dictionary

_dict = { 'a': 1, 'b': 2 }
new_dict = Dictionary.map_values(lambda x: x * 2, _dict)
```

### Develop

```bash 
pipenv install --dev
```

### Test

```bash
pipenv run pytest
```
