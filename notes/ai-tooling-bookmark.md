# AI Tooling Bookmark

> Saved 2026-06-16. A curated reference list of 52 AI coding/agent/MCP tools.
> Preserved verbatim as provided. Star counts and claims are as-listed and
> have not been independently verified.

## Part 1: AI Coding Agents & IDEs 🛠️
Tools that let AI write, review, and manage code on your behalf.

1. **Claude Code** — Anthropic's command-line coding agent. Reads files, writes code, runs tests, operates directly in your local environment. https://docs.anthropic.com/en/docs/claude-code
2. **Cursor** — AI-first code editor built on VS Code. Inline completions, chat with your codebase, multi-file editing. https://www.cursor.com
3. **Codex CLI** — OpenAI's terminal coding agent. Natural-language instructions, reads codebase, writes/executes code. https://github.com/openai/codex
4. **Windsurf** — AI coding IDE by Codeium. Cascade agent for multi-file editing and deep codebase understanding. https://codeium.com/windsurf
5. **Superpowers** — 20+ Claude Code skills (TDD, debugging, plan-to-execute). https://github.com/obra/superpowers
6. **Spec Kit (GitHub)** — Spec-driven development; write specs, AI generates code. https://github.com/github/spec-kit
7. **Aider** — AI pair programming in your terminal; works with any LLM. https://github.com/paul-gauthier/aider

## Part 2: Agent Frameworks 🤖
Build autonomous systems that think, act, and iterate.

8. **OpenClaw** — Open-source AI agent; persistent, multi-channel (WhatsApp, Telegram, Discord), writes its own skills. https://github.com/openclaw/openclaw
9. **LangGraph** — Multi-agent orchestration as code; graphs with branching, human-in-the-loop, persistent state. https://github.com/langchain-ai/langgraph
10. **CrewAI** — Multi-agent framework with roles, goals, backstories. https://github.com/crewAIInc/crewAI
11. **AutoGPT** — Autonomous agent platform for long-running tasks. https://github.com/Significant-Gravitas/AutoGPT
12. **Dify** — Open-source LLM app builder (workflows, RAG, agents, model management). https://github.com/langgenius/dify
13. **OWL** — Multi-agent cooperation framework; tops the GAIA benchmark. https://github.com/camel-ai/owl
14. **CopilotKit** — Embed AI copilots into React applications. https://github.com/CopilotKit/CopilotKit
15. **pydantic-ai** — Type-safe agent framework built on Pydantic. https://github.com/pydantic/pydantic-ai

## Part 3: MCP Servers & Tool Integration 🔗
MCP gives AI access to the outside world.

16. **Tavily** — Search engine built for AI agents (search, extract, crawl, map). Remote MCP. https://github.com/tavily-ai/tavily-mcp
17. **Context7** — Injects up-to-date library docs into the LLM context. Add "use context7". https://github.com/upstash/context7
18. **Task Master AI** — Feed it a PRD; generates structured tasks with dependencies. https://github.com/eyaltoledano/claude-task-master
19. **MCP Playwright** — Browser automation for LLMs via natural language. https://github.com/executeautomation/mcp-playwright
20. **fastmcp** — Build MCP servers in minimal Python. https://github.com/jlowin/fastmcp
21. **markdownify-mcp** — Convert PDFs, images, audio into Markdown. https://github.com/zcaceres/markdownify-mcp
22. **MCPHub** — Manage multiple MCP servers via HTTP; one dashboard. https://github.com/samanhappy/mcphub

## Part 4: Claude Skills (Top Picks) 🧠
Skills teach Claude specialized workflows.

23. **PDF Processing (Official)** — Read, extract tables, fill forms, merge/split PDFs. https://github.com/anthropics/skills/tree/main/skills/pdf
24. **Frontend Design (Official)** — Real design systems, bold typography, production-grade UI. https://github.com/anthropics/skills/tree/main/skills/frontend-design
25. **Skill Creator (Official)** — Describe a workflow in plain English, get a SKILL.md back. https://github.com/anthropics/skills/tree/main/skills/skill-creator
26. **Marketing Skills by Corey Haines** — 20+ skills: CRO, copywriting, SEO, email, growth. https://github.com/coreyhaines31/marketingskills
27. **Claude SEO** — Full-site audits, schema validation, keyword analysis (12 sub-skills). https://github.com/AgriciDaniel/claude-seo
28. **Obsidian Skills** — Auto-tagging, auto-linking, vault-native ops (by Obsidian's CEO). https://github.com/kepano/obsidian-skills
29. **Context Optimization** — Reduce token costs, improve KV-cache efficiency. https://github.com/muratcankoylan/agent-skills-for-context-engineering
30. **Deep Research Skill** — 8-phase research with auto-continuation. https://github.com/199-biotechnologies/claude-deep-research-skill

## Part 5: Local AI & Model Running 🖥️
Run models on your own hardware.

31. **Ollama** — Run open-source LLMs locally with one command. https://github.com/ollama/ollama
32. **Open WebUI** — Self-hosted ChatGPT-like interface; pairs with Ollama. https://github.com/open-webui/open-webui
33. **LlamaFile** — Package an entire LLM as a single executable file. https://github.com/Mozilla-Ocho/llamafile
34. **Unsloth** — Fine-tune models 2x faster with 70% less memory. https://github.com/unslothai/unsloth
35. **vLLM** — High-throughput inference engine for production serving. https://github.com/vllm-project/vllm

## Part 6: Workflow & Automation ⚡
Connect AI to your existing tools and processes.

36. **n8n** — Open-source workflow automation, 400+ integrations, AI nodes. https://github.com/n8n-io/n8n
37. **Langflow** — Visual drag-and-drop for agent pipelines. https://github.com/langflow-ai/langflow
38. **Huginn** — Self-hosted web agents for monitoring, alerts, data collection. https://github.com/huginn/huginn
39. **DSPy** — Program (not prompt) foundation models. https://github.com/stanfordnlp/dspy
40. **Temporal** — Durable workflow engine for long-running processes. https://github.com/temporalio/temporal

## Part 7: Search, Data & RAG 🔍
Get information into and out of AI systems.

41. **GPT Researcher** — Autonomous research agent producing compiled reports. https://github.com/assafelovic/gpt-researcher
42. **Firecrawl** — Turn any website into LLM-ready data. https://github.com/mendableai/firecrawl
43. **Vanna AI** — Natural language to SQL. https://github.com/vanna-ai/vanna
44. **Instructor** — Structured JSON outputs from any LLM via Pydantic models. https://python.useinstructor.com
45. **Chroma** — Open-source vector database for semantic search / memory. https://github.com/chroma-core/chroma
46. **dlt** — LLM-native data pipelines from 5,000+ sources. https://github.com/dlt-hub/dlt
47. **ExtractThinker** — ORM for document intelligence; structured extraction. https://github.com/enoch3712/ExtractThinker

## Part 8: API & Infrastructure 🏗️
The plumbing that makes everything work in production.

48. **FastAPI** — Python web framework for serving AI apps. https://github.com/tiangolo/fastapi
49. **Portkey Gateway** — Route requests to 250+ LLMs through one API. https://github.com/Portkey-AI/gateway
50. **OmniRoute** — API proxy for 44+ AI providers; load balancing, fallbacks. https://github.com/diegosouzapw/OmniRoute
51. **lmnr** — Trace and evaluate agent behavior. https://github.com/lmnr-ai/lmnr
52. **Codebase Memory MCP** — Convert your codebase into a persistent knowledge graph. https://github.com/DeusData/codebase-memory-mcp

## Part 9: Curated Collections & Learning 📚
Where to find more and keep learning.

53. **Awesome Claude Skills** — The best curated skill list. Start here for new skills. https://github.com/travisvn/awesome-claude-skills
54. **Anthropic Skills Repo** — Official reference implementations from Anthropic. https://github.com/anthropics/skills
55. **Awesome Agents** — 100+ open-source agent tools in one curated list. https://github.com/kyrolabs/awesome-agents
56. **PromptingGuide** — Comprehensive prompt engineering reference. https://www.promptingguide.ai
57. **Anthropic Prompt Engineering Tutorial** — 9 chapters of hands-on Jupyter exercises. https://github.com/anthropics/prompt-eng-interactive-tutorial
58. **SkillsMP** — Marketplace with 80,000+ community skills. https://skillsmp.com
59. **MAGI//ARCHIVE** — Daily feed of fresh AI repos. https://tom-doerr.github.io/repo_posts/
60. **Anthropic Official Docs** — API, prompting, tool use, agents. https://docs.anthropic.com

## How to Actually Use This List
Don't try to install all 60 tools at once. Pick one path, go deep, add more as needs grow.

- **If you're a developer:** Claude Code (01) + Superpowers (05) + Context7 (17) + Tavily (16) — AI coding setup with search and docs access.
- **If you're a creator / knowledge worker:** OpenClaw (08) + Obsidian Skills (28) + PDF Processing (23) + Frontend Design (24) — assistant with file management, document processing, content creation.
- **If you're building a product:** FastAPI (48) + Instructor (44) + Chroma (45) + LangGraph (09) — backend framework, structured outputs, memory, agent orchestration.
- **If you want to learn:** Anthropic Tutorial (57) + PromptingGuide (56) + Anthropic Docs (60) — build the foundation before stacking tools.

## TL;DR
- **Skills** = teach AI *how* to do things better.
- **MCP** = give AI *access* to external tools and data.
- **Repos** = the open-source engines powering it all.

---

## Bonus: Claude Code Power-Ups (de-duplicated & URL-verified)
> Cleaned 2026-06-16. URLs confirmed reachable via raw.githubusercontent.com
> (a README exists on the default branch). ✅ = verified. ⚠️ = could not
> verify; source URL was truncated. Items already in Parts 1–9 above were
> dropped to avoid duplicates (Superpowers → #5, Obsidian Skills → #28).

- ✅ **Claude Mem** — Persistent memory across sessions; stop re-teaching Claude your codebase. https://github.com/thedotmack/claude-mem
- ✅ **n8n-MCP** — Connect Claude Code to 400+ n8n integrations via MCP. https://github.com/czlonkowski/n8n-mcp
- ✅ **LightRAG** — Graph + vector RAG; understand large codebases structurally. https://github.com/HKUDS/LightRAG
- ✅ **Everything Claude Code** — Skills, instincts, security scanning, multi-language; full agent harness. https://github.com/affaan-m/everything-claude-code
- ✅ **Awesome Claude Code** — Curated skills, hooks, slash commands, orchestrators. https://github.com/hesreallyhim/awesome-claude-code
- ✅ **Claude Code Ultimate Guide** — Docs, templates, quizzes; beginner to power user. https://github.com/FlorianBruniaux/claude-code-ultimate-guide
- ✅ **Antigravity Awesome Skills** — 1,200+ ready-to-use skills; large collection. https://github.com/sickn33/antigravity-awesome-skills
- ✅ **Claude Agent Blueprints** — 75+ agent workspace templates beyond coding. https://github.com/danielrosehill/claude-agent-blueprints
- ✅ **Awesome Claude Plugins** — Repos indexed with adoption metrics. https://github.com/quemsah/awesome-claude-plugins
- ✅ **GSD (Get Shit Done)** — Claude Code workflow toolkit. https://github.com/gsd-build/get-shit-done
- ✅ **Agency Agents** — 120+ specialized AI agents across 12 divisions (engineering, design, marketing, etc.); MIT, works with Claude Code/Cursor/Copilot/Gemini/Windsurf. Install: `cp -r agency-agents/* ~/.claude/agents/`. https://github.com/msitarzewski/agency-agents · [agent index spreadsheet](https://docs.google.com/spreadsheets/d/1wiSGtWO4S_JgUE3y30pLJi94ts8uqGNL/edit)
- ⚠️ **UI UX Pro Max** — 50+ styles, 161 palettes, 99 UX guidelines. Source URL truncated (`github.com/nextlevelbuild…`); couldn't resolve the exact repo.
- ⚠️ **VoiceMode MCP** — Voice conversations with Claude Code via Whisper + Kokoro. Source URL truncated (`github.com/mikecbaley/voi…`); couldn't resolve the exact repo.

> Dropped as duplicates of Parts 1–9: **Superpowers** (#5), **Obsidian Skills** (#28).
