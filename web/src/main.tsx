import { StrictMode, useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import './style.css';

type Capabilities = {
  schema_version: string;
  stage: string;
  version: string;
  runtime_connected: boolean;
  creation_enabled: boolean;
  persistence_enabled: boolean;
};

function App() {
  const [api, setApi] = useState<Capabilities | null>(null);
  const [status, setStatus] = useState('正在连接 API…');

  useEffect(() => {
    let active = true;
    const controller = new AbortController();
    const timer = window.setTimeout(() => controller.abort(), 8000);
    async function connect() {
      try {
        const response = await fetch('/api/v1/capabilities', { signal: controller.signal });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data: unknown = await response.json();
        if (!isCapabilities(data)) throw new Error('Unexpected capabilities schema');
        if (active) {
          setApi(data);
          setStatus('API 已连接');
        }
      } catch {
        if (active) setStatus('API 未连接，请启动本机服务后刷新');
      } finally {
        window.clearTimeout(timer);
      }
    }
    void connect();
    return () => { active = false; window.clearTimeout(timer); controller.abort(); };
  }, []);

  return (
    <div className="workbench">
      <aside className="navigation">
        <a className="brand" href="/">◈ <span>创作工作台</span></a>
        <div className="section-label">我的空间</div>
        <div className="active-nav">项目概览</div>
        <p className="muted">把灵感、资料与作品<br />放进同一个创作空间。</p>
        <div className="nav-bottom">开发预览 · B00</div>
      </aside>
      <main>
        <header><span>工作空间 / 开始创作</span><span className="badge">初始化</span></header>
        <section className="welcome">
          <span className="eyebrow">从一个想法开始</span>
          <h1>让灵感，成为作品。</h1>
          <p>围绕一份资料，写文章、做演示、讲一个更完整的故事。</p>
          <div className="formats">
            {['文章', '图片', '信息图', '演示文稿', '视频', '数据分析'].map((name, index) => (
              <div className="format" key={name}><span className="format-index">0{index + 1}</span>
                <strong>{name}</strong><span className="muted">待接入</span></div>
            ))}
          </div>
          <div className="composer">
            <label htmlFor="prompt">你想创作什么？</label>
            <textarea id="prompt" disabled placeholder="模型接入后，在这里描述你的创作想法…" />
            <div className="composer-footer"><span>创作能力将在模型接入验证后开放</span>
              <button disabled>开始创作 ↑</button></div>
          </div>
        </section>
        <footer role="status">{status}{api ? ` · ${api.version}` : ''}</footer>
      </main>
      <aside className="workspace-panel">
        <h2>作品工作区</h2>
        <div className="empty-artifact"><span className="artifact-icon">▤</span>
          <h3>作品将在这里展开</h3><p>预览、选中内容、提出修改，<br />保留每一个创作版本。</p></div>
        <div className="connection"><span className="status-dot" />
          {api?.runtime_connected ? 'Runtime 已连接' : '模型尚未接入'}</div>
        <p className="panel-note">当前为项目起始页，尚不提供生成、编辑或保存功能。</p>
      </aside>
    </div>
  );
}

function isCapabilities(value: unknown): value is Capabilities {
  if (typeof value !== 'object' || value === null) return false;
  const data = value as Record<string, unknown>;
  return data.schema_version === '1' && typeof data.stage === 'string'
    && typeof data.version === 'string' && typeof data.runtime_connected === 'boolean'
    && typeof data.creation_enabled === 'boolean' && typeof data.persistence_enabled === 'boolean';
}

createRoot(document.getElementById('root')!).render(<StrictMode><App /></StrictMode>);
