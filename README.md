# Database Management System
## Intro to Databases - COSC 280
### Greg Wills and David Wilke

The system uses a similar grammar to SQL. Check it out [here](https://forcedotcom.github.io/phoenix/). Python was chosen for a few reasons, the main one being its ability to parse strings with ease. Building the parser proved to be a difficult first step in our system, but was made easier by python’s ability to parse the queries entered by the user on the front end. The system functions in a similar fashion to SQL on the user interface side. The back end was fully developed separate from SQL.

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
  Our query input manager is a simple line editor when run from the command line interface. Queries are entered through the CLI and received by the parser. Upon arrival in the parser, each word in the query is converted to lowercase. This becomes important because each value in the relation will be all lower case. Key words can be either upper or lowercase.

### Parser
  Our top-down recursive parser iterates through a query to determine the necessary information to pass to the evaluator/back end of our system.
* Assumption: Parenthesis and commas must not have spaces on both sides.

## Data Definition Language
### Implementation

#### Features
  1. CREATE TABLE
  - Syntax
    - > CREATE TABLE <relation\> (<col\> <col_type>, <col\> <col_type>,...,<col\> <col_type>)
  - Examples
    - > CREATE TABLE CUSTOMERS (first string, last string, position string, age int);
    - > CREATE TABLE EQUIPMENT (type string, purchase_date string, sell_date string);
  - **NOTE**: Every value contained in the relation is entered as a string, so the syntax above renders the type specification with no significance. As noted below, this does not effect the comparison of integers with binary comparison operators.
  2. DROP TABLE
  - The drop table command will remove the specified relation from the database object. Similarly, it will remove the file from the storage directory named *Storage* whose functionality is detailed below.
  - Syntax
    - > DROP TABLE <relation\>;
  - Examples
    - > DROP TABLE CUSTOMERS;
    - > DROP TABLE EQUIPMENT;
  3. CREATE INDEX
  - The create index command will create the specified index on a table object if the object exists in the database object. It is stored as part of the table object.
  - Syntax
    - > CREATE INDEX <indexName\> on <relation\> (<col\>);
  - Examples
    - > CREATE INDEX index_name on CUSTOMERS (age);
    - > CREATE INDEX index_name on CUSTOMERS (first, last);
  4. DROP INDEX
  - The drop index command will remove the specified index from the specified table object if the table exists and if the index exists.
  - Syntax
    - > DROP INDEX <indexName\> on <relation\>;
  - Examples
    - > DROP INDEX index_name on CUSTOMERS;

## Data Manipulation Language
### Operators
  1. SELECT
  - The system will parse the components of the query, validate the table selection, project attributes for all identified tables, then execute the query based on the conditions. If multiple relations are given, it will join two relations to make complete the query.
  - Syntax
    - > SELECT <cols\> FROM <relation\> WHERE <conditions\>
  - **Assumption**: If there is more than one table in the select statement, there will be aliases.
  - **Assumption**: The WHERE clause is the last thing in a query if it exists.
  - Example of table validation
  ```
  if database.tableExists(table_name):
    table_obj = database.getRelation(table_name)
  ```
  - Examples
    - > SELECT * FROM customers WHERE first = john OR last = smith
  2. INSERT
  - The system will add a tuple to the relation given the tuple stated in the update statement. It will resize the relation by adding a row and updating the table object.
  - Syntax
    - > INSERT INTO <relation\> VALUES (<val\>,<val\>,...,<val\>)
  - Examples
    - > INSERT INTO CUSTOMERS VALUES (20, Ophir, Frieder, 29);
    - > INSERT INTO EQUIPMENT VALUES (5, crane, 2017, 2018);
  - Assumption: only full tuples can be inserted into the relation.
  - **Note**: Key and/or full tuple cannot be a duplicate.
  - **Note**: Insert is where the syntax of our system diverges from SQL slightly. A SQL insert would look like *INSERT INTO CUSTOMERS (first, last) VALUES (David, Ortiz);* which allows for partial tuples to be entered. Because our system only allows full tuples, we have chosen to make the insert statement easier by not having to specify the attribute names.
  3. UPDATE
  - The system will update values in every tuple that matches conditions stated.
  - Syntax
    - > UPDATE <relation\> SET <col\> = <val\> WHERE <condtions\>
  - Examples
    - > UPDATE customers SET age = 30 WHERE last = Frieder
  4. DELETE
  - The system will delete a tuple from a relation and return the updated relation to the parser.
  - Syntax
    - > DELETE FROM <relation\> WHERE <conditions\>
  - Examples
    - > DELETE FROM customers WHERE first = donald;

## Main Memory Execution
1. Attribute value distributions
   - Conjunctive and disjunctive selections - our system allows for both conjunctive and disjunctive selections using set union and intersections, respectively
   ```
   if conditions[condition_num-1] == "and":
      intersection_list = list(set(matched_rows_list[0]) & set(matched_rows_list[itr]))
      matched_rows_list[0] = intersection_list[:]
      itr+=1
   elif conditions[condition_num-1] == "or":
      intersection_list = list(set(matched_rows_list[0]) | set(matched_rows_list[itr]))
      matched_rows_list[0] = intersection_list[:]
      itr +=1
   ```
2. Efficient sorting
  - The system uses merge-scan to join relations together, being more efficient than a nested loop join. When two relations are in a select statement, merge-scan is used to join those relations specified together.

## Storage Structures
  Our system has the ability to save the state of the database between executions of the program. Using the python package *pickle*, the system saves each relation to a file of that relations name in the subdirectory *Storage*.
  - Save state
  ```
  def save_state(database):
      dir = "Storage"
      for relation in database.relationList:
          filename = str(relation.name)
          cwd = os.getcwd()
          file = os.path.join(cwd,dir,filename)
          with open(file, 'wb') as output:
              pickle.dump(relation, output, pickle.HIGHEST_PROTOCOL)
  ```
  - Restore state
  ```
  def restore_state():
      database = Database()
      relationList = []
      dir = "Storage"
      cwd = os.getcwd()
      mypath = os.path.join(cwd,dir)
      onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
      for file in onlyfiles:
          file = os.path.join(mypath,file)
          with open(file, 'rb') as input:
              relation = pickle.load(input)
              database.relationList.append(relation)
      return database
  ```

## Estimated Grade
Our estimate of our grade on this project is a 92%. We feel this is an accurate grade given that almost all required functions of our database management system execute with efficiency and consistency. With few small assumptions and little to no deviation from SQL grammar, our system operates according to our detailed documentation and project specifications. Thank you.

----
**April 25th, 2019**
