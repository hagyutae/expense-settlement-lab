import { useState } from "react";
import "./App.css";

const API = "http://127.0.0.1:8000/api/settle";

type Violation = { code: string; name: string; message: string };

type Judgement = {
  claim_id: string;
  employee_name: string;
  department: string;
  used_date: string;
  expense_type: string;
  amount: number | null;
  is_passed: boolean;
  violations: Violation[];
};

type Aggregation = { name: string; columns: string[]; rows: (string | number)[][] };

type Result = { judgements: Judgement[]; aggregations: Aggregation[] };

function won(value: number | null) {
  return value === null ? "" : value.toLocaleString("ko-KR");
}

export default function App() {
  const [result, setResult] = useState<Result | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function upload(file: File) {
    setBusy(true);
    setError(null);
    const body = new FormData();
    body.append("file", file);
    try {
      const response = await fetch(API, { method: "POST", body });
      if (!response.ok) {
        const detail = await response.json();
        throw new Error(detail.detail ?? response.statusText);
      }
      setResult(await response.json());
    } catch (e) {
      setResult(null);
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setBusy(false);
    }
  }

  const passed = result?.judgements.filter((j) => j.is_passed).length ?? 0;
  const rejected = (result?.judgements.length ?? 0) - passed;

  return (
    <main>
      <h1>경비 정산</h1>

      <label className="pick">
        청구 파일 선택
        <input
          type="file"
          accept=".csv,.md"
          onChange={(e) => e.target.files?.[0] && upload(e.target.files[0])}
        />
      </label>

      {busy && <p className="note">판정 중입니다.</p>}
      {error && <p className="error">{error}</p>}

      {result && (
        <>
          <p className="note">
            전체 {result.judgements.length}건 · 통과 {passed} · 반려 {rejected}
          </p>

          {result.aggregations.map((table) => (
            <section key={table.name}>
              <h2>{table.name}</h2>
              <table>
                <thead>
                  <tr>
                    {table.columns.map((c) => (
                      <th key={c}>{c}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {table.rows.map((row) => (
                    <tr key={String(row[0])}>
                      {row.map((cell, i) => (
                        <td key={i} className={i === 0 ? "" : "num"}>
                          {typeof cell === "number" ? cell.toLocaleString("ko-KR") : cell}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </section>
          ))}

          <section>
            <h2>판정</h2>
            <table>
              <thead>
                <tr>
                  <th>청구ID</th>
                  <th>성명</th>
                  <th>사용일자</th>
                  <th>계정과목</th>
                  <th>금액</th>
                  <th>판정</th>
                  <th>위반</th>
                </tr>
              </thead>
              <tbody>
                {result.judgements.map((j) => (
                  <tr key={j.claim_id}>
                    <td>{j.claim_id}</td>
                    <td>{j.employee_name}</td>
                    <td>{j.used_date}</td>
                    <td>{j.expense_type}</td>
                    <td className="num">{won(j.amount)}</td>
                    <td className={j.is_passed ? "pass" : "reject"}>
                      {j.is_passed ? "통과" : "반려"}
                    </td>
                    <td>{j.violations.map((v) => v.code).join(" ")}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </section>
        </>
      )}
    </main>
  );
}
