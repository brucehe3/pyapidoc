<?php

/**
 * @apidoc
 * @path  /api/aaa/bbb/ POST
 * @name api演示接口
 * @desc 用于说明如何注释的api接口
 * @author hebin <hebin@comteck.cn>
 * @param  code  string  代码
 * @param  name  string  姓名
 * @return {'code':'0','msg':'success','data':[]}
 */
 function api2()
 {
 }

 /**
 * @apidoc
 * @path  /api/aaa/ccc/ POST
 * @name api演示接口2
 * @desc 用于说明如何注释的api接口
 * @author hebin <hebin@comteck.cn>
 * @param  code  string  代码
 * @param  name  string  姓名
 * @return_block
 * msg: 返回消息 <string>
 * code: 返回编码 <string>
 * data: 返回值 <list>
 *     id: <integer>
 *     code: 编码 <string>
 *     created_at: 采购时间 <string>
 * @end_return_block
 */
 function api2()
 {
 }