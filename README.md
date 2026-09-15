# Lesson

Learn API design and debugging with an agent. Start with the system context, focus on one issue, improve it through code and discussion, then revisit the wider impact.

Each lesson assumes the reader has not read the relevant source. Use real code or labeled pseudocode. Save articles as `lesson/YYYY-MM-DD-{bug|design}-topic.md` in the target project, with YAML frontmatter. Revise by deleting and rebuilding the article.

See [SKILL.md](plugins/lesson/skills/lesson/SKILL.md) for the full workflow. The plugin contains only a skill, with no runtime dependencies.

The same skill ships through GitHub and npm: Codex uses a Git marketplace, Pi uses npm, and other compatible clients can use Skills CLI.

## Entry points

| Entry | Example | When to write |
| --- | --- | --- |
| Active learning | "Help me learn this project's API design. Let's find and improve one issue." | After analysis, tradeoffs, and validation; for explanation only, after clarifying behavior and boundaries |
| Retrospective | "Turn the bug fix we just completed into a lesson." | After checking existing code and evidence, without repeating completed work |

Invoke the skill explicitly or express learning intent in a client that supports implicit selection. Routine fixes, reviews, and optimizations do not trigger it by default. Implicit selection depends on the client; invoke explicitly when you want to ensure activation.

Follow-up questions and changes on the same topic continue the workflow without a new invocation or article each turn. Exit when learning ends or the topic changes. Requested progress records may be written earlier, with unfinished work and validation gaps marked. Installation does not enable automatic retrospectives.

## Install in Codex

After a version is published, run these commands. Replace `v0.1.0` with the desired [release](https://github.com/shenxiangzhuang/lesson/releases):

```sh
codex plugin marketplace add shenxiangzhuang/lesson --ref v0.1.0
codex plugin add lesson@lesson
```

Restart Codex, start a new task, and invoke `$lesson`:

```text
$lesson Explore this client's API with me. Start with the system context,
focus on one small design issue, explain the code and options, implement
and validate the improvement, and write a self-contained lesson.
```

To upgrade or roll back, remove the marketplace registration, then repeat the installation commands with the target tag:

```sh
codex plugin marketplace remove lesson
# Repeat the two installation commands above with the target version.
```

Codex treats different Git refs as different sources. Remove the registration before switching to a local directory or development branch too. Pinned tags do not follow development changes.

To follow development, install with `--ref master`, then update with:

```sh
codex plugin marketplace upgrade lesson
codex plugin add lesson@lesson
```

You can also add a GitHub marketplace from the Codex plugin page: use repository `shenxiangzhuang/lesson` and the target tag as the Git ref, then install Lesson.

## Install in Pi

After the version is published to npm:

```sh
pi install npm:@shenxiangzhuang/lesson@0.1.0
```

Start a new Pi session and invoke `/skill:lesson`.

The package's `pi.skills` points to the same skill directory as Codex. To upgrade or roll back, repeat the command with the target version. Pinned versions do not follow the latest release. See the [Pi package docs](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/packages.md).

## Other clients

Once the code is on GitHub, install with [Skills CLI](https://skills.sh/docs/cli) and select your client:

```sh
npx skills add shenxiangzhuang/lesson --skill lesson
```

OpenCode can use this skill installation method. This npm package has no OpenCode JavaScript plugin entry point, so do not add it to OpenCode's `plugin` configuration.

## Local validation

```sh
python3 scripts/check-release.py
codex plugin marketplace add .
codex plugin add lesson@lesson
codex plugin list --marketplace lesson --json
```

The check requires Python 3.9+, Node.js, and npm. It packs into a temporary directory, verifies that Pi and Codex share the same skill and that package contents match the source, then removes the temporary package. It installs no project dependencies.

The remaining commands configure the current user's Codex. Start a new task to try the installed skill. Packaging checks do not validate teaching quality in real use.

## Releases

[package.json](package.json) owns the version, in `X.Y.Z` format. Bump it with:

```sh
npm version patch --no-git-tag-version
```

The npm `version` hook syncs the [Codex manifest](plugins/lesson/.codex-plugin/plugin.json). Use `minor`, `major`, or an exact version as needed. Commit both manifests; checks reject mismatched npm, Codex, and Git tag versions.

### Set up npm publishing

The proposed package name is `@shenxiangzhuang/lesson`. The publishing account needs access to that scope. To use another scope, update `package.json` and the installation examples.

The workflow supports npm Trusted Publishing (OIDC). Before the package exists, add an `NPM_TOKEN` with publish access to the repository's Actions secrets for the first tagged release. After that release, add a GitHub Actions trusted publisher in the npm package settings:

- Organization or user: `shenxiangzhuang`
- Repository: `lesson`
- Workflow filename: `release.yml`
- Allowed actions: allow direct `npm publish`

Then remove `NPM_TOKEN` to use OIDC for later releases. The workflow uses a GitHub-hosted runner, Node.js 24, and `id-token: write`. See [npm Trusted Publishing](https://docs.npmjs.com/trusted-publishers/).

### Push a release tag

1. Update the skill or plugin metadata, bump with `npm version`, commit, and push to `master`. Wait for checks to pass. The first release can use the existing `0.1.0`.
2. Tag that commit with the matching `vX.Y.Z` and push. For the first release:

   ```sh
   python3 scripts/check-release.py v0.1.0
   git tag -a v0.1.0 -m "Release v0.1.0"
   git push origin v0.1.0
   ```

3. The [release workflow](.github/workflows/release.yml) validates the packages and tag, publishes npm, then creates a GitHub Release with generated notes. Failed checks or npm publication prevent the GitHub Release.

If npm succeeds but GitHub Release creation fails, use **Re-run failed jobs** in GitHub Actions. Do not republish the existing npm version.

Codex installs from Git tags; Pi installs from npm. Both receive the same skill at the same version. Keep published tags and npm versions immutable; publish a new version for revisions.

Distribution follows [Ponytail](https://github.com/dietrichgebert/ponytail) and the [OpenAI plugin docs](https://developers.openai.com/codex/plugins/build). Relative marketplace paths keep the plugin in the same Git snapshot, so a pinned tag also pins its skill content.

## License

[MIT](LICENSE)
