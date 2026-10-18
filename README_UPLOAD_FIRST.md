# Alpha Radar V19.8.1 - safe Cloud startup and restartable factor laboratory

DEPLOYMENT: Install extracted source files into the GitHub project root,
replacing files with matching names; Streamlit main module is app.py. Keep
private data/, SQLite, the deployed Secrets and FINMIND_TOKEN unchanged.
The ZIP contains exactly 100 root files. The retired single-purpose
review_indicators_v1961.py is preserved in legacy_release_notes.zip.

IMPORTANT: App now starts in SAFE MODE by default. First open the URL and
confirm the lightweight startup page appears. Then click Open complete
dashboard. If the full dashboard fails, the error ID will remain visible;
open Manage app > Logs and search ALPHARADAR_BOOT_ERROR. This is a diagnostic
containment change, NOT proof that a previously unseen Cloud crash was fixed.
The underlying V19.8 factors, history, ranking, costs and adoption rules
have NOT been changed by this Cloud repair.

Research optimisation is a separate offline CLI (do not run indefinitely
inside a Streamlit Cloud free-tier web worker). Requirements for the CLI
are already covered by requirements.txt. The same exposed-price report can
be downloaded from the previous V19.8 Research Results archive.

Step 1 - explore with no fixed number-of-rounds cap (time and plateau limits
still apply, and the checkpoint is persisted after every round):

  python research_lab.py --bundle AlphaRadar_V19_8_Research_Results.zip --output lab1981 --rounds 0 --max-minutes 20 --patience 12 --batch 12

Step 2 - if interrupted, continue the deterministic, identical protocol:

  python research_lab.py --bundle AlphaRadar_V19_8_Research_Results.zip --output lab1981 --rounds 0 --max-minutes 20 --patience 12 --batch 12 --resume

Step 3 - ONE-TIME final audit and seal, with no more tuning on those dates:

  python research_lab.py --bundle AlphaRadar_V19_8_Research_Results.zip --output lab1981 --resume --batch 12 --finalize

Step 4 - after truly NEW point-in-time history arrives, compare the frozen
weights without refitting them on new outcomes:

  python research_lab.py --bundle UPDATED_NEW_RESEARCH_BUNDLE.zip --output forward1981 --frozen-model lab1981/frozen_models.json --fresh-after 2026-10-15

Use exactly the same data/feature/seed/batch configuration for search and
seal. To start another research experiment use a new output folder. A sealed
experiment cannot resume tuning. A different ZIP/algorithm/factor bank cannot
silently reuse the checkpoint.

The CLI evaluates every historically available common signal date, rather
than the original UI's 100 sampled cutoffs. Dates and holding windows can
overlap, so they are NOT independent trials. At most four independently
selected scoring inputs are searched; a deleted factor stays at zero.
Historical date order is preserved and an h-session purge separates tuning
from the held-out segment. Existing Yahoo/FinMind data and sample composition
have already been inspected repeatedly: research-only, NOT a new blind test.
Default candidate bank is technical only. Optional financial/ownership
signals are OFF by default and require PIT provenance to interpret responsibly.

A large dataset, long-running compute, memory availability and consistent
persistence cannot be guaranteed on Streamlit Community Cloud. For long
experiments run the CLI on a local machine or a persistent CI/compute runner.
No amount of backtesting guarantees convergence to a profitable model.
Neither the safety wrapper nor the research CLI automatically submits orders
or upgrades the web app's V19.8 production rankings.
