# WP-10 stdout-default migration

## Active behavior

Artifact-producing commands now select stdout when `-o` is omitted:

```text
No -o supplied  -> stdout
-o -            -> stdout
-o FILE         -> controlled filesystem publication
```

This applies to `pack`, `envelope`, and `unwrap`.

Automation that depended on an implicit numbered output must provide `-o FILE` explicitly. Filesystem publication remains atomic and symlink-safe. `--force` is invalid for omitted output and `-o -`. Artifact stdout contains artifact bytes only; diagnostics use stderr and reports require an explicit report path.
