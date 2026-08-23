# Finance Tracker — Web Frontend

A Flask + HTML/CSS dashboard for the Personal Finance Analyzer, built so you can
click through a real UI (and screenshot it) instead of the command line.

## Run it

```
pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:5000 in your browser.

## Notes

- On first run, it seeds a few months of sample transactions and a budget
  under `data/` so the dashboard and charts aren't empty. Delete the `data/`
  folder (or edit the JSON files) to start fresh — the sample data is only
  there to make the first screenshots look good.
- Data is stored locally in `data/transactions.json` and `data/budgets.json`.
  This is a personal/local tool, not built for multi-user or production use.
- Pages: Dashboard, Add Transaction, Transactions (with filters), Budget
  (set + track), and Reports (category, budget, and trend charts).
