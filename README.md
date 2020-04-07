# Linux env parser

Parse environment variables from a specific file.

## Examples

### Provide configuration

```
ipaddr=192.168.0.123
arch=aarch64-linux-gnu
aabbcc123
#aaa=bbb
#aaa=ccc
```

### Call envparser

```
import envparser

env = envparser("./demo", True)
```

Only 'ipaddr' and 'arch' will be recognized.

```
======== ENV ========
arch = aarch64-linux-gnu
ipaddr = 192.168.0.123
=====================
```

### Get 'hostname' via envparser

```
env.get('hostname') # prints "demo"
```

### Get 'aaa' with the default value 'bbb'

```
env.get('aaa', 'bbb') # prints "bbb"
```

### Replace 'hostname'

```
env.set('hostname', 'mine', True) # replace from "demo" to "mine"
```

### Delete 'hostname'

```
env.set('hostname')
```