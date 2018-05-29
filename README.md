pyapidoc
===================

自文档化工具，将注释转为markdown文档

Author: Bruce He <hebin@comteck.cn>

Version: `0.1`

Requirements
-------------
* Python(2.7,3.4,3.5,3.6)

Installation
------------
将 `pyapidoc.py` 直接下载到相应代码目录下

Documentation
-------------

### 使用方式
```
usage: pyapidoc.py [-h] [-p PATH] [-f] [dest]
positional arguments:
  dest                  指定生成的文件地址 如：app/api.md

optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  指定扫描的代码目录，默认为当期目录
  -f, --force           是否覆盖存在的md文件

```


将当前目录下所有PHP文档中 符合注释规范的内容转为api.md文档
```
python pyapidoc.py api.md

```


将指定目录`app`下所有PHP文档中 符合注释规范的内容转为api.md文档
```
python pyapidoc.py -p app/ api.md

```



### 可用的注释变量

**@apidoc** 
起始符，所有需要转换的注释都以开始

**@name** 
接口名称

**@author**
接口开发者名称

**@param**
变量，可以多条，一条代表一个变量 变量名、变量类型、变量说明间用空格分割

**@return**
单行返回符，可以多条，多条效果同@return_block

**@return_block**
返回块的起始符，与@end_return_block 配对使用 目前仅保持块内格式的直接输出

**@end_return_block**
返回块的结束符

### 注释举例一
```javascript
    /**
     * @apidoc
     * @name [接口名称]
     * @desc [接口描述]
     * @author [开发者]
     * @param  [变量名1] [变量类型] [变量说明]
     * @param  [变量名2] [变量类型] [变量说明]
     * @return_block
     * code 代码 <string>
     * msg 返回消息 <string>
     *     data <array>
     *         ....
     * @end_return_block
     */
    function api_test(...)
    ...

```

### 注释举例二
```javascript
    /**
     * @apidoc
     * @name [接口名称]
     * @desc [接口描述]
     * @author [开发者]
     * @param  [变量名1] [变量类型] [变量说明]
     * @param  [变量名2] [变量类型] [变量说明]
     * @return {'code':'0','msg':'success',data:[....]}
     */
    function api_test(...)
    ...

```

#### 输出的内容

见 [demo.md][demo]

[demo]: https://github.com/brucehe3/pyapidoc/blob/master/demo.md