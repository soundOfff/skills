# Build a pull request review bot

Comment `/ai-review` on a pull request and get one review back, written by a headless model that cannot touch your repository. This guide builds that in two sizes. Tier 1 is one GitHub Actions workflow and takes an afternoon. Tier 2 is a GitHub App with a queue and a worker, for reviews that run long or need their own identity.

Both tiers reuse this kit's adversarial review: the prompt in [`skills/flow-adv-review/prompts/adversarial-review.md`](../skills/flow-adv-review/prompts/adversarial-review.md) and the output schema in [`skills/flow-adv-review/schemas/review-output.schema.json`](../skills/flow-adv-review/schemas/review-output.schema.json). Locally, `/flow-adv-review` runs the same review on demand.

## What every version needs

1. A trigger and an authorization gate.
2. A pinned target: base SHA, head SHA, and a hash of the diff.
3. Trusted instructions and the JSON schema, read from the default branch.
4. A headless model call with no write credentials in reach.
5. Code that validates, sanitizes, and renders the model's output.
6. One `COMMENT` review, posted by a separate step with minimal permissions.

## How it stays safe

- **The gate is the security boundary.** An `issue_comment` workflow always runs the workflow file from the default branch, with secrets available, even for pull requests from forks. A pull request cannot edit the gate expression that checks the exact comment and the commenter's `author_association`.
- **Instructions come from the default branch.** Read the prompt and the schema from the default-branch tip, never from the pull request head. Otherwise a pull request could rewrite its own reviewer.
- **The job that reads pull request code holds no write token.** The jobs that write never run pull request code.
- **The review is pinned.** Hash the diff with `git diff --binary <base>...<head> | git hash-object --stdin`. Check the head again before you publish, and publish nothing when it moved.
- **The review is a `COMMENT`.** `POST /repos/{owner}/{repo}/pulls/{number}/reviews` also accepts `APPROVE`, and an auto-merge workflow that counts approvals would count a bot's approval as the required one. Always send `COMMENT`, and set `commit_id` to the reviewed head.

Three kinds of credentials appear below. `GITHUB_TOKEN` is the per-run Actions token, and anything it writes is authored by `github-actions[bot]`. A personal access token acts as one person with that person's full scope, so keep it out of bots. A GitHub App has its own identity, its own narrow permissions, and webhooks, and it trades a signed JWT for an installation token that lasts one hour.

## Tier 1: one GitHub Actions workflow

1. Copy the kit's prompt and schema to the default branch of the repository you want reviewed, as `.github/ai-review/prompt.md` and `.github/ai-review/schema.json`.
2. Store the model key and pick the model:

   ```bash
   gh secret set ANTHROPIC_API_KEY
   gh variable set REVIEW_MODEL --body "<model id>"
   ```

3. Add this workflow as `.github/workflows/ai-review.yml`. Replace each `<pinned-sha>` with the commit SHA of the action release you trust, and `<pinned-version>` with an exact Claude Code version.

```yaml
name: AI Review
on:
  issue_comment:
    types: [created]
permissions: {}

jobs:
  authorize:
    if: >-
      github.event.issue.pull_request &&
      github.event.issue.state == 'open' &&
      github.event.comment.body == '/ai-review' &&
      contains(fromJSON('["OWNER","MEMBER","COLLABORATOR"]'),
      github.event.comment.author_association)
    runs-on: ubuntu-latest
    timeout-minutes: 5
    permissions:
      pull-requests: write
    outputs:
      base_sha: ${{ steps.pin.outputs.base_sha }}
      head_sha: ${{ steps.pin.outputs.head_sha }}
    env:
      GH_TOKEN: ${{ github.token }}
      PR: ${{ github.event.issue.number }}
    steps:
      - name: Acknowledge
        continue-on-error: true
        run: >-
          gh api -X POST
          "repos/$GITHUB_REPOSITORY/issues/comments/${{ github.event.comment.id }}/reactions"
          -f content=eyes
      - name: Pin base and head
        id: pin
        run: |
          gh api "repos/$GITHUB_REPOSITORY/pulls/$PR" > "$RUNNER_TEMP/pr.json"
          jq -e '.draft == false' "$RUNNER_TEMP/pr.json" > /dev/null
          echo "base_sha=$(jq -r .base.sha "$RUNNER_TEMP/pr.json")" >> "$GITHUB_OUTPUT"
          echo "head_sha=$(jq -r .head.sha "$RUNNER_TEMP/pr.json")" >> "$GITHUB_OUTPUT"

  review:
    needs: authorize
    runs-on: ubuntu-latest
    timeout-minutes: 45
    permissions:
      contents: read
    concurrency:
      group: ai-review-${{ github.event.issue.number }}
      cancel-in-progress: false
    env:
      BASE: ${{ needs.authorize.outputs.base_sha }}
      HEAD: ${{ needs.authorize.outputs.head_sha }}
      DEFAULT_BRANCH: ${{ github.event.repository.default_branch }}
    steps:
      - uses: actions/checkout@<pinned-sha>
        with:
          ref: ${{ needs.authorize.outputs.head_sha }}
          fetch-depth: 0
          persist-credentials: false
      - name: Trusted instructions and bounded evidence
        run: |
          set -euo pipefail
          git cat-file -e "$BASE^{commit}"
          R="$RUNNER_TEMP/r"; mkdir -p "$R"
          git show "origin/$DEFAULT_BRANCH:.github/ai-review/prompt.md" > "$R/prompt.md"
          git show "origin/$DEFAULT_BRANCH:.github/ai-review/schema.json" > "$R/schema.json"
          git diff --binary "$BASE...$HEAD" | git hash-object --stdin > "$R/diff-hash"
          {
            echo "## Commit log"; git log --oneline "$BASE..$HEAD"
            echo; echo "## Diff stat"; git diff --stat "$BASE...$HEAD"
            echo; echo "## Branch diff"; git diff --no-ext-diff --unified=80 "$BASE...$HEAD"
          } > "$R/evidence.md"
          python3 - "$R" <<'PY'
          import pathlib, re, sys
          r = pathlib.Path(sys.argv[1])
          values = {
              "TARGET_LABEL": "pull request diff",
              "USER_FOCUS": "No extra focus provided.",
              "REVIEW_COLLECTION_GUIDANCE": "",
              "OUTPUT_SCHEMA": (r / "schema.json").read_text(),
              "REVIEW_INPUT": (r / "evidence.md").read_text(),
          }
          prompt = re.sub(r"\{\{([A-Z_]+)\}\}", lambda m: values.get(m.group(1), ""), (r / "prompt.md").read_text())
          (r / "input.md").write_text(prompt)
          PY
          test "$(wc -c < "$R/input.md")" -le 2097152
      - name: Review with zero tools
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          REVIEW_MODEL: ${{ vars.REVIEW_MODEL }}
        run: |
          set -euo pipefail
          npm install -g @anthropic-ai/claude-code@<pinned-version>
          cd "$RUNNER_TEMP/r"
          claude --print --safe-mode --no-chrome --no-session-persistence \
            --model "$REVIEW_MODEL" \
            --permission-mode plan --tools "" --disable-slash-commands \
            --strict-mcp-config --mcp-config '{"mcpServers":{}}' \
            --system-prompt "Perform only the code review described by the user prompt." \
            --output-format json --json-schema "$(cat schema.json)" \
            < input.md > raw.json
          jq -e 'if type == "array" then (map(select(.type == "result")) | last) else . end
            | .structured_output.review' raw.json > review.json
      - uses: actions/upload-artifact@<pinned-sha>
        with:
          name: ai-review
          path: |
            ${{ runner.temp }}/r/review.json
            ${{ runner.temp }}/r/diff-hash

  publish:
    needs: [authorize, review]
    if: always() && needs.authorize.result == 'success'
    runs-on: ubuntu-latest
    timeout-minutes: 5
    permissions:
      pull-requests: write
    env:
      GH_TOKEN: ${{ github.token }}
      PR: ${{ github.event.issue.number }}
      HEAD: ${{ needs.authorize.outputs.head_sha }}
    steps:
      - uses: actions/download-artifact@<pinned-sha>
        if: needs.review.result == 'success'
        with:
          name: ai-review
      - name: Publish exactly one COMMENT review
        run: |
          set -euo pipefail
          live=$(gh api "repos/$GITHUB_REPOSITORY/pulls/$PR" --jq .head.sha)
          [ "$live" = "$HEAD" ] || { echo "Superseded; publishing nothing."; exit 0; }
          if [ -f review.json ]; then
            jq -r --arg hash "$(cat diff-hash)" '
              def safe: gsub("@"; "@​") | gsub("<"; "&lt;");
              "## AI review: \(.verdict)\n\n\(.summary | safe)\n\n"
              + ([.findings[] | "#### \(.severity) · \(.title | safe)\n`\(.file):\(.line_start)` \(.body | safe)\n**Change:** \(.recommendation | safe)\n"] | join("\n"))
              + "\nTarget: `\(env.HEAD[0:7])` · `\($hash[0:12])`"
            ' review.json > body.md
          else
            printf '## AI review: REVIEW INCOMPLETE\n\nThe reviewer failed before producing valid output.\n' > body.md
          fi
          printf '\n<!-- ai-review run:%s head:%s -->\n' "$GITHUB_RUN_ID" "$HEAD" >> body.md
          gh api -X POST "repos/$GITHUB_REPOSITORY/pulls/$PR/reviews" \
            -f event=COMMENT -f commit_id="$HEAD" -F body=@body.md
```

4. Test it in a scratch repository. An `issue_comment` workflow always runs the file on the default branch, so a workflow on a feature branch never triggers. On your own repositories your `author_association` is `OWNER`.

### Notes on the workflow

- **Claude flags.** These are the flags the kit's runner passes in `buildHarnessInvocation()` in [`adapters.mjs`](../skills/flow-adv-review/scripts/lib/adapters.mjs), which its tests and a live run checked against Claude Code 2.1.309, plus `--model`. `--safe-mode` turns off `CLAUDE.md`, skills, plugins, hooks, and MCP servers and keeps normal authentication, so it works with `ANTHROPIC_API_KEY`. The prompt goes on stdin because `--tools` and `--mcp-config` take a variable number of values and would swallow a positional prompt.
- **Array output.** Claude Code 2.1.309 prints `--output-format json` as an array of events that ends with a `result` event, which is why the `jq` filter picks the last `result` before it reads `structured_output`.
- **Codex instead of Claude.** Authenticate with an API key, not a device login, and keep the reviewed repository's own `AGENTS.md` out of the reviewer. These flags are checked against codex-cli 0.161.0:

  ```bash
  codex --strict-config --model "$REVIEW_MODEL" --config model_reasoning_effort="high" \
    --sandbox read-only --ask-for-approval never \
    --config project_doc_max_bytes=0 --config web_search="disabled" \
    exec --ephemeral --ignore-user-config --ignore-rules \
    --cd "$RUNNER_TEMP/r" --output-schema schema.json \
    --output-last-message review.json - < input.md
  ```

- **Validation.** `jq -e` only checks that a review exists. Add a real schema check, such as `ajv-cli`, before the upload. `validateReview()` in the kit's [`contract.mjs`](../skills/flow-adv-review/scripts/lib/contract.mjs) is the reference.

### What Tier 1 does not give you

- **Identity.** `github-actions[bot]` authors every review. For your own name, create a small GitHub App and mint its token in the `publish` job with `actions/create-github-app-token`.
- **Repository context.** With zero tools the model sees only the diff. A middle ground is the Codex command above with `--cd` pointed at the checkout, because its read-only sandbox lets the model read the code.
- **Idempotency.** Re-running the workflow posts a second review. Search the existing reviews for your marker and head SHA first.
- **Queueing.** GitHub keeps only one pending run per concurrency group, so a third request while one runs and one waits is dropped.
- **Compute.** Each job has a six-hour cap, no warm caches, and no persistent login, so you pay API prices.

## Tier 2: a GitHub App with a queue and a worker

Build this when reviews take longer than a workflow should hold, or when you want one review at a time across many repositories. In order of importance:

1. **A GitHub App.** Permissions `pull_requests:write`, `issues:write`, `contents:read`, `checks:read`, and `metadata:read`. The only event is `issue_comment`. Give it nothing else, because every installation token carries every App permission.
2. **A webhook function.** Verify the HMAC-SHA256 signature over the raw body. Accept only an exact trigger, optionally followed by a space and focus text, from an allowed login or a `MEMBER` or `OWNER`. Record the delivery ID with a conditional write, so a redelivered webhook does nothing. Take a per-pull-request lease, queue the job, add a reaction, and return 202. Answer within GitHub's 10-second webhook timeout. GitHub does not redeliver a failed webhook by itself.
3. **A queue, a dead-letter queue, and a table** for deliveries and leases.
4. **A worker.** A Lambda's 15-minute cap rules it out for long reviews. Run it on a small EC2 instance, as one Fargate task per message, or on a Mac at home that long-polls the queue with an IAM user limited to `sqs:ReceiveMessage`, `sqs:DeleteMessage`, `sqs:ChangeMessageVisibility`, and `secretsmanager:GetSecretValue`. The Mac needs no inbound ports.
5. **Monitoring.** A scheduled check for stuck deliveries, and alarms that notify a person.

An untested SST v4 sketch. Check the property names against your SST version:

```ts
export default $config({
  app: () => ({ name: "pr-review-bot", home: "aws" }),
  async run() {
    const webhookSecret = new sst.Secret("GitHubWebhookSecret");
    const appId = new sst.Secret("GitHubAppId");
    const appKey = new sst.Secret("GitHubAppPrivateKey");
    const modelKey = new sst.Secret("ModelApiKey");

    const dlq = new sst.aws.Queue("ReviewDlq");
    const queue = new sst.aws.Queue("ReviewQueue", {
      visibilityTimeout: "20 minutes",
      dlq: { queue: dlq.arn, retry: 3 },
    });
    const deliveries = new sst.aws.Dynamo("Deliveries", {
      fields: { pk: "string" },
      primaryIndex: { hashKey: "pk" },
      ttl: "expiresAt",
    });

    const api = new sst.aws.ApiGatewayV2("Webhook");
    api.route("POST /github/webhook", {
      handler: "src/webhook.handler",
      link: [queue, deliveries, webhookSecret, appId, appKey],
      timeout: "15 seconds",
    });

    new sst.aws.Cron("StaleMonitor", {
      schedule: "rate(5 minutes)",
      function: { handler: "src/monitor.handler", link: [deliveries] },
    });

    return { webhookUrl: api.url };
  },
});
```

The worker is not in the sketch. Add an `aws.ec2.Instance` with an instance profile, a Fargate task, or the IAM user for a Mac, and link it to `queue`, `appKey`, and `modelKey`.

| AWS piece | SST v4 or Pulumi |
| --- | --- |
| Queue and dead-letter queue | `sst.aws.Queue` with `dlq` |
| Table with a TTL | `sst.aws.Dynamo` |
| HTTP API in front of a function | an `sst.aws.ApiGatewayV2` route |
| Scheduled monitor | `sst.aws.Cron` |
| Secrets | `sst.Secret`, or `aws.secretsmanager.Secret` |
| A VPC with public subnets only | a raw `aws.ec2.Vpc`, because `sst.aws.Vpc` adds private subnets and NAT |
| Worker host and its role | `aws.ec2.Instance` (`userData`, `metadataOptions.httpPutResponseHopLimit: 1`, `disableApiTermination`) and `aws.iam.InstanceProfile` |
| Worker deploy step | `aws.ssm.Document` |
| GitHub OIDC deploy role | `aws.iam.OpenIdConnectProvider` and `aws.iam.Role` |

### What stays manual

- **Creating the App.** Use the manifest flow. Serve a page that posts a manifest to `https://github.com/settings/apps/new`, with `hook_attributes.url` set to the `webhookUrl` output, `default_permissions`, and `default_events: ["issue_comment"]`. You click Create, and GitHub redirects back with a `code`. `POST /app-manifests/{code}/conversions` returns the App `id`, its `pem`, and its `webhook_secret`, which a script can pipe into `sst secret set`. Installing the App on your repositories is one more click.
- **Model authentication.** Use an API key stored as a secret. An interactive device login lives on one host as state that no infrastructure code recreates.
- **The first deploy** bootstraps the cloud state.
- **GitHub settings can be code.** `@pulumi/github` covers environments with branch policies, environment secrets, Actions variables, and the OIDC subject template. Runner groups exist only for organizations.

## Swift projects

- **Unchanged:** the trigger, the gate, pinning, trusted instructions, the schema, the renderer, and the `COMMENT` review.
- **Changed:** only the toolchain checks. Use `xcodebuild -version`, `swift build`, `swift test`, `xcodebuild -scheme <scheme> -destination 'platform=macOS' test`, and `swiftlint` or `swift-format lint --strict`.
- **Platform.** A Swift package without Apple frameworks builds on Linux `swift` images. Anything that touches AppKit, SafariServices, extension targets, code signing, or the Simulator needs macOS: GitHub-hosted `macos-*` runners, which cost far more per minute on private repositories, or a self-hosted Mac.
- **Split build from review.** Run build and test in a normal `pull_request` workflow on macOS, and let the reviewer read the pull request's check runs through the API. The review job then stays on cheap Linux and runs no pull request code.
- **Self-hosted Mac on a public repository.** A pull request from a fork can target that runner through its own `pull_request` workflow. Use a self-hosted Mac only for private repositories.

## Gotchas

1. **Never `APPROVE`.** An auto-merge workflow that counts approvals counts the bot's.
2. **Keep the write token away from pull request code.** A worker host that can read the App's private key must never run `install` or build scripts from the pull request with network access.
3. **Give the App only review permissions.** An installation token carries every App permission. If you reuse an App that has broader permissions, the bot inherits them. Never fall back to a personal access token.
4. **Start after CI finishes** if the reviewer reads check runs. A check that has not completed yet reads as a failure.
5. **Mind the schema details.** Wrap the result as `{review: ...}`, because OpenAI's strict mode rejects a top-level `anyOf`. Omit `$schema` for Claude. Encode the verdict in the branches: `approve` requires zero findings and `needs-attention` requires at least one. When the output looks like a review but fails validation, fail the run instead of asking another model, or you are shopping for an approval.
6. **Never truncate the evidence.** Fail the run when it exceeds the bound, for example more than 500 files, more than 2 MiB, or binary files. Cap the captured output streams too, because a CLI can echo the whole prompt to stderr.
7. **Pass an explicit environment.** Removing a few session variables does not hide secrets. On a server, start the model with an allowlisted environment, such as `HOME`, `LANG`, `PATH`, and the temporary-directory variables.
8. **Merges made with `GITHUB_TOKEN` trigger no other workflow.** An auto-merge workflow must dispatch any follow-up workflow itself.
9. **Retries are yours.** GitHub does not redeliver failed webhooks, and a crashed worker keeps its per-pull-request lease until the lease expires.
10. **No inline comments.** GitHub rejects inline comments outside the diff, and one review body is a single atomic write tied to one head SHA.
