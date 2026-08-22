# Releasing bro-ocr

This is the maintainer-only checklist for shipping a new version to PyPI. Day-to-day work always happens on `dev`; `main` only moves when you're deliberately cutting a release, and a release only ships when a `vX.Y.Z` tag is pushed (see `.github/workflows/publish.yml`).

## One-time setup (already done)

- Trusted publisher registered at `pypi.org/manage/account/publishing/` for `bro-ocr`, pointing at this repo + `publish.yml`. No API token or GitHub secret involved — see the workflow's `permissions: id-token: write`.

## Release flow

1. **Finish your work on `dev`** as usual — commit and push like normal, no special steps yet.

   ```bash
   git checkout dev
   git add .
   git commit -m "..."
   git push origin dev
   ```

2. **Bump the version** in `pyproject.toml` as the last commit before releasing, so the exact commit you tag later is "version X.Y.Z":

   ```toml
   [project]
   version = "0.1.1"   # was 0.1.0
   ```

   ```bash
   git add pyproject.toml
   git commit -m "bump version to 0.1.1"
   git push origin dev
   ```

3. **Merge `dev` into `main`.** Prefer a PR on GitHub so you get a reviewable diff (and, once set up, CI checks) before it lands — direct merge works too if you want to skip that:

   ```bash
   git checkout main
   git pull origin main
   git merge dev
   git push origin main
   ```

4. **Tag the release commit on `main`.** The tag name must start with `v` and match the version you just set in `pyproject.toml` — this is what actually triggers the publish workflow:

   ```bash
   git tag -a v0.1.1 -m "release 0.1.1"
   git push origin v0.1.1
   ```

5. **Watch the Actions tab.** The `publish.yml` workflow runs `build` then `publish` and uploads to PyPI via trusted publishing — no secrets to manage.

6. **Confirm** the new version is live at `https://pypi.org/project/bro-ocr/`.

## For every future version

Steps 1–6 repeat exactly, only the version number changes. There's no separate "first release vs. later release" flow — `0.1.0 → 0.1.1 → 0.2.0 → ...` all go through the same five steps.

A couple of things worth keeping in mind as this repeats:

- **PyPI never lets you reuse a version number.** If `0.1.1` ships broken, the fix is tagging `0.1.2`, not re-tagging `0.1.1` — there's no "overwrite," only "yank" (marks it discouraged, doesn't delete it).
- **Tag version and `pyproject.toml` version should always match.** Nothing currently enforces this automatically — it's on you to keep them in sync until/unless a CI check is added for it.
- **If a `CHANGELOG.md` gets added later**, update it as part of step 2, in the same commit as the version bump, so every tagged release has a matching changelog entry.
