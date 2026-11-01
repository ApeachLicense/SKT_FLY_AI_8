import { v4 as uuidv4 } from 'uuid';

export interface CommitNode {
  id: string;
  label: string;
  author: string;
  date: string;
  branch: string;
  parents: string[];
}

export interface GraphData {
  nodes: CommitNode[];
  edges: { source: string; target: string }[];
}

const AUTHORS = ['Alice', 'Bob', 'Charlie', 'Dave', 'Eve'];
const BRANCHES = ['master', 'develop', 'feature/auth', 'feature/ui', 'hotfix/login'];

export const generateMockData = (count: number): GraphData => {
  const nodes: CommitNode[] = [];
  const edges: { source: string; target: string }[] = [];
  
  // Track the tip (latest commit hash) for each branch
  const branchTips: Record<string, string | null> = {};
  BRANCHES.forEach(b => branchTips[b] = null);

  // Initial commit
  const rootId = uuidv4();
  const rootNode: CommitNode = {
    id: rootId,
    label: 'Initial commit',
    author: 'Alice',
    date: new Date().toISOString(),
    branch: 'master',
    parents: []
  };
  nodes.push(rootNode);
  branchTips['master'] = rootId;

  for (let i = 1; i < count; i++) {
    // Pick a random branch to work on
    const activeBranches = Object.keys(branchTips).filter(b => branchTips[b] !== null);
    if (activeBranches.length === 0) break; // Should not happen

    const currentBranch = activeBranches[Math.floor(Math.random() * activeBranches.length)];
    const parentId = branchTips[currentBranch]!;
    
    // Actions: 0=Commit, 1=Branch Output (if not exists), 2=Merge (if possible)
    const action = Math.random();
    
    const newId = uuidv4();
    const author = AUTHORS[Math.floor(Math.random() * AUTHORS.length)];
    
    let newNode: CommitNode = {
      id: newId,
      label: `Commit ${i}`,
      author,
      date: new Date().toISOString(),
      branch: currentBranch,
      parents: [parentId]
    };

    // Logic to simulate branching and merging
    // 10% chance to merge, 10% chance to switch branch, 80% linear commit
    
    if (action < 0.1 && activeBranches.length > 1) {
        // Merge: picked branch merges INTO another branch? 
        // Or merge another branch INTO picked branch.
        // Let's merge another random branch tip INTO currentBranch
        const otherBranch = activeBranches.find(b => b !== currentBranch && branchTips[b] !== null);
        if (otherBranch) {
            const otherTip = branchTips[otherBranch]!;
            newNode.parents.push(otherTip);
            newNode.label = `Merge ${otherBranch} into ${currentBranch}`;
            // The other branch tip stays where it is? usually merge commit moves current branch forward.
        }
        edges.push({ source: parentId, target: newId });
        newNode.parents.forEach(p => {
             if (p !== parentId) edges.push({ source: p, target: newId }); 
        });
        branchTips[currentBranch] = newId;

    } else if (action < 0.2) {
        // Create/Switch to a new branch from here? 
        // Pick a target branch that is currently empty or we want to switch to
        const targetBranch = BRANCHES[Math.floor(Math.random() * BRANCHES.length)];
        
        if (branchTips[targetBranch] === null) {
            // Start new branch
            newNode.branch = targetBranch;
            newNode.label = `Start branch ${targetBranch}`;
            branchTips[targetBranch] = newId;
            edges.push({ source: parentId, target: newId });
        } else {
             // Just a regular commit on current branch
             edges.push({ source: parentId, target: newId });
             branchTips[currentBranch] = newId;
        }
    } else {
        // Regular commit
        edges.push({ source: parentId, target: newId });
        branchTips[currentBranch] = newId;
    }

    nodes.push(newNode);
  }

  return { nodes, edges };
};
