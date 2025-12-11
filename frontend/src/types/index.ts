export type TLevel = "easy" | "medium" | "hard";

export interface IProblem {
  id: number;
  answerId: number;
  description: string;
  level: TLevel;
  options: string[] | string;
  solution: string;
}

export interface IQuota {
  remain: number;
  lastResetDate: number;
}
