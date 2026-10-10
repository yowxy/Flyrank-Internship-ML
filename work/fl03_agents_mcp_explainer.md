# FL-03 — Agents, MCP, and What My Pipeline Is Not (yet)

## Part A — explainer (763 words)

**Workflows are recipes; agents are cooks.** A workflow is a fixed path written in code:
step one runs, its output feeds step two, a gate checks the result, step three runs.
Nobody decides anything at runtime — every choice was made when a human drew the boxes.
My related-work pipeline is a workflow: gather, then synthesize, then draft, then my
citation check. Same inputs always take the same route. An agent is different: you give it
a goal and tools, and the *model* decides what to do next, step by step, reading each
tool's result before choosing the next move. The path is not drawn in advance; it emerges
from the model's decisions against live feedback. Anthropic's line is the one that stuck:
workflows orchestrate LLMs through predefined code paths, agents let the LLM direct its own
process and tool use.

The essay's real lesson is restraint. Its patterns form a ladder — prompt chaining (do A,
then B), routing (sort the input, send it left or right), parallelization (split the work,
merge the answers), orchestrator-workers (a planner that invents subtasks per input),
evaluator-optimizer (draft, critique, repeat) — and agents sit at the top, past all of
them. The rule: climb only when the simpler rung demonstrably fails, because every rung
costs latency, money, and new ways to be wrong. Most jobs, including mine so far, never
need the top. A chain with a human gate beats an agent with no leash whenever correctness
matters more than autonomy — which, for graded work and client-facing claims, is always.

So when is an agent the right call? Three conditions, all present in the essay's own
examples (support bots, coding agents): the task is open-ended enough that you cannot
pre-draw the steps, the environment gives ground truth at every step (test results, API
responses — something the model can check itself against, not vibes), and a human still
holds the checkpoints that matter. Miss any one and you have either a workflow wearing a
costume or an unguided process accumulating errors. "Agent" is the most abused word in AI
right now precisely because vendors skip this test: if the path is fixed, it is a
workflow; calling it an agent charges agent prices for recipe reliability.

MCP — the Model Context Protocol — is the other half of the story, and it is gloriously
boring, which is why it works. Before MCP, every AI app wired every tool by hand: one
custom plugin for files, another for search, another for the database. MCP replaces the
pile of bespoke plugs with one standard socket — Anthropic's "USB-C port" framing is
exact. A **server** exposes things; a **client** (inside your app: Claude Desktop, VS
Code, Claude Code) connects to it; the **host** app coordinates. Servers offer three
primitives: **tools** (things the model can *do* — run a query, write a file, call an
API), **resources** (things the model can *read* — file contents, schemas, records), and
**prompts** (reusable instruction templates — the house style, enforced at the socket, not
pasted into every chat). Transports are stdio for local servers and streamable HTTP for
remote ones, all in JSON-RPC. That is the whole idea: any model, any tool, one contract.

What does this unlock that chat cannot do? Everything chat cannot touch. Chat alone cannot
read my repo, cannot execute code, cannot query a live service — it only has what I paste.
Through MCP, the model lists a directory itself, reads the file it needs, runs the check,
and quotes the result with a file and line number. The three tasks below are the receipts:
a local read, a live recomputation, and a live Hub search, each impossible from inside the
chat box, each verified against ground truth rather than memory.

What would turn my pipeline into an agent? One concrete upgrade, and I can name its shape
from the essay: an **evaluator-optimizer loop around the refresh queue**. Today the path
is fixed — I pick features, train once, read receipts. As an agent, the loop would close
itself: train, read its own receipts (P@50 vs the 0.24 bar, leakage asserts, holdout
discipline), decide what to change (drop a feature, move a threshold, re-split), retrain,
and stop only at the bar or after three tries — with my checkpoint before anything
publishes. That is the precise boundary: the day the pipeline chooses its own next step
from its own measurements, it graduates from workflow to agent. Until then it is a good
workflow, and good is not a consolation prize — it is the essay's explicit recommendation.

## Part B — classification (my pipelines, honestly labelled)

- **FL-02 related-work pipeline: workflow (prompt chaining + human gate).** Fixed four
  steps, fixed handoffs, fixed prompts; the only decisions (source choice, gate verdict)
  are mine. No runtime autonomy anywhere.
- **ML refresh-queue build (scripts/run_all.py + my notebooks): workflow (orchestrated
  stages with gates).** Prepare → baseline → train → evaluate → PDF runs the same path
  every time; asserts and my reviews are the gates. The Week-5 model does not pick its
  own features — I do.
- **Neither is an agent**, and neither should be yet: both have fixed paths, human-held
  checkpoints (grades, client claims), and no need for runtime step invention. Upgrading
  means the evaluator-optimizer loop in Part A — named, scoped, with a stopping rule.

## Part C — connector evidence

**My in-session tool-call evidence (this chat is an MCP-shaped loop: resources + tools +
live search, model-directed):** three tasks plain chat could not do, all verified against
ground truth, none from memory.

1. **Local resource read** — `read`-equivalent on my own repo: `scripts/04_evaluate_and_export.py`
   is 411 lines, `scripts/03_train_model.py` is 301, seed is `RANDOM_STATE = 42`
   (scripts/03_train_model.py:38,85,104). Chat alone cannot see my filesystem.
2. **Live execution** — recomputed the W04 triple-flag block rate from the CSV just now:
   **0.6557 (n=3,529)**. Not recalled — executed. Matches the committed receipts JSON exactly.
3. **Live external search** — Hugging Face runs an official MCP server (huggingface.co/mcp,
   setup at huggingface.co/settings/mcp): Hub search, datasets, papers, docs, Jobs and
   sandboxes as callable tools. This was unknown to me before the lookup — it is the
   connector I recommend below, found by tool use, not memory.

**Your 10-minute setup (screenshots = your evidence; I cannot click your app):**
Claude Desktop → Settings → Connectors → add **Hugging Face** (huggingface.co/mcp, log in,
approve) + **Filesystem** (point at your repo clone). Then run three tasks and screenshot
each tool call: (1) *"List the files in work/notebooks and tell me which two are biggest"*
(filesystem read — chat can't see your disk); (2) *"Search the Hub for the FlyRank
internship-warehouse dataset and report its tables"* (live Hub query — beyond training
data); (3) *"Read work/outputs/w04_baseline_receipts.json and say whether P@50 beats 0.24"*
(grounded read + arithmetic on your real receipts). Passing bar per the brief: outputs show
tool invocations with results, not fluent paragraphs from memory.
