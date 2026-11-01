import React, { useMemo } from 'react';
import ReactFlow, { 
  Background, 
  Controls, 
  Node, 
  Edge,
  ConnectionLineType,
  MarkerType
} from 'reactflow';
import 'reactflow/dist/style.css';
import { GraphData } from '../utils/mockData';

interface Props {
  data: GraphData;
}

const FlowGraph: React.FC<Props> = ({ data }) => {
  const { nodes: commitNodes, edges: commitEdges } = data;

  const { nodes, edges } = useMemo(() => {
    // Basic Layout Calculation
    // X axis: Branch index
    // Y axis: Time (index in array)
    
    // Map branch names to X coordinates
    const branches = Array.from(new Set(commitNodes.map(n => n.branch)));
    const branchX = new Map(branches.map((b, i) => [b, i * 150]));

    const flowNodes: Node[] = commitNodes.map((node, i) => ({
      id: node.id,
      position: { x: branchX.get(node.branch) || 0, y: i * 80 },
      data: { label: `${node.branch}\n${node.label}` },
      style: { 
        width: 140, 
        fontSize: 10, 
        background: '#fff', 
        border: '1px solid #777', 
        borderRadius: 5,
        textAlign: 'center'
      }
    }));

    const flowEdges: Edge[] = commitEdges.map((edge) => ({
      id: `${edge.source}-${edge.target}`,
      source: edge.source,
      target: edge.target,
      type: ConnectionLineType.SmoothStep,
      markerEnd: { type: MarkerType.ArrowClosed },
      animated: false
    }));

    return { nodes: flowNodes, edges: flowEdges };
  }, [commitNodes, commitEdges]);

  return (
    <div style={{ height: '100%', width: '100%', border: '1px solid #ddd' }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        fitView
      >
        <Background />
        <Controls />
      </ReactFlow>
    </div>
  );
};

export default FlowGraph;
