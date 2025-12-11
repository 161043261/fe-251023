import { useEffect, useState, type ChangeEvent } from "react";
import styles from "./index.module.scss";
import Problem from "../../components/problem";
import type { IProblem, IQuota, TLevel } from "../../types";
import useRequest from "../../hooks/use-request";

export default function Home() {
  const [problem, setProblem] = useState<IProblem>({
    id: 0,
    description: "Description of the default problem",
    answerId: 2,
    level: "easy",
    options: [
      "A: default option 0",
      "B: default option 1",
      "C: default option 2",
      "D: default option 3",
    ],
    solution: "Solution to the default problem",
  });

  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string>("");
  const [level, setLevel] = useState<TLevel>("easy");
  const [quota, setQuota] = useState<IQuota>();
  const makeRequest = useRequest();

  const fetchQuota = async () => {
    try {
      const res = await makeRequest<IQuota>("/quota");
      setQuota(res);
    } catch (err) {
      console.log(err);
    }
  };
  const generateProblem = async () => {
    setIsLoading(true);
    setErrorMessage("");
    try {
      const res = await makeRequest<IProblem>(
        "/generate/problem", // endpoint
        "POST", // method
        { level }, // body
      );
      setProblem(res);
      fetchQuota();
    } catch (err) {
      setErrorMessage(err instanceof Error ? err.message : JSON.stringify(err));
    } finally {
      setIsLoading(false);
    }
  };

  const getNextResetDate = () => {
    if (!quota?.lastResetDate) {
      return "Unknown date";
    }
    const resetDate = new Date(quota.lastResetDate);
    resetDate.setDate(resetDate.getDate() + 1);
    return resetDate.toLocaleString();
  };

  const handleLevelChange = (e: ChangeEvent<HTMLSelectElement>) => {
    setLevel(e.target.value as TLevel);
  };

  useEffect(() => {
    fetchQuota();
  }, []);

  return (
    <div className={styles["home-container"]}>
      <h2>Coding Problem Generator</h2>
      <div className={styles["quota-container"]}>
        <p>Quota remain: {quota?.remain ?? 0}</p>
        {quota?.remain !== 0 && <p>Next reset time: {getNextResetDate()}</p>}
      </div>

      <div className={styles["level-container"]}>
        <label htmlFor="level-selector">Select level</label>
        <select
          id="level-selector"
          value={level}
          onChange={handleLevelChange}
          disabled={isLoading}
        >
          <option value="easy">Easy</option>
          <option value="medium">Medium</option>
          <option value="hard">Hard</option>
        </select>
      </div>

      <button
        type="button"
        onClick={generateProblem}
        disabled={isLoading || quota?.remain === 0}
        className={styles["generate-button"]}
      >
        {isLoading ? "Generating..." : "Generate a coding problem"}
      </button>

      <Problem problem={problem} />

      {errorMessage && (
        <div className={styles["error-message"]}>
          <p>{errorMessage}</p>
        </div>
      )}
    </div>
  );
}
