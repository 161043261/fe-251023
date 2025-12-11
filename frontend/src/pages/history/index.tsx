import { useEffect, useState } from "react";
import styles from "./index.module.scss";
import type { IProblem } from "../../types";
import Problem from "../../components/problem";
import useRequest from "../../hooks/use-request";

export default function History() {
  const [history, setHistory] = useState<IProblem[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string>("Hello, World!");
  const makeRequest = useRequest();

  const fetchHistory = async () => {
    setIsLoading(true);
    setErrorMessage("");
    try {
      const { history: problemList } = await makeRequest<{
        history: IProblem[];
      }>("/history");
      setHistory(problemList);
    } catch (err) {
      setErrorMessage(err instanceof Error ? err.message : JSON.stringify(err));
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  if (isLoading) {
    return <div className={styles["loading-container"]}>Loading...</div>;
  }

  if (errorMessage) {
    return (
      <div className={styles["error-message"]}>
        <p>{errorMessage}</p>
        <button type="button" onClick={fetchHistory}>
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className={styles["history-container"]}>
      <h1>History</h1>
      {history.length === 0 ? (
        <p>No history.</p>
      ) : (
        <div className={styles["history-list"]}>
          {history.map((detail) => (
            <Problem problem={detail} key={detail.id} showTips />
          ))}
        </div>
      )}
    </div>
  );
}
