# serializer

### Made for transfering data between brython and a python webserver.

1. An issue with JSON is it can't serialize python's datetime classes very well.  YAML doesn't play well with brython.

2. I needed a way to send `datetime.date` and `datetime.time` to the client. This serializer might not be the best thing
   for this but it does what it needed.
   
3. I also send quite a bit of data from the server that is exactly the same, this was written to assist in making the 
   transfer time smaller.
   
4. Any python structure, nested or not can be passed.

5. It does use json under the hood to faciliate the transfering of the data between server and client.

```python
from datetime import date
import serializer
serialized = serializer.dump(date.today())
# '{"&0": {"int": 2021}, "&1": {"int": 2}, "&2": {"int": 25}, "&3": {"tuple": ["&0", "&1", "&2"]}, "date": "&3"}'
serialized.loads(serialized)
# datetime.date(2021, 2, 25)
```

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
