
# TODO

## Future Improvements

* Add end-to-end test that spins up a minimal MkDocs build to catch regressions
  automatically.
* Add Windows CI job to ensure path separator handling remains correct (`Path`
  vs `/`).
* Consider exposing a `dry-run` mode that just logs transformations without
  mutating objects (useful for debugging large projects).
* Improve test coverage for the new `on_nav` hook functionality.

