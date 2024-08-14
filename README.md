# litchi

The AI coding assistant powered by LLM.

* 使用大模型理解源码含义和生成源代码。
* 为源码文件生成索引，支持语义搜索和检索增强查询。
* 自动过滤非源码文件和识别编程语言，批量自动化处理项目文件。


## Features

* [x] 语义搜索和检索增强查询
* [x] 自动过滤非源码文件和识别编程语言
* [x] 批量自动化处理项目文件
* [x] 使用大模型理解源码含义和生成源代码
* [x] 为源码文件生成索引
* [ ] 支持 Chat to Code
* [ ] 支持基于需求文本的代码生成

## Install

```
pip install .
```

## Usage

初始化项目，生成 `./litchi/` 目录和源码文件等。

```
litchi init $PROJECT_PATH

litchi init --language Chinese $PROJECT_PATH
```

遍历源码文件，更新 `./litchi/source_files.yaml` 文件。

```
litchi source update
```

创建索引，用户可以针对指定文件或整个项目源码创建索引。

```
litchi index create $FILE_PATH

litchi index create --all
```

查看索引，用户可以查看指定文件或所有索引信息。

```
litchi index show $FILE_PATH

litchi index show --all
```

更新索引，用户可以更新指定文件或所有索引信息。

```
litchi index update $FILE_PATH

litchi index update --all
```

查询相关索引，用户可以基于查询语句来提取相关索引信息。

```
litchi index search $QUERY
```

生成代码，用户可以基于需求文本生成代码。

```
litchi code generate $QUERY

litchi code generate $QUERY --diff

litchi code generate $QUERY --without-index
```

监听文件变化，用户可以监听文件变化并自动生成代码。

```
litchi code watch $REQUIREMENT_FILE


自动生成脚本文件并执行。

```
litchi code execute $QUERY
```








## Index

```
sqlite3 ./.litchi/source_file_index.db
```

```
select * from indexes;
```

## Size

```
sqlite3 ./.litchi/source_file_index.db
```



## Tokens

```
sqlite3 ./.litchi/source_file_index.db
```

```
select sum(tokens) from indexes;
```