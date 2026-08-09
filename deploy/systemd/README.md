# Ubuntu service deployment

The repository includes `zelda.service` as a systemd template service.

## Environment

Create the local environment file at `~/.config/zelda/zelda.env`. Do not commit secrets.

Example:

```text
ZELDA_AI_PROVIDER=rules
ZELDA_HOST=127.0.0.1
ZELDA_PORT=8765
```

## Install

Copy the unit into the user's systemd directory, reload systemd, enable it, and start it.

```bash
mkdir -p ~/.config/zelda ~/.config/systemd/user
cp deploy/systemd/zelda.service ~/.config/systemd/user/zelda.service
systemctl --user daemon-reload
systemctl --user enable --now zelda.service
systemctl --user status zelda.service
```

For a public deployment, terminate TLS at a reverse proxy and keep the Z.E.L.D.A. daemon bound to a trusted interface unless direct WSS exposure is intentionally configured.
