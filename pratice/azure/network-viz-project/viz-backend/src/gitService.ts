import { spawn } from 'child_process';
import path from 'path';

export interface CommitNode {
  id: string;
  label: string;
  author: string;
  date: string;
  parents: string[];
}

export interface Edge {
  source: string;
  target: string;
}

export interface GraphData {
  nodes: CommitNode[];
  edges: Edge[];
}

export const getGitLog = (repoPath: string): Promise<GraphData> => {
  return new Promise((resolve, reject) => {
    // Format: Hash | ParentHashes | AuthorName | Date | Subject
    const gitProcess = spawn('git', [
      'log',
      '--pretty=format:%H|%p|%an|%ad|%s',
      '--date=iso',
      '--all' // Include all branches
    ], { cwd: repoPath });

    let stdoutData = '';
    let stderrData = '';

    gitProcess.stdout.on('data', (data) => {
      stdoutData += data.toString();
    });

    gitProcess.stderr.on('data', (data) => {
      stderrData += data.toString();
    });

    gitProcess.on('close', (code) => {
      if (code !== 0) {
        return reject(new Error(`Git process exited with code ${code}: ${stderrData}`));
      }

      const nodes: CommitNode[] = [];
      const edges: Edge[] = [];

      const lines = stdoutData.split('\n');
      
      lines.forEach((line) => {
        if (!line.trim()) return;
        
        const [hash, parentsString, author, date, subject] = line.split('|');
        const parents = parentsString ? parentsString.split(' ') : [];

        nodes.push({
          id: hash,
          label: subject,
          author,
          date,
          parents
        });

        parents.forEach(parentHash => {
          edges.push({
            source: parentHash,
            target: hash
          });
        });
      });

      resolve({ nodes, edges });
    });
  });
};
