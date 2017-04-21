# RedisDesktopManager Native Value Formatters

![91f4b202-89a4-11e5-8446-b34f21ee9152](https://cloud.githubusercontent.com/assets/1655867/20011127/315cb0c4-a2b3-11e6-8479-ae8a6d030f40.png)

**Advantages:**
- Plugin can be developed by any software engineer (Java/C++/C#/Python/PHP/Node.js etc)
- Plugin can be easily debugged

## How to implement native value formatter
1. Create directory with meaningful name. Name of the directory will be used as formatter name.
2. Implement script or executable which meets API described below. 
3. Add file `usage.json` with usage shell command<br />
For example for python script it will be: `['python', 'my_super_formatter.py']`
4. Test your formatter in RDM!

## API
### Version:

IN: `<executable> --version`

OUT (plain text):

```
1.0.0
```
### Decode binary data:  

IN: `<executable> decode <binary-data-encoded-with-base64>`

OUT (json): 

```
{
    “output”: “<decoded data for human-friendly edit>”,
    “read-only”: “false”,    
    “format”: “plain_text” // or “json”
}
```
### Encode string-representation 
**Required only for formatters which return `“read-only”: false` in `decode` method**

IN: `<executable> encode <edited-string-representation-encoded-with-base64>`

OUT (json): 
```
{
    “output”: “<binary-data-encoded-with-base64>”,    
}

```

### Error handling:
If formatter cannot decode/encode value error response should be returned:
OUT (json): 
```
{
    “error”: “Invalid CBOR data”,    
}
```

