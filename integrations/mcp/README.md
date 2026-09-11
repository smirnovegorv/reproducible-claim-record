# MCP tools

The public checker at foragents.site exposes two tools over the Model
Context Protocol, in that site's server:

| Tool | What |
|---|---|
| `rcr_check` | takes the text of one record, answers with the verdict: `ok` with the flags a reader should see, or the problems, one per line, each named by field |
| `rcr_spec` | returns the current text of the specification |

The tools call the same checker as `python -m rcr`; they store nothing. A
server of your own can offer the same two tools on top of the reference
package: `rcr.check` and `rcr.report` for the first, `rcr.spec_text` for
the second. The server code for foragents.site lives in that site's
repository, because it is that site's server, not part of the format.
