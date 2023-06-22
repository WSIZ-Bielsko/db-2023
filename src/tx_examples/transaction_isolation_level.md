# transaction isolation level in postgres

Goal:

- have fast code
- have as much separation from the effects of other thransactions as needed

Solutions:

- isolation leves
- postgres uses Multiversion Concurrency Control, MVCC, [https://www.postgresql.org/docs/current/mvcc-intro.html]

## Problems (read phenomena)

[https://en.wikipedia.org/wiki/Isolation_(database_systems)#Read_phenomena]]

### Dirty Read

- tx2 reads update written by tx1, before tx1 commits

### Lost Update

- tx1 reads, tx2 reads
- tx1 updates (depending on what it read)
- tx2 updates (depending on what it read)
- the tx1 has been overwritten (has no influence on current state)

### Non-Repeatable Read

- tx1 reads
- tx2 writes
- tx1 reads again -- sees different value (although still in transaction)

### Phantom read

[https://stackoverflow.com/questions/11043712/what-is-the-difference-between-non-repeatable-read-and-phantom-read]

- as with Non-Rep Read, but deals with a range of rows
- tx2: select * ... where ...
- tx1: insert into ...
- tx1: commit
- tx2: select * ... where ... --extra rows visible

## Isolation levels

TL&DL:

- READ_UNCOMMITTED prevents nothing. It's the zero isolation level
- READ_COMMITTED prevents just one, i.e. Dirty reads
- REPEATABLE_READ prevents two anomalies: Dirty reads and Non-repeatable reads
- SERIALIZABLE prevents all three anomalies: Dirty reads, Non-repeatable reads and Phantom reads

### 'read_committed'  (default)

When a transaction uses this isolation level:

- SELECT query sees only data committed before _the/this query_ began
- never sees either uncommitted data
- never sees changes committed during (this) query execution by concurrent transactions,
- two successive SELECT commands can see different data (non-rep reads)
- this mode starts each command with a new snapshot that includes all transactions committed up to that instant,

### 'repeatable_read'

- Applications using this level must be prepared to retry transactions due to serialization failures.
  (asyncpg.exceptions.SerializationError)
- 

Here:

- query in a repeatable read transaction sees a snapshot as of the start of
  the first non-transaction-control statement in the transaction,
  not as of the start of the current statement within the transaction
- successive SELECT commands within a single transaction see the same data, i.e., they do not see
  changes made by other transactions that committed after their own transaction started.
- if the first updater commits (and actually updated or deleted the row, not just locked it) then
  the repeatable read transaction will be rolled back with the message
- repeatable read transaction cannot modify or lock rows changed by other transactions
  after the repeatable read transaction began

- The Repeatable Read mode provides a rigorous guarantee that
  each transaction sees a completely stable view of the database

### 'serializable'
