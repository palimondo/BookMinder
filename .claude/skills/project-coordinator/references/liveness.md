# Liveness — reclamation survival, watchdogs, resume

**Scope: remote cloud sessions only** (Claude Code on claude.ai/code — web, iOS, desktop-remote). There the session container is reclaimed on inactivity and background work does not keep it alive, so everything below applies. It does NOT apply to local Claude Code (process lives as long as the machine) or to GitHub-Actions-style CI infra (job-scoped lifetime, no mid-run reclamation, no watchdog needed). Check which environment you are in before applying this page.


The platform reclaims the session container after inactivity, and background workflows **do not** count as activity. This is documented only as existing; the window and the definition of activity are undocumented, and the relevant GitHub issues (#51052, #32050) are closed as not-planned. Assume any unattended run will die silently to it unless the architecture below is in place.

The architecture that survives it, in order of importance:

1. **Deliverables committed as they land** — reclamation cannot destroy finished work.
2. **Journal-based resume** — relaunching the workflow against its prior run's journal replays cached agents; a restart costs only in-flight work.
3. **A self-re-arming watchdog** — a `send_later` / Routine firing into this session that checks liveness per run, resumes killed slices, batch-commits orphans, runs the persistence sweep (mechanics in `persistence.md` — embed the sweep instruction in the watchdog trigger's own prompt so it fires by machinery), posts a progress report, and schedules the next firing before it finishes.
4. **Cadence is 20 minutes.** Do not lengthen it without asking.
5. **`PushNotification` when he is away**, carrying counts and liveness only — "N/24 done, all slices alive" — never time estimates. He explicitly leaves you to work and waits on iOS notifications.
6. Re-arm the watchdog whenever you stop a swarm to edit it. A *disabled* watchdog left over from a stop leaves the next run unprotected — the worst persistence gap there is.
7. Record this architecture in `threads.md`; it is not obvious to a post-compaction reader.

The coordinator batch-commit sweep is a *backstop* only — workers self-commit as the primary mechanism (`delegation.md`). When the backstop fires, check `git log` before claiming anything about whether worker self-commits are working.

For heavy runs, the platform-native shape is Routine-fired batches — each firing a fresh session doing one batch, with zero dependence on container longevity.

- Order on recovery: commit finished orphans first (by name; never partials — a truncated file committed reads as done), re-arm the watchdog second, resume the run third — protection precedes relaunch so the resumed run is covered from its first second.
