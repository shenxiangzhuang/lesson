# Lesson

与 Agent 一起学习 API 设计和调试：从全局聚焦一个具体问题，通过代码分析、方案比较和实践完成改进，再回到全局理解影响。

每篇文章都假设读者没有读过相关源码，以真实代码或明确标注的伪代码展开。产物保存在目标项目的 `lesson/YYYY-MM-DD-{bug|design}-主题.md`，带 YAML frontmatter；需要修订时删除旧文档并完整重建。

完整行为约定见 [SKILL.md](plugins/lesson/skills/lesson/SKILL.md)。插件仅包含 skill，无运行时依赖。

同一份 skill 通过 GitHub 和 npm 分发：Codex 使用 Git marketplace，Pi 使用 npm 包，其他支持标准 skill 的客户端可通过 Skills CLI 安装。

## 使用入口

| 入口 | 示例 | 何时生成文档 |
| --- | --- | --- |
| 主动学习 | “我想学习这个项目的 API 设计，一起找一个问题并优化” | 完成该问题的分析、取舍和验证后；只学习现有设计时，在机制与边界讲清楚后 |
| 事后复盘 | “把刚才这个 Bug 的修复整理成 lesson” | 核对已有代码和验证证据后，不重复实施已完成的工作 |

可以显式调用 skill，也可以向支持隐式选择的客户端表达学习或沉淀意图。普通修复、代码审查和优化请求默认不触发；客户端的隐式选择取决于其能力与判断，需要明确进入流程时请显式调用。

同一主题的追问和修改沿用学习流程，无需每轮调用或生成文档；结束学习或切换无关任务时退出。明确要求阶段性记录时可以提前生成，并标明尚未实施或验证的部分。安装本插件不会自动开启每次任务结束后的复盘。

## 安装到 Codex

发布对应版本后，在终端执行以下命令。将 `v0.1.0` 替换为 [Releases](https://github.com/shenxiangzhuang/lesson/releases) 中需要的版本：

```sh
codex plugin marketplace add shenxiangzhuang/lesson --ref v0.1.0
codex plugin add lesson@lesson
```

然后重启 Codex 应用并新建任务，使用 `$lesson` 调用，例如：

```text
$lesson 和我一起检查当前客户端 API，从全局聚焦一个小的设计问题，
解释现有代码与优化方案，完成修改和验证，并生成一篇自包含的 lesson。
```

需要升级或回退时，先移除旧 marketplace 登记，再执行安装命令并将 `--ref` 改为目标版本标签：

```sh
codex plugin marketplace remove lesson
# 随后重新执行上面的两条安装命令，使用目标版本标签。
```

Codex 将不同 Git ref 视为不同来源；切换到本地目录或开发分支前也需要这一步。固定标签不会随着开发分支变化而更新。

若希望跟随开发分支，将 `--ref` 设为 `master`；之后运行：

```sh
codex plugin marketplace upgrade lesson
codex plugin add lesson@lesson
```

Codex 应用也可从插件页面添加 GitHub marketplace：仓库填 `shenxiangzhuang/lesson`，Git ref 填目标版本标签，随后安装 Lesson。

## 安装到 Pi

对应版本发布到 npm 后执行：

```sh
pi install npm:@shenxiangzhuang/lesson@0.1.0
```

开启新的 Pi 会话后，使用 `/skill:lesson` 调用。

包中的 `pi.skills` 指向与 Codex 相同的 skill 目录。升级或回退时重新执行命令，替换目标版本；固定版本不会自动跟随最新版。详见 [Pi 包文档](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/packages.md)。

## 其他支持标准 skill 的客户端

代码推送到 GitHub 后，可通过 [Skills CLI](https://skills.sh/docs/cli) 安装并选择目标客户端：

```sh
npx skills add shenxiangzhuang/lesson --skill lesson
```

这是标准 skill 安装方式。OpenCode 也可通过该方式安装 skill；本 npm 包不包含 OpenCode 所要求的 JavaScript 插件入口，因此不要把它填写到 OpenCode 的 `plugin` 配置中。

## 本地验证

```sh
python3 scripts/check-release.py
codex plugin marketplace add .
codex plugin add lesson@lesson
codex plugin list --marketplace lesson --json
```

检查命令需要 Python 3.9+、Node.js 和 npm，会实际打包到临时目录，验证 Pi/Codex 使用同一份 skill、npm 产物与源码一致，然后清理临时包。检查不安装项目依赖。

后面的本地安装命令会配置当前用户的 Codex。安装后开启新任务测试；打包检查不代表教学效果已经通过真实场景验证。

## 发布版本

版本入口是 [package.json](package.json) 的 `version` 字段，使用 `X.Y.Z` 格式。通过下面的命令升级版本，npm 的 `version` hook 会同步 [Codex 插件清单](plugins/lesson/.codex-plugin/plugin.json)：

```sh
npm version patch --no-git-tag-version
```

也可将 `patch` 改为 `minor`、`major` 或具体版本。将两份清单一起提交；检查会拒绝 npm、Codex 与 Git 标签的版本差异。

### 首次配置 npm 发布

包名暂定为 `@shenxiangzhuang/lesson`，发布账号需要拥有该 scope 的发布权限。若使用其他 scope，修改 `package.json` 与安装示例中的包名。

工作流使用 npm Trusted Publishing（OIDC）。包尚未创建时，可先在 GitHub 仓库的 Actions secrets 中设置有该包发布权限的 `NPM_TOKEN`，供首次标签发布使用。首次发布成功后，在 npm 包设置中添加 GitHub Actions trusted publisher：

- Organization or user：`shenxiangzhuang`
- Repository：`lesson`
- Workflow filename：`release.yml`
- Allowed actions：允许直接 `npm publish`

配置完成后可移除 `NPM_TOKEN`，后续通过 OIDC 发布。工作流使用 GitHub-hosted runner、Node.js 24 和 `id-token: write`。配置规则见 [npm Trusted Publishing 文档](https://docs.npmjs.com/trusted-publishers/)。

### 推送版本标签

1. 修改 skill 或插件元数据，通过 `npm version` 更新版本，提交并推送到 `master`，等待检查通过。初次发布可直接使用已有的 `0.1.0`。
2. 在该提交上创建同版本的 `vX.Y.Z` 标签并推送。例如首次发布：

   ```sh
   python3 scripts/check-release.py v0.1.0
   git tag -a v0.1.0 -m "Release v0.1.0"
   git push origin v0.1.0
   ```

3. [发布工作流](.github/workflows/release.yml) 先校验两种包及标签，然后发布 npm，成功后创建 GitHub Release 并生成发布说明。检查或 npm 发布失败时不创建 GitHub Release。

如果 npm 已成功而 GitHub Release 步骤失败，使用 GitHub Actions 的 **Re-run failed jobs** 仅重试失败的任务；不要重新发布已存在的 npm 版本。

Codex 从 Git 标签安装，Pi 从 npm 安装；两者使用同版本、同内容的 skill。已发布标签与 npm 版本保持不变，后续修订发布新版本。

安装与打包方式参考 [Ponytail](https://github.com/dietrichgebert/ponytail) 和 [OpenAI 插件文档](https://developers.openai.com/codex/plugins/build)。本仓库的 marketplace 使用相对路径引用同一 Git 快照内的插件，使固定标签同时固定 skill 内容。

## 许可证

[MIT](LICENSE)
