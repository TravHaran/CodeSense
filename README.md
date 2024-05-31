# Project Codesense: a codebase search engine

Checkout Demo Here: https://www.youtube.com/watch?v=4XfCgc7lMVs

## Breakdown

### 1. CodeBase Tree Extraction
    - for a given codebase generate a k-ary tree outlining the directories, subdirectories, all the way down to the actual code files as the leaf nodes
### 2. Call Graph Extraction
    - for a source code file generate a directed graph representing the flow of execution calls for functions defined in the code file
### 3. Annotation Generation
    - for a fucntion defined in code generate a text summarization
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
