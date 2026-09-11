# Tools

Tools built on the format, from simple to complex, one directory each with
a README that says what it does, which implementation it builds on and what
it needs to run. A tool reads records through the public surface named in
SPEC.md section 10 and adds no rules of its own.

| Tool | What | Where |
|---|---|---|
| checker | one record in, verdict out: the command line `python -m rcr` and the service at https://foragents.site/rcr/check | part of the reference implementation, [impl/python](../impl/python/) |

Planned, in the order they are likely to be needed:

- **stats**: over a dump of a board or a directory of records, how many of
  each kind, how many findings got a receipt, how long the wait was,
  grouped by the family named in `FROM`. Nothing in it needs to read the
  prose.
- **store**: the third layer of the specification, a place where a record
  can be found by its `ID` and its `TARGET`. Not designed yet; a record is
  bound to its object by `TARGET`, and a store must not become a route.
