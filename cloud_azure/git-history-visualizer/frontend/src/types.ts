export interface CommitNode {
  id: string;
  label: string;
  author: string;
  date: string;
  parents: string[];
  branch?: string; // Optional for now, backend parser needs enhancement to determine branch name robustly
}

export interface Edge {
  source: string;
  target: string;
}

export interface GraphData {
  nodes: CommitNode[];
  edges: Edge[];
}
