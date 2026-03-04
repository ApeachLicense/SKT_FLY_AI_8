import React, { useEffect, useRef } from 'react';
import { Network } from 'vis-network';
import { DataSet } from 'vis-data';
import { GraphData } from '../types';

interface Props {
  data: GraphData;
}

const VisGraph: React.FC<Props> = ({ data }) => {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    const nodes = new DataSet(
      data.nodes.map((n, i) => ({
        id: n.id,
        label: n.label.length > 10 ? n.label.substring(0, 10)+'...' : n.label,
        group: n.branch,
        // Optional: Pre-calculate position if physics is off
        // x: branchIndex * 100, y: i * 100
      }))
    );

    const edges = new DataSet(
      data.edges.map(e => ({
        from: e.source,
        to: e.target,
        arrows: 'to'
      }))
    );

    const options = {
      layout: {
        hierarchical: {
          direction: 'UD',
          sortMethod: 'hubsize', // or 'directed'
          nodeSpacing: 150,
          levelSeparation: 100
        }
      },
      physics: {
        enabled: false // Better performance for large graphs
      },
      nodes: {
        shape: 'box'
      }
    };

    const network = new Network(containerRef.current, { nodes, edges }, options);

    return () => {
      network.destroy();
    };
  }, [data]);

  return (
    <div ref={containerRef} style={{ height: '100%', width: '100%', border: '1px solid #ddd' }} />
  );
};

export default VisGraph;
