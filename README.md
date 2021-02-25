# serializer

### Made for transfering data between brython and a python webserver.

> An issue with JSON is it can't serialize python's datetime classes very well.  YAML doesn't play well with brython.
>
> I needed a way to send `datetime.date` and `datetime.time` to the client. This serializer might not be the best thing
> for this but it does what it needed.
> 
> I also send quite a bit of data from the server that is exactly the same, this was written to assist in making the
> transfer time smaller.

```python
from datetime import date
import serializer
serialized = serializer.dump(date.today())
serialized.loads(serialized)
# datetime.date(2021, 2, 25)
```

> Any python structure, nested or not can be passed.

## Serializable python types 

| type | comment |
|---|---|
| bytes |
| str |
| int |
| float |
| dict |
| list |
| tuple |
| set |
| datetime |
| date |
| time |
| Decimal | Some values transfer poorly.
| None |
| True |
| False |
