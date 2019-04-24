# cosc280project
*Created in Python*

*Possible Grammar: https://www.jooq.org/doc/latest/manual/sql-building/sql-parser/sql-parser-grammar/*

TO DO LIST (4/19)
  1. Finish eval_delete() - if time allows
  2. ~~Incorporate table class into existing evaluator and parser (mostly done)~~
  3. ~~Look into incorporating < and >~~
  4. Get indexes to work --> basically check the values of the indexed col first
      1. eval_select
      3. eval_delete
      4. eval_update  
  5. Relational schema
      1. ~~Create a way to keep track of tables (list of tables)~~
      2. Parser accounts for aliases
      3. ~~Write a join algorithm (probably merge-scan) but could be nested~~
  6. Adapt eval_update
  7. Check for duplicates/referential integrity (insert, update, delete)

Parser TODO:
  1. Tokenize the input
  2. Validate that it's in a valid form / each token is valid
  3. Semantical analysis - https://sqldep.com/sql-parser/

*Start of documentation*

# Database Management System

## How to run

### Files

## Query Input Manager

### Input

### Parser

## Data Definition Language

### Implementation

#### Features
  1. Create table
  2. Drop table
  3. Create index
    ⋅⋅* Single attribute index
  4. Drop index

## Data Manipulation Language

### Operators
  1. SELECT
    1. Parse components
    2. Validate table selection
    3. Project attributes for all identified tables
    4. Execute query
  2. INSERT
  3. UPDATE
  4. DELETE

### Considerations
  1. Duplicates
  2. Referential Integrity

## Main Memory Execution

  1. Attribute value distributions
  * Conjunctive and disjunctive selections
  * Determination of inner vs. outer join
  2. Efficient sorting

## Storage Structures



*User starts the project, which opens up a prompt for entering queries*
