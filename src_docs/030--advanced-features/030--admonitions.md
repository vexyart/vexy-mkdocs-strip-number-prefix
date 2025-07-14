# Admonitions

Admonitions are special styled blocks for important information.

!!! note "Note Title"
    This is a note admonition. Use it for supplementary information.

!!! tip "Pro Tip"
    The strip-number-prefix plugin works seamlessly with MkDocs Material's admonitions!

!!! warning "Warning"
    Make sure your file naming is consistent to avoid URL collisions.

!!! danger "Danger"
    Never use the same number prefix for multiple files in the same directory.

!!! success "Success"
    Your documentation now has clean URLs!

!!! question "Question"
    Did you know you can customize the prefix pattern?

!!! info "Information"
    This plugin is compatible with all MkDocs themes.

!!! example "Example"
    ```yaml
    plugins:
      - strip-number-prefix:
          pattern: '^\d{3}_'
    ```

!!! quote "Quote"
    "Clean URLs make for better documentation" - Every developer

## Collapsible Admonitions

??? note "Click to expand"
    This content is hidden by default!

???+ tip "Expanded by default"
    This content is visible by default but can be collapsed.

[Previous: Tables](020--tables.md) | [Next: Images](040--images.md)