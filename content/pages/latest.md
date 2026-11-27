---
id: latest
type: reference
title: What changed this month
title_accent: this month
summary: Notable reports and papers on measuring AI-assisted delivery published between 28 October and 27 November 2026.
sources: [atlassian-ai-sdlc-index, larridin-dora-space, hatchworks-agent-eval, aws-verisk-aisdlc, keyhole-2026, sonar-agentic-economics, gamut-agent-eval, atlassian-measuring-ai, github-octoverse-2026, jellyfish-ai-trends, arxiv-newman-levelup, arxiv-ghagentci, jellyfish-ai-investment, linearb-ai-gap]
---

Published 28 October to 27 November 2026, and what each item changes on the map. Figures are each
publisher's own finding for its own population, not targets.

## Three things that moved

**Agents now open a large share of pull requests, but the share depends on the definition.** GitHub
counts pull requests started with an agent, Jellyfish counts merged pull requests with any agent
involvement, and LinearB counts pull requests written by autonomous agents. The map's
[agent-opened pull request share](agent-pr-share.html) page shows all three.

**Cost per unit of output became a reported metric.** Atlassian's AI SDLC Index, Jellyfish's November
trends report and Sonar each published a cost-per-output measure this month. Earlier guides from
Jellyfish and LinearB use other definitions, and no two divide the same costs by the same output. See [AI spend per unit of output](ai-spend-per-output.html).

**Agent reliability needs repeated runs.** Agent evaluation guides from HatchWorks and Gamut both
explain pass^k, success on every one of k runs, and show how fast success falls as runs are repeated. See
[agent task success rate](agent-task-success.html).

## Reports and blogs

| Date | Publisher | What it adds |
|---|---|---|
| 18 Nov | [Atlassian: Introducing the AI SDLC Index](https://www.atlassian.com/blog/company-news/introducing-the-atlassian-ai-sdlc-index) | An index of AI share of merged code and AI spend per unit of output |
| 16 Nov | [Larridin: DORA and SPACE with AI](https://larridin.com/blog/dora-space-metrics-ai) | Keeps DORA as the base and adds AI attribution and cost layers |
| Nov | [Jellyfish: AI Engineering Trends](https://jellyfish.co/ai-engineering-trends/) | Agent involvement in merged pull requests, auto-merges and cost per pull request |
| 6 Nov | [HatchWorks: AI agent evaluation frameworks](https://hatchworks.com/blog/ai-agents/ai-agent-evaluation-frameworks/) | pass^k and containment rate for agents |
| 5 Nov | [AWS: AI-SDLC at Verisk](https://aws.amazon.com/blogs/industries/reinventing-software-delivery-with-ai-sdlc-on-amazon-bedrock-agentcore/) | A single-company case study of agent output acceptance |
| 5 Nov | [Keyhole Software: 2026 benchmarks](https://keyholesoftware.com/developer-productivity-metrics/) | A digest of DORA, SPACE and AI-assisted delivery benchmarks |
| 4 Nov | [Sonar: the economics of agentic development](https://www.sonarsource.com/resources/library/economics-of-agentic-development/) | Cost per accepted change, first-pass acceptance and override rate |
| 4 Nov | [Gamut: AI agent evaluation](https://www.gamut.so/blog/ai-agent-evaluation-guide) | Task success rate and pass^k |
| 3 Nov | [Atlassian: measuring AI across the lifecycle](https://www.atlassian.com/blog/ai-at-work/measuring-and-orchestrating-ai-across-the-full-engineering-lifecycle) | Argues adoption is not the goal; pull request size and onboarding data from DX |
| 28 Oct | [GitHub Octoverse 2026](https://github.blog/news-insights/octoverse/octoverse-commits-pushes-reach-new-highs-in-2026-as-developers-build-with-agents/) | Share of pull requests started with an agent |

## Research

| Date | Paper | What it adds |
|---|---|---|
| 13 Nov | [Newman, Bird, Butler, Murphy-Hill: Level Up!](https://arxiv.org/abs/2611.18939) | How AI-assisted authoring changes code review practice and reviewer load |
| 11 Nov | [Ogenrwot et al.: GHAgentCI](https://arxiv.org/abs/2611.15522) | A public dataset of coding-agent invocations in CI workflow histories |

## Sources
