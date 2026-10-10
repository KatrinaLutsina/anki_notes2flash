# Personal computer setup

## Ready-to-install add-on

1. Copy `output/notes2flash.ankiaddon` to the personal computer.
2. In Anki, open **Tools → Add-ons → Install from file** and select it.
3. Restart Anki.
4. Open **Tools → Add-ons → Notes2Flash → Config** and enter newly created personal credentials:
   - `openrouter_api_key`
   - `notion_api_key`
5. Share the required Notion pages with the personal Notion integration.

The package deliberately contains no API keys, logs, document URLs, user inputs, or tracking state.

## Tracking state and Anki sync

`tracked_docs.json` is not included. The first run on the new computer therefore treats a document as new. If the same cards already arrived through Anki sync, processing the same document again may create duplicates.

If continuity is required, copy `tracked_docs.json` privately from the installed add-on directory after installation. Never commit it or add it to a public archive: it can contain source URLs and document-processing state.

## Build from source

```bash
docker compose up --build
```

The generated file is `output/notes2flash.ankiaddon`.

The custom Mandarin workflow is included as `addon/workflow_configs/mandarin_vocab_extraction_workflow_config.yml`. Both it and the general workflow wait 10 seconds between chunks to reduce free-model rate-limit failures.

## Publish a personal fork

Authenticate GitHub CLI on the personal account, create the fork, and push the changes from this repository:

```bash
gh auth login -h github.com
gh repo fork Colmmm/notes2flash --remote --remote-name fork
git push -u fork HEAD
```

Keep `docs/LICENSE`; the upstream project is distributed under AGPL-3.0. Configure all credentials only inside Anki on the target computer.
