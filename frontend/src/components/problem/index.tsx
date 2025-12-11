import { useState } from "react";
import styles from "./index.module.scss";
import type { IProblem } from "../../types";

interface IProps {
  problem: IProblem;
  showTips?: boolean;
}

export default function Problem(props: IProps) {
  const {
    problem: { answerId, description, level, options: rawOptions, solution },
    showTips: showTipsInitialVal = false,
  } = props;

  const options = Array.isArray(rawOptions)
    ? rawOptions
    : (JSON.parse(rawOptions) as string[]);

  const [selectedIdx, setSelectedIdx] = useState<number>(-1);
  const [showTips, setShowTips] = useState<boolean>(showTipsInitialVal);

  const handleSelectOption = (optionIdx: number) => {
    setSelectedIdx(optionIdx);
    setShowTips(true);
  };

  const getOptionClassnames = (optionIdx: number) => {
    if (selectedIdx !== optionIdx) {
      return styles["option-item"];
    }
    if (optionIdx === answerId) {
      return `${styles["option-item"]} ${styles["option-correct"]}`;
    } else {
      return `${styles["option-item"]} ${styles["option-wrong"]}`;
    }
  };

  return (
    <div className={styles["problem-container"]}>
      <p>
        <strong>Level</strong>: {level[0].toUpperCase() + level.slice(1)}
      </p>

      <p className={styles["problem-description"]}>{description}</p>

      <div className={styles["options-container"]}>
        {options.map((option, idx) => (
          <div
            key={idx}
            className={getOptionClassnames(idx)}
            onClick={() => {
              handleSelectOption(idx);
            }}
          >
            {option}
          </div>
        ))}
      </div>

      {showTips && selectedIdx !== -1 && (
        <div className={styles["solution-container"]}>
          <h1>Solution</h1>
          {solution}
        </div>
      )}
    </div>
  );
}
