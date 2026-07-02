# Runtime Node Scheduling

Generated agents include `runtime_node.py`, a one-shot command for personal always-on runtime nodes.

The runtime node is intentionally simple during MVP:

```bash
python runtime_node.py
```

It runs generated-agent health checks, optionally runs the report, counts notification inbox events, and appends `.setup_os/runtime_node.jsonl`.

Use a scheduler to run it on a Mac mini, home server, spare laptop, NAS, mini PC, or private VPS.

## Before Scheduling

From the generated agent directory:

```bash
python health.py
python report.py
python runtime_node.py
```

Confirm:

- `health.py` passes
- `report.py` produces the expected report
- `.setup_os/runtime_node.jsonl` is appended
- `.setup_os/notifications.jsonl` contains expected alerts

## macOS launchd

Create `~/Library/LaunchAgents/com.setupos.portfolio-runtime.plist`.

Replace paths with the generated agent directory and Python executable for your machine.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.setupos.portfolio-runtime</string>

  <key>WorkingDirectory</key>
  <string>/Users/YOU/Setup OS/generated/desktop-portfolio-os</string>

  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/python3</string>
    <string>runtime_node.py</string>
  </array>

  <key>StartInterval</key>
  <integer>3600</integer>

  <key>StandardOutPath</key>
  <string>/tmp/setup-os-portfolio-runtime.out.log</string>

  <key>StandardErrorPath</key>
  <string>/tmp/setup-os-portfolio-runtime.err.log</string>
</dict>
</plist>
```

Load it:

```bash
launchctl load ~/Library/LaunchAgents/com.setupos.portfolio-runtime.plist
launchctl start com.setupos.portfolio-runtime
```

Unload it:

```bash
launchctl unload ~/Library/LaunchAgents/com.setupos.portfolio-runtime.plist
```

## Windows Task Scheduler

Create a basic task:

1. Open Task Scheduler.
2. Create Basic Task.
3. Trigger: daily, hourly, or on logon.
4. Action: Start a program.
5. Program/script: path to `python.exe`.
6. Add arguments: `runtime_node.py`.
7. Start in: generated Portfolio OS directory.

Example:

```text
Program/script:
C:\Users\YOU\AppData\Local\Programs\Python\Python312\python.exe

Add arguments:
runtime_node.py

Start in:
C:\Users\YOU\Setup OS\generated\desktop-portfolio-os
```

## Linux cron

Example hourly cron entry:

```cron
0 * * * * cd "/home/YOU/setup-os/generated/desktop-portfolio-os" && /usr/bin/python3 runtime_node.py >> /tmp/setup-os-runtime.log 2>&1
```

## Current Limits

- This is a one-shot scheduled runner, not a daemon.
- Phone push still depends on local inbox plus configured push adapters such as ntfy.
- No quiet-hours policy is enforced yet.
- No remote health dashboard exists yet.
- Secrets and connector credentials are still out of scope for local CSV MVP.
