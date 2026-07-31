# agentic_projects

Personal workspace for the [Master AI Agentic Engineering](https://github.com/ed-donner/agents) course.

This is a **private fork** of the course materials for personal learning and experimentation. It intentionally excludes all `community_contributions` folders from the upstream repo.

## Upstream course

- Course repo: [ed-donner/agents](https://github.com/ed-donner/agents)
- Setup instructions: [setup/SETUP-mac.md](setup/SETUP-mac.md)

## Structure

| Folder | Description |
|--------|-------------|
| `1_foundations/` – `6_mcp/` | Weekly course labs and reference code |
| `guides/` | Supplemental guides and notebooks |
| `setup/` | Environment setup instructions |
| `projects/` | Personal agent projects (not shared with the community repo) |

## Setup

```bash
cd /Users/alansaucedo/projects/agentic_projects
uv venv .venv --python 3.12
source .venv/bin/activate
uv sync
```

## Personal projects

- [`projects/job-scout-agent/`](projects/job-scout-agent/) — Job search, ranking, and cover letter pipeline

## Syncing course updates

Pull updates from the read-only upstream clone at `/Users/alansaucedo/projects/agents`, then re-run rsync with the same exclude rules into this repo. Do not push personal work to the community course repo.

## License

Course materials retain the upstream [LICENSE](LICENSE) from the Ed Donner agents repository.
