#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
将特定注释转换为指定格式，以便友好化访问
===========================================================================
@Author Bruce He <hebin@comteck.cn>
@Date  2018-05-29
@Version 0.1
"""
import os
import re
import argparse


class MDGenerator:
    """
    生成MD格式文档
    """
    def __init__(self, data=''):
        """
        传入待处理数据
        """
        pass

    def title(self, text, font_size=1):
        """
        返回标题
        :param text:
        :param font_size: 1-5 对应 1-5号标题
        :return:
        """
        if font_size not in (1,2,3,4,5,):
            raise AttributeError('字号大小不正确')
        return '#' * font_size + ' ' + text

    def bold(self, text):

        return '**%s**' % text

    def comment(self, text):
        return '> %s%s' % (text, os.linesep)

    def highline(self, text):
        return "`%s`" % text

    def code(self,text, code_type=''):

        return """```%s%s%s%s```""" % (code_type, os.linesep, text, os.linesep)

    def newline(self):
        return '---'

    def table(self, *args, **kwargs):
        """
        表格输出
        参数需要有tilte,alignment,data_list
        :return:
        """
        title = kwargs.get('title')
        alignment = kwargs.get('alignment')
        data = kwargs.get('data')

        if not isinstance(data, list) or not isinstance(title, list):
            raise TypeError('参数类型有误')
        if not data or not title:
            raise AttributeError('参数不正确')

        length = len(title)

        if not alignment:
            alignment = [':---'] * length
        # 字段长度要保持一致
        output = [' | '.join(title), ' | '.join(alignment)]
        for d in data:
            data_string = ' | '.join(d)
            if len(d) < length:
                # 要补足
                data_string += ' | ' * (length - len(d))

            output.append(data_string)

        return os.linesep.join(output)

    def output(self):
        """
        输出文档
        :param format:
        :return:
        """
        pass


class Doc:
    """
    文档类
    """

    def __init__(self, path):
        """
        初始化参数
        """
        self.md_generator = MDGenerator()
        self.root_path = path
        self.docs = []
        self.parsed_list = []
        _linesep = os.linesep
        self.path_pattern = re.compile("\*\s*?@path([\s\S]*?)"+_linesep)
        self.desc_pattern = re.compile("\*\s*?@desc([\s\S]*?)"+_linesep)
        self.author_pattern = re.compile("\*\s*?@author([\s\S]*?)"+_linesep)
        self.param_pattern = re.compile("\*\s*?@param([\s\S]*?)"+_linesep)
        self.method_pattern = re.compile("\*\s*?@method([\s\S]*?)"+_linesep)
        self.return_pattern = re.compile("\*\s*?@return([\s\S]*?)"+_linesep)
        self.return_block_pattern = re.compile("\*\s*?@return_block([\s\S]*?)@end_return_block")
        self.name_pattern = re.compile("\*\s*?@name([\s\S]*?)"+_linesep)

        self.walk()

        self.find()
    
    def walk(self):
        """
        爬文档
        :return: 
        """
        if not os.path.exists(self.root_path):
            raise AttributeError('路径不存在')
        
        if not os.path.isdir(self.root_path):
            raise AttributeError('必须是一个目录')
        
        for dirpath, dirname, filenames in os.walk(self.root_path):
            for filename in filenames:
                # 只读取php文件
                if filename[-4:].lower() == '.php':
                    self.docs.append(os.path.join(dirpath, filename))

    def get_parsed_list(self):
        return self.parsed_list

    def add_parsed_list(self, doc_name, data):
        """
        加入已转换的列表
        :param doc_name:
        :param data:
        :return:
        """
        self.parsed_list.append({
            'doc_name': doc_name,
            'data': data
        })

    def find(self):
        """
        寻找特征注释文档
        :return: 
        """
        if not self.docs:
            raise AttributeError('没有找到需要解析的文档')

        pattern = re.compile("\/\*\*\s*?\*\s*?@apidoc([\s\S]*?)\*\/")

        # 读取文件找到所有符合的注释
        for doc_name in self.docs:
            with open(doc_name) as f:
                try:
                    php_content = f.read()
                    results = pattern.findall(php_content)
                    if results:
                        self.add_parsed_list(doc_name, self.parse(doc_name, results))
                except UnicodeDecodeError:
                    print(doc_name, '编码有误，跳过...')
                except AttributeError as e:
                    print(doc_name, str(e))

    def parse(self, doc_name, results):
        """
        解析注释
        doc_name: 文件名
        results: 分析到的注释
        :return:
        """
        data = []
        for result in results:
            apipath, method = self.regular_path(result)
            data.append({
                'name': self.regular_name(result),
                'desc': self.regular_desc(result),
                'method': method,
                'author': self.regular_author(result),
                'apipath': apipath,
                'params': self.regular_param(result),
                'return': self.regular_return(result)
            })

        return data

    def regular_return(self, result):
        """
        合规化返回的数据
        :param result:
        :return:
        """
        # 先查找是否存在返回块
        return_block = self.return_block_pattern.findall(result)

        if not return_block:
            # 查找 return 行
            return_block = self.return_pattern.findall(result)

        if not return_block:
            return '默认返回'

        return_block_list = return_block[0].split(os.linesep)

        regular_return_block = []
        for block in return_block_list:
            _block = block.strip()
            if _block:
                # 找到* 去除之前的空格
                _star_pos = _block.find('*')
                if _star_pos >= 0:
                    _block = _block[_star_pos+1:]
                regular_return_block.append(_block)

        return os.linesep.join(regular_return_block)

    def regular_method(self, result):
        """
        合规化提交方式 默认POST
        :param result:
        :return:
        """
        methods = self.method_pattern.findall(result)
        if not methods:
            return 'POST'

        valid_methods = ['POST','GET','DELETE','PUT','PATCH',]
        # 只返回第一条
        method = methods[0].upper().strip()
        if method not in valid_methods:
            raise AttributeError('method参数有误，应该是如下之一：%s' % str(valid_methods))

        return method

    def regular_desc(self, result):
        """
        合规化描述 如无返回未定义
        :param result:
        :return:
        """
        descs = self.desc_pattern.findall(result)

        return descs and descs[0].strip() or '未定义'

    def regular_author(self, result):
        """
        合规化作者 如无返回未定义
        :param result:
        :return:
        """
        authors = self.author_pattern.findall(result)

        return authors and authors[0].strip() or '未定义'

    def regular_path(self, result):
        """
        合规化接口地址及提交方式
        :param result:
        :return:
        """
        paths = self.path_pattern.findall(result)
        if not paths:
            raise AttributeError('api地址未提供')
        
        path = paths[0].split()

        if len(path) == 1:
            return path[0], 'POST'

        valid_methods = ['POST', 'GET', 'DELETE', 'PUT', 'PATCH', ]
        # 只返回第一条
        method = path[1].upper().strip()
        if method not in valid_methods:
            raise AttributeError('method参数有误，应该是如下之一：%s' % str(valid_methods))

        return path[0], method

    def regular_param(self, result):
        """
        合规化参数
        ---
        类型 变量名 描述
        :param result:
        :return:
        """
        params = self.param_pattern.findall(result)
        data = []
        for param in params:
            data.append(param.split())

        return data

    def regular_name(self,result):
        """
        合规化名称
        :return:
        """
        name = self.name_pattern.findall(result)
        if not name:
            raise AttributeError('接口名称未定义')

        return name[0].strip()

    def output(self, dest, override=False, format='MD'):
        """
        输出 目前输出markdown
        :param override:
        :param format:
        :return:
        """

        if not override and os.path.isfile(dest):
            raise ValueError('文件已存在')

        parsed_list = self.parsed_list
        _output = list()

        for api_doc in parsed_list:
            # print(api_doc['doc_name'])
            for api_data in api_doc['data']:
                # 转为api md 文档
                _output.extend(self.format_api_doc(api_data))

        content = (os.linesep*2).join(_output)

        with open(dest,'+w') as f:
            f.write(content)

        return True

    def format_api_doc(self, api_data):
        """
        封装返回的api 格式
        :param data:
        :return:
        """

        generator = self.md_generator
        _output = list()

        # 接口名称
        _output.append(generator.title(api_data['name'], 2))
        # 接口描述
        _output.append(generator.comment(api_data['desc']))
        # _output.append(generator.newline())
        _output.append('%s %s' % (generator.bold('请求地址：'), api_data['apipath']))
        _output.append('%s %s' % (generator.bold('请求方式：'), api_data['method']))

        # 参数表
        _table_data = {
            'title': ['变量名', '类型', '描述'],
            'data': api_data['params'],
        }
        _output.append(generator.table(**_table_data))
        # 返回参数
        _output.append(generator.bold('返回参数：'))
        _output.append(generator.code(api_data['return']))
        _output.append(generator.newline())

        return _output


if __name__ == '__main__':

    description = """
        PHP自文档化助手 0.1
    """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('dest', nargs='?', default='', help="指定生成的文件地址 如：app/api.md")
    parser.add_argument('-p', '--path', default='./', help="指定扫描的代码目录，默认为当前目录")
    parser.add_argument('-f', '--force', action="store_true", help="是否覆盖存在的md文件")

    args = parser.parse_args()

    path = args.path
    dest = args.dest
    force = args.force

    if not dest:
        parser.print_help()
        exit()

    doc = Doc(path)
    if doc.output(dest, force):
        print(dest, '保存成功')