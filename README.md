# RedisDesktopManager Native value formatters

![91f4b202-89a4-11e5-8446-b34f21ee9152](https://cloud.githubusercontent.com/assets/1655867/20011127/315cb0c4-a2b3-11e6-8479-ae8a6d030f40.png)


**Advantages:**
- Plugin can be developed by any software engineer (Java/C++/C#/Python/PHP/Node.js etc)
- Plugin can be easily debugged

**API**
- Get info:

IN: `<executable> info`

OUT (json):

```
{
    “name”: “CBOR formatter”,
    “version”: “0.0.1”,
    “supported_values”: [“plain”, “binary”],
}
```
- Decode binary data:  

IN: `<executable> decode <binary-data>`

OUT (json): 

```
[{
    “output”: “<decoded data for human-friendly edit>”,
    “read-only”: “false”,
    “format”: “plain_text” // or “json”
}]
```
-  Validate

IN: `<executable> is_valid <binary-data>`

OUT (json): 

```
[{
    “valid”: “false”,
    “message”: “Invalid CBOR”
}]
```
- Encode string-representation (will be ignored if ‘decode’ output returns “read-only”: true)

IN: `<executable> encode <edited-string-representation>`

OUT (binary): 
df
```
<binary-data>
```
## 
