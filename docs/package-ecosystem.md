# B.E.L. Package Ecosystem Design

**Version:** 0.1.0  
**Date:** 2026-06-08  
**Status:** Draft

## Vision
Discoverable, reliable, fast, community-driven, and secure from day one.

## Components
- Central registry (`registry.bel-lang.dev`)
- `bel pkg` with `Bel.toml` + `Bel.lock`
- Semantic versioning enforcement
- Git + path + registry dependencies
- Workspaces, features, build scripts (sandboxed)

## Security (First-Class)
- Package signing + checksums in lockfile
- 2FA + trusted publishing (OIDC)
- Vulnerability database from day one
- Automated scanning + rate limits on new publishers

## Discovery
High-quality search, automatically hosted documentation, badges for maintenance status, download counts, etc.

## Success Targets
Fast resolution and downloads, strong supply-chain security, sustainable governance.
