# cosc280project
*Created in Python*

*Possible Grammar: https://www.jooq.org/doc/latest/manual/sql-building/sql-parser/sql-parser-grammar/*

TO DO LIST (4/19)
  1. Finish eval_delete() - if time allows
  2. ~~Incorporate table class into existing evaluator and parser (mostly done)~~
  3. ~~Look into incorporating < and >~~
  4. Get indexes to work
  5. Relational schema
      1. ~~Create a way to keep track of tables (list of tables)~~
      2. Parser accounts for aliases
      3. ~~Write a join algorithm (probably merge-scan) but could be nested~~

Parser TODO:
  1. Tokenize the input
  2. Validate that it's in a valid form / each token is valid
  3. Semantical analysis - https://sqldep.com/sql-parser/

*User starts the project, which opens up a prompt for entering queries*
