# Litchi

## Introduction

`Litchi` is yet another coding assistant powered by LLM.

Unlike other programming assistants, `litchi` supports global indexing across all source files in projects and code-based retrieval augmented generation. It makes features like chat-to-code and code-generation more effective and practical.

## Features

`Litchi` has more features than other coding assistants or copilot plugins because it is integrated with indexes which can be used as standalone tools.

* Support indexing source code files for the whole project.
* Manager any code index by creating, updating, showing, and searching.
* Retrieval augmented generation with source code for user's query.
* Addoc chat to code which will retrieval related source files to query LLM.
* Generate code based on user's query and related source files.
* One step to filter the source files which can be customed for different projects.
* Compatible with all large language models like ChatGPT and others.
* Compatible with public and private MaaS which can be deployed in local.

## Use Cases

* Normal chat: chat with LLM without indexes which is useful for general purposes.
* Chat with file: use LLM to read and understand a local file.
* Chat with files: collect file names in index file and chat with all files.
* Generate code for user's query:
  * Quickly generate python script like port detecting to execute.
* Generate code for user's query and source files:
  * Rewrite the source code in different programming languages.
  * Generate unit test cases for the source code.
* Run commands: generate the script and execute immediately
* Write requirements instead of coding: Edit local requirement file and automatically generating code
* Optimize code for user's query and source file:
  * Add annotation for original source code.
  * Format, refactor or optmize the source code with specified style.
  * Inplace or ask permission to update the source code with optimized code.
  * Implement the TODO functions in the source code.

  

## Install

Install the `litchi` command as a standard Python package.

```
git clone https://github.com/OrchardUniverse/litchi.git

cd ./litchi/

pip install .
```

## Usage

Initialize the project and generate directory `./.litchi/`. You can input the language as "Chinese" so that it will create index and query in Chinese.

```
litchi init $PROJECT_PATH

litchi init --language Chinese $PROJECT_PATH
```

Go to the project directory and create source file `./.litchi/source_files.yaml`. You can edit `./.litchi/ignore_rules.yaml` to choose the expected source files.

```
litchi source create
```

Create the index for single file or all source files in project.

```
litchi index create $FILE_PATH

litchi index create --all
```

Show the detail of the index of single file or all indexes.

```
litchi index show $FILE_PATH

litchi index show --all
```

You can input a query and get the related indexes.

```
litchi index query $QUERY
```

If you want to read the source code with index, use the following commands which will copy the readable index file next to the source file.

```
litchi index copy-to-source

litchi index delete-from-source
```

