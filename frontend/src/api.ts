import { DatasetType, Correction } from "./types";

const BASE_URL = "http://localhost:8000";

export async function uploadDataset(
  file: File,
  datasetType: DatasetType
): Promise<any> {
  const form = new FormData();
  form.append("file", file);
  form.append("dataset_type", datasetType);
  const res = await fetch(`${BASE_URL}/upload`, {
    method: "POST",
    body: form,
  });
  return res.json();
}

export async function runRules(datasetId: string, templateName: string) {
  const res = await fetch(
    `${BASE_URL}/rules/apply/${datasetId}?template_name=${templateName}`,
    { method: "POST" }
  );
  return res.json();
}

export async function submitDecisions(
  datasetId: string,
  corrections: Correction[],
  user: string
) {
  const payload = corrections.map((c) => ({
    row_index: c.row_index,
    field: c.field,
    decision: c.decision,
    modified_value: c.decision === "modify" ? c.proposed_value : null,
    user,
    reason: c.decision === "modify" ? "Manual override" : null,
  }));
  const res = await fetch(`${BASE_URL}/corrections/decide/${datasetId}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return res.json();
}
