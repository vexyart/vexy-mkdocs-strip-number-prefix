# File layouts

These layouts show how to number files and what URLs they produce with the
default pattern `^\d+--`.

## Sequential numbering

Number in steps of 10 so you can insert pages later without renaming others.
Use the same number of digits everywhere, so that names sort correctly:
`010`, `020`, ... `100`, not `10`, `20`, ... `100`.

```text
docs/
├── index.md                  → /
├── 010--introduction.md      → /introduction/
├── 020--installation.md      → /installation/
├── 030--configuration.md     → /configuration/
├── 040--advanced.md          → /advanced/
└── 999--troubleshooting.md   → /troubleshooting/
```

`999--` keeps a page at the end however many pages you add.

## Grouped numbering

Use the hundreds digit for a topic and the tens for pages within it. All
files stay in one folder:

```text
docs/
├── 100--getting-started.md   → /getting-started/
├── 110--installation.md      → /installation/
├── 120--first-steps.md       → /first-steps/
├── 200--configuration.md     → /configuration/
├── 210--basic-config.md      → /basic-config/
├── 220--advanced-config.md   → /advanced-config/
└── 900--appendix.md          → /appendix/
```

## Numbered folders

Prefix folders as well as files. Both are cleaned:

```text
docs/
├── 010--getting-started/
│   ├── 010--quickstart.md     → /getting-started/quickstart/
│   ├── 020--installation.md   → /getting-started/installation/
│   └── 030--first-steps.md    → /getting-started/first-steps/
├── 020--user-guide/
│   ├── 010--basics.md         → /user-guide/basics/
│   └── 020--configuration.md  → /user-guide/configuration/
└── 030--reference/
    ├── 010--api.md            → /reference/api/
    └── 020--cli.md            → /reference/cli/
```

Pages in different folders may share a clean name. `010--getting-started/020--installation.md`
and `020--user-guide/020--installation.md` would become
`getting-started/installation.md` and `user-guide/installation.md`, which do
not collide.

## Mixed: only some files numbered

Unprefixed files are left alone, so you can number only the pages whose order
matters:

```text
docs/
├── index.md             → /
├── 010--overview.md     → /overview/
├── 020--tutorial.md     → /tutorial/
├── changelog.md         → /changelog/
└── license.md           → /license/
```

In the automatic navigation, files are sorted by source name, so the
prefixed files (starting with digits) come before `changelog.md` and
`license.md`.

## This site

The documentation you are reading is laid out like this:

```text
src_docs/md/
├── index.md
├── 010--installation.md
├── 020--quickstart.md
├── 030--configuration.md
├── 040--how-it-works.md
├── 050--links-and-navigation.md
├── 060--edge-cases.md
├── 070--migration.md
├── 080--examples/
│   ├── 010--file-layouts.md      ← this page, served at examples/file-layouts/
│   └── 020--prefix-patterns.md
└── 090--development.md
```
