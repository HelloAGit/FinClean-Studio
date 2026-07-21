# FinClean Studio

FinClean Studio is a web-based financial data quality workbench that **identifies, explains and corrects inconsistent or unclean financial data** before it is used for reporting, forecasting, auditing or business intelligence.

## Core value proposition

1. Upload a financial dataset (CSV or Excel).
2. Review detected data-quality problems and proposed corrections.
3. Approve, reject or modify each correction.
4. Export a validated dataset with a complete audit trail and reconciliation summary.

The original uploaded file is **immutable**. FinClean Studio always creates a new cleaned version and a machine-readable cleaning recipe.

## Target users

- Financial analysts and accountants  
- SMEs without dedicated data-engineering teams  
- Audit and advisory firms  
- NGOs and development organisations  
- Banks and fintech companies  
- Finance departments consolidating data from multiple offices or countries  

## Core workflow

1. **Upload dataset** (CSV/Excel).
2. **Select dataset type**: bank transactions, general ledger, AP, AR, budget data, etc.
3. **Profile dataset**:
   - Rows, columns, data types
   - Missing-value percentages
   - Unique/duplicate values
   - Amount statistics (min, max, average)
   - Date ranges
   - Currency and number formats
   - Potentially sensitive columns
   - Overall data-quality score
4. **Map columns** to a standard financial schema.
5. **Run validation rules** (deterministic, explainable).
6. **Review corrections** (before/after, reason, confidence, decision).
7. **Approve/reject/modify** corrections.
8. **Export package**:
   - Cleaned CSV/Excel
   - Data-quality report
   - Rejected-record file
   - Transformation log
   - Machine-readable cleaning recipe
   - Reconciliation summary

## Problems detected (MVP)

- Inconsistent dates  
- Invalid monetary values  
- Duplicate transactions  
- Missing required values  
- Inconsistent account codes  
- Debit/credit errors  
- Inconsistent supplier names  
- Blank and malformed rows  
- Mixed currencies  
- Reconciliation failures  

## Tech stack (MVP)

- **Backend**: Python, FastAPI, Pandas  
- **Frontend**: React + TypeScript + Vite  
- **Storage**: Local filesystem (for MVP), pluggable for cloud later  

## Development

```bash
# Backend
cd backend
uvicorn app:app --reload

# Frontend
cd frontend
npm install
npm run dev
