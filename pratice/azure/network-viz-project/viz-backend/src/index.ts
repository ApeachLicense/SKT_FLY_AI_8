import express from 'express';
import cors from 'cors';
import { getGitLog } from './gitService';
import path from 'path';

const app = express();
const PORT = 3000;

app.use(cors());
app.use(express.json());

// Target repo path (default to current working directory where server is started, 
// usually root of project in this context, or passed via env)
const REPO_PATH = process.env.REPO_PATH || path.resolve(__dirname, '../../'); 
// Assuming viz-backend is in root/viz-backend, so ../../ is root.

app.get('/api/log', async (req, res) => {
  try {
    console.log(`Fetching git log for ${REPO_PATH}`);
    const data = await getGitLog(REPO_PATH);
    res.json(data);
  } catch (error: any) {
    console.error('Error fetching git log:', error);
    res.status(500).json({ error: error.message });
  }
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
  console.log(`Monitoring repo at: ${REPO_PATH}`);
});
