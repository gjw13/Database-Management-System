# cosc280project
*Created in Python*

*Start of documentation*

# Database Management System
Greg Wills and David Wilke

Our system uses a similar grammar to SQL. Check it out [here](https://forcedotcom.github.io/phoenix/).

## How to run
> python main.py

### Files
* **main.py** - this is the driver of the system, handles storage
* **parser.py** - contains the majority of the parsing of the queries
* **eval.py** - contains the back end of the system, receives input from parser and makes appropriate executions
* **table.py** - contains the table class
* **database.py** - contains the database class
* **Storage/** - directory that contains the stored relations in separate files

## Query Input Manager
### Input
Our query input manager is a simple line editor when run from the command line interface. Queries
are entered through the CLI and received by the parser.

### Parser
Our top-down recursive parser iterates through a query to determine the necessary information
to pass to the evaluator/back end of our system.
* Assumption: Parenthesis and commas must not have spaces on both sides.

## Data Definition Language
### Implementation

#### Features
  1. Create table
  - Examples
    - > CREATE TABLE CUSTOMERS (first string, last string, position string, age int);
    - > CREATE TABLE EQUIPMENT (type string, purchase_date string, sell_date string);
  - **NOTE**: Every value contained in the relation is entered as a string, so the syntax above renders the type specification with no significance. As noted below, this does not effect the comparison of integers with binary comparison operators.
  2. Drop table
  - Examples
    - > DROP TABLE CUSTOMERS;
    - > DROP TABLE EQUIPMENT;
  - The drop table command will remove the specified relation from the database object. Similarly, it will remove the file from the storage directory named "Storage" which is detailed below.
  3. Create index
  * Single attribute index
  4. Drop index

## Data Manipulation Language

### Operators
  1. SELECT
  * Parse components
    * Assumption: If there is more than one table in the select statement, there will be aliases.
    * Assumption: The WHERE clause is the last thing in a query if it exists.
  * Validate table selection
  * Project attributes for all identified tables
  * Execute query
  2. INSERT
  * Assumption: only full tuples can be inserted into the relation.
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

## Estimated Grade
Our estimate of our grade on this project is a 92%. We feel this is an accurate grade given that almost all required functions of our database management system execute with efficiency and consistency. With few small assumptions and little to no deviation from SQL grammar, our system operates according to our detailed documentation and project specifications. Thank you.

**April 25th, 2019**
