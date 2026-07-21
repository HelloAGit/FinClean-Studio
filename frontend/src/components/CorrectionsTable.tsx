import React from "react";
import { Correction } from "../types";

interface Props {
  corrections: Correction[];
  onChange: (updated: Correction[]) => void;
}

export const CorrectionsTable: React.FC<Props> = ({
  corrections,
  onChange,
}) => {
  const updateDecision = (
    index: number,
    decision: "approve" | "reject" | "modify"
  ) => {
    const next = [...corrections];
    next[index] = { ...next[index], decision };
    onChange(next);
  };

  const updateProposedValue = (index: number, value: string) => {
    const next = [...corrections];
    next[index] = { ...next[index], proposed_value: value };
    onChange(next);
  };

  return (
    <table className="fc-table">
      <thead>
        <tr>
          <th>Row</th>
          <th>Field</th>
          <th>Original value</th>
          <th>Proposed value</th>
          <th>Reason</th>
          <th>Confidence</th>
          <th>Decision</th>
        </tr>
      </thead>
      <tbody>
        {corrections.map((c, i) => (
          <tr key={`${c.row_index}-${c.field}`}>
            <td>{c.row_index}</td>
            <td>{c.field}</td>
            <td>{c.original_value}</td>
            <td>
              <input
                value={c.proposed_value ?? ""}
                onChange={(e) => updateProposedValue(i, e.target.value)}
              />
            </td>
            <td>{c.reason}</td>
            <td>{Math.round(c.confidence * 100)}%</td>
            <td>
              <select
                value={c.decision ?? ""}
                onChange={(e) =>
                  updateDecision(
                    i,
                    e.target.value as "approve" | "reject" | "modify"
                  )
                }
              >
                <option value="">Select</option>
                <option value="approve">Approve</option>
                <option value="reject">Reject</option>
                <option value="modify">Modify</option>
              </select>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};
