# cosc280project
*Created in Python*

*Possible Grammer: https://www.jooq.org/doc/latest/manual/sql-building/sql-parser/sql-parser-grammar/*

Parser TODO:
  1. Tokenize the input
  2. Validate that it's in a valid form / each token is valid
  3. Semantical analysis - https://sqldep.com/sql-parser/

*User starts the project, which opens up a prompt for entering queries*

Testing out the grammar (not technically accurate grammar, but functions similar)

<program> --> <E>
<E>       --> <DDL>
<E>       --> <DML>
<DDL>     --> CREATE_TABLE | DROP_TABLE | CREATE_INDEX | DROP_INDEX
<DML>     --> SELECT | DELETE
