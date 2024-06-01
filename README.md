# CodeSense: AI Search Engine for Codebases

We implemented a RAG pipeline which models a codebase and traverses it to feed into an LLM and generate responses to your questions

### Ask a question about a codebase:

![codesense_gif_demo1](https://github.com/TravHaran/CodeSense/assets/34573516/374aa452-eb9a-45db-8dd3-ece5ef72e253)

### Ask a question about multiple codebases:

![codesesens_gif_demo2](https://github.com/TravHaran/CodeSense/assets/34573516/c13b9327-4143-4e75-beec-545751f2d1fd)


Checkout Full Demo Here: [https://www.youtube.com/watch?v=4XfCgc7lMVs](https://www.youtube.com/watch?v=_bPMY-AagAM&ab_channel=TravisRatnaharan)

## Breakdown

### 1. CodeBase Tree Extraction
    - for a given codebase generate a k-ary tree outlining the directories, subdirectories, all the way down to the actual code files as the leaf nodes
### 2. Call Graph Extraction
    - for a source code file generate a directed graph representing the flow of execution calls for functions defined in the code file
### 3. Annotation Generation
    - for a function defined in code generate a text summarization
### 4. Annotation Aggregation
    - for a source-code file modeled as a call graph with annnotations at each node, output an aggregated report of all the annotations
### 5. Keyword Extraction
    - from the aggregated annotation report extract a list of keywords
    - from a usery query extract a list of keywords
### 6. Tree Traversal
    - given a list of target keywords traverse the code-base tree until you find the node with the most matching keywords
    - once the target node has been found, return it's corresponding aggregated annotation report
### 7. Question Answering
    - given the aggregated annoation report as context, provide an answer to the user's query.

## Installation & Setup
TODO
