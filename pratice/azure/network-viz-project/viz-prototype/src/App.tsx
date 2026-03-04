import { useState, useEffect } from 'react';
import VisGraph from './components/VisGraph';
// import FlowGraph from './components/FlowGraph'; // Disabled for MVP
import { GraphData } from './types';
import './App.css';

function App() {
  const [data, setData] = useState<GraphData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch('http://localhost:3000/api/log');
      if (!res.ok) {
        throw new Error(`Failed to fetch: ${res.statusText}`);
      }
      const json: GraphData = await res.json();
      
      // Post-processing to add branch info mock or infer it if missing
      // (The simple parser might not provide branch names for all commits yet)
      const nodesWithBranch = json.nodes.map(n => ({
        ...n,
        branch: n.branch || 'unknown' // Default to unknown if not strictly parsed
      }));

      setData({ ...json, nodes: nodesWithBranch });
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
      <div style={{ padding: 10, borderBottom: '1px solid #ccc', background: '#f0f0f0', display: 'flex', gap: 10, alignItems: 'center' }}>
        <h2>Task Master Git Viz (MVP)</h2>
        <button onClick={fetchData} disabled={loading}>
          {loading ? 'Refreshing...' : 'Refresh Log'}
        </button>
        {error && <span style={{ color: 'red' }}>Error: {error}</span>}
        {data && <span>Loaded {data.nodes.length} commits.</span>}
      </div>

      <div style={{ flex: 1, position: 'relative' }}>
          {loading && <div style={{ padding: 20 }}>Loading...</div>}
          {!loading && data && (
              <VisGraph data={data} key={data.nodes.length} />
          )}
      </div>
    </div>
  );
}

export default App;
