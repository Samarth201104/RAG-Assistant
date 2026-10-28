'use client';

import { useEffect, useRef, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import {
  Activity, ArrowRight, BookOpen, Check, FileImage, FileText, Files,
  GraduationCap, LayoutDashboard, Menu, MessageSquareText, Moon, Plus,
  Search, Send, Sparkles, Sun, Trash2, Upload, X, Scale,
} from 'lucide-react';
import { api, type ChatResult, type Citation } from '@/lib/api';

type Section = 'Overview' | 'Documents' | 'Research chat' | 'Semantic search' | 'Summarize' | 'Compare' | 'Study notes';
type Message = { role: 'user' | 'assistant'; text: string; citations?: Citation[] };
type SearchResult = { content: string; metadata: Record<string, unknown> };

const navigation: { name: Section; icon: typeof LayoutDashboard; group: string }[] = [
  { name: 'Overview', icon: LayoutDashboard, group: 'Workspace' },
  { name: 'Documents', icon: Files, group: 'Workspace' },
  { name: 'Research chat', icon: MessageSquareText, group: 'Research' },
  { name: 'Semantic search', icon: Search, group: 'Research' },
  { name: 'Summarize', icon: FileText, group: 'Create' },
  { name: 'Compare', icon: Scale, group: 'Create' },
  { name: 'Study notes', icon: GraduationCap, group: 'Create' },
];

const tools: [Section, string, string][] = [
  ['Research chat', 'Ask your library', 'Get cited answers grounded in your documents.'],
  ['Semantic search', 'Find a passage', 'Search by meaning across your indexed research.'],
  ['Summarize', 'Create a summary', 'Surface the core argument and key findings.'],
  ['Compare', 'Compare papers', 'Understand where two studies align or diverge.'],
  ['Study notes', 'Build study notes', 'Turn a paper into a focused learning guide.'],
];

function outputText(value: unknown): string {
  if (typeof value === 'string') return value;
  if (!value || typeof value !== 'object') return String(value ?? '');
  return Object.entries(value as Record<string, unknown>)
    .map(([key, item]) => `## ${key.replaceAll('_', ' ')}\n\n${typeof item === 'string' ? item : JSON.stringify(item, null, 2)}`)
    .join('\n\n');
}

export default function Home() {
  const [section, setSection] = useState<Section>('Overview');
  const [documents, setDocuments] = useState<string[]>([]);
  const [apiOnline, setApiOnline] = useState<boolean | null>(null);
  const [dark, setDark] = useState(false);
  const [mobileMenu, setMobileMenu] = useState(false);
  const [query, setQuery] = useState('');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [results, setResults] = useState<SearchResult[]>([]);
  const [output, setOutput] = useState('');
  const [selected, setSelected] = useState('');
  const [second, setSecond] = useState('');
  const [noteType, setNoteType] = useState('detailed');
  const [dragging, setDragging] = useState(false);
  const fileInput = useRef<HTMLInputElement>(null);
  const feed = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setDark(localStorage.getItem('atlas-theme') === 'dark');
    api.health().then(() => setApiOnline(true)).catch(() => setApiOnline(false));
    void refreshDocuments().catch(reason => {
      setError(reason instanceof Error ? reason.message : 'Unable to load indexed documents.');
    });
  }, []);

  useEffect(() => {
    document.documentElement.dataset.theme = dark ? 'dark' : 'light';
    localStorage.setItem('atlas-theme', dark ? 'dark' : 'light');
  }, [dark]);

  useEffect(() => {
    feed.current?.scrollTo({ top: feed.current.scrollHeight, behavior: 'smooth' });
  }, [messages, busy]);

  async function refreshDocuments() {
    const files = await api.documents();
    setDocuments(files);
    setSelected(current => current || files[0] || '');
    setSecond(current => current || files[1] || '');
  }

  async function run<T>(operation: () => Promise<T>, done: (value: T) => void) {
    setBusy(true);
    setError('');
    try { done(await operation()); }
    catch (reason) { setError(reason instanceof Error ? reason.message : 'Unable to complete the request. Please try again.'); }
    finally { setBusy(false); }
  }

  function askQuestion() {
    const question = query.trim();
    if (!question || busy) return;
    setMessages(current => [...current, { role: 'user', text: question }]);
    setQuery('');
    void run(() => api.ask(question), result => {
      const response = (result as { response?: ChatResult }).response;
      setMessages(current => [...current, {
        role: 'assistant',
        text: response?.answer || 'The service returned an empty answer.',
        citations: response?.citations || [],
      }]);
    });
  }

  async function uploadFiles(fileList: FileList | null) {
    if (!fileList?.length) return;
    const files = Array.from(fileList);
    const supported = /\.(pdf|png|jpe?g|bmp|tiff)$/i;
    if (files.some(file => !supported.test(file.name))) {
      setError('Choose PDF, PNG, JPG, JPEG, BMP, or TIFF files.');
      return;
    }
    setBusy(true);
    setError('');
    try { await api.upload(files); await refreshDocuments(); }
    catch (reason) { setError(reason instanceof Error ? reason.message : 'Upload failed.'); }
    finally { setBusy(false); if (fileInput.current) fileInput.current.value = ''; }
  }

  function generate() {
    if (!selected) return;
    const operation = section === 'Summarize'
      ? () => api.summarize(selected)
      : section === 'Compare'
        ? () => api.compare(selected, second)
        : () => api.notes(selected, noteType);
    void run(operation, response => setOutput(outputText((response as { response?: unknown }).response)));
  }

  function searchDocuments() {
    if (!query.trim()) return;
    void run(() => api.search(query), response => {
      setResults((response as { response?: { documents?: SearchResult[] } }).response?.documents || []);
    });
  }

  function renderOverview() {
    return <>
      <div className="welcome">
        <div>
          <div className="eyebrow"><i /> YOUR AI RESEARCH WORKSPACE</div>
          <h1>Good research starts<br />with a better question.</h1>
          <p>Bring your papers together. Find the signal, follow the sources, and move your thinking forward.</p>
          <button className="button primary" onClick={() => setSection('Research chat')}><Sparkles size={16} /> Ask your documents <ArrowRight size={15} /></button>
        </div>
        <div className="hero-art" aria-hidden="true">
          <div className="orb" /><div className="hero-core"><Sparkles size={24} /></div>
          <div className="float-card fa"><FileText size={15} /> Research paper</div>
          <div className="float-card fb"><MessageSquareText size={15} /> Grounded answer <Check size={13} /></div>
          <div className="float-card fc"><BookOpen size={15} /> Source passages</div>
        </div>
      </div>
      <div className="section-heading"><div><h2>Research tools</h2><p>Move from source material to useful insight.</p></div><span className="muted-label">YOUR WORKFLOW</span></div>
      <div className="action-grid">{tools.map(([destination, title, description], index) => <button className="action-card" key={destination} onClick={() => setSection(destination)}>
        <div className={`action-icon a${index}`}>{index === 0 ? <MessageSquareText size={19} /> : index === 1 ? <Search size={19} /> : index === 2 ? <FileText size={19} /> : index === 3 ? <Scale size={19} /> : <GraduationCap size={19} />}</div>
        <div className="action-title">{title}<ArrowRight size={14} /></div><p>{description}</p>
      </button>)}</div>
      <div className="section-heading library-heading"><div><h2>Your library</h2><p>Documents available to your research assistant.</p></div><button className="text-button" onClick={() => setSection('Documents')}>View library <ArrowRight size={14} /></button></div>
      {documents.length ? <DocumentList documents={documents.slice(0, 4)} /> : <EmptyState title="Your library is ready to grow" text="Upload a paper or image to start asking questions." action={() => setSection('Documents')} />}
    </>;
  }

  function renderDocuments() {
    return <>
      <PageIntro tag="KNOWLEDGE BASE" title="Your documents" description="Bring the research you trust into one searchable workspace." />
      <div className={`dropzone ${dragging ? 'dragging' : ''}`} onDragOver={event => { event.preventDefault(); setDragging(true); }} onDragLeave={() => setDragging(false)} onDrop={event => { event.preventDefault(); setDragging(false); void uploadFiles(event.dataTransfer.files); }}>
        <input ref={fileInput} type="file" accept=".pdf,.png,.jpg,.jpeg,.bmp,.tiff" multiple hidden onChange={event => void uploadFiles(event.target.files)} />
        <div className="upload-symbol"><Upload size={21} /></div><h3>{busy ? 'Processing your documents' : 'Drop documents here'}</h3>
        <p>PDFs and images — indexed for chat, search and study tools.</p>
        <button className="button primary" disabled={busy} onClick={() => fileInput.current?.click()}><Plus size={15} />{busy ? 'Working…' : 'Choose files'}</button>
        <small>Multiple files supported · PDF, PNG, JPG, BMP, TIFF</small>
      </div>
      <div className="section-heading library-heading"><div><h2>Indexed documents</h2><p>{documents.length} {documents.length === 1 ? 'document' : 'documents'} in your library</p></div><button className="icon-button" onClick={() => void refreshDocuments().catch(reason => setError(reason instanceof Error ? reason.message : 'Unable to refresh documents.'))} aria-label="Refresh documents"><Activity size={16} /></button></div>
      {documents.length ? <div className="doc-table">{documents.map(name => <div className="doc-row" key={name}>
        <div className="file-icon">{/\.(png|jpe?g|bmp|tiff)$/i.test(name) ? <FileImage size={17} /> : <FileText size={17} />}</div>
        <div className="doc-meta"><b>{name}</b><small>Available for research</small></div><span className="badge"><i /> Indexed</span>
        <button className="icon-button" aria-label={`Delete ${name} from the library and backend storage`} title="Delete uploaded file and indexed data" disabled={busy} onClick={() => {
          if (!window.confirm(`Delete ${name} from the library and permanently remove its uploaded file from backend storage?`)) return;
          void run(() => api.remove(name), response => {
            const remaining = response.data?.remaining_documents;
            const nextDocuments = Array.isArray(remaining) && remaining.every(item => typeof item === 'string')
              ? remaining as string[]
              : documents.filter(document => document !== name);
            setDocuments(nextDocuments);
            setSelected(current => current === name ? nextDocuments[0] || '' : current);
            setSecond(current => current === name ? nextDocuments.find(document => document !== nextDocuments[0]) || '' : current);
          });
        }}><Trash2 size={15} /></button>
      </div>)}</div> : <EmptyState title="No documents yet" text="Upload your first PDF or image to start a grounded research session." action={() => fileInput.current?.click()} />}
    </>;
  }

  function renderChat() {
    return <>
      <div className="chat-top"><div><div className="eyebrow"><i /> GROUNDED IN YOUR LIBRARY</div><h1>Research assistant</h1><p>Ask a question and explore the sources behind each answer.</p></div><button className="button secondary small" onClick={() => setMessages([])}><Plus size={15} /> New conversation</button></div>
      <div className="chat-panel"><div className="chat-feed" ref={feed}>
        {!messages.length ? <div className="chat-welcome"><div className="chat-spark"><Sparkles size={22} /></div><h2>What are you researching?</h2><p>Ask across {documents.length} indexed {documents.length === 1 ? 'document' : 'documents'}. Responses include citations returned by your research API.</p><div className="prompt-chips">{['What are the main findings?', 'Compare the key approaches', 'What limitations are discussed?'].map(prompt => <button key={prompt} onClick={() => setQuery(prompt)}>{prompt}<ArrowRight size={13} /></button>)}</div></div>
          : messages.map((message, index) => <div className={`message ${message.role}`} key={index}><div className="message-avatar">{message.role === 'assistant' ? <Sparkles size={14} /> : <span>SM</span>}</div><div className="message-body"><div className="message-label">{message.role === 'assistant' ? 'Atlas assistant' : 'You'}</div><div className="markdown"><ReactMarkdown remarkPlugins={[remarkGfm]}>{message.text}</ReactMarkdown></div>
            {message.citations?.length ? <div className="sources"><div className="sources-title">Sources · {message.citations.length}</div>{message.citations.map((citation, citationIndex) => <div className="source-card" key={`${citation.source}-${citation.chunk}-${citationIndex}`}><FileText size={15} /><div><b>{citation.source}</b><small>Page {citation.page} · Passage {citation.chunk}</small></div><span>[{citationIndex + 1}]</span></div>)}</div> : null}
            <button className="copy-action" onClick={() => void navigator.clipboard.writeText(message.text)}>Copy answer</button>
          </div></div>)}
        {busy && <div className="thinking"><i /><i /><i /> Searching your research library…</div>}
      </div><div className="composer"><textarea value={query} onChange={event => setQuery(event.target.value)} onKeyDown={event => { if (event.key === 'Enter' && !event.shiftKey) { event.preventDefault(); askQuestion(); } }} placeholder="Ask anything about your documents…" rows={2} /><div className="composer-bottom"><span>Enter to send · Shift + Enter for new line</span><button className="send-button" disabled={!query.trim() || busy} onClick={askQuestion} aria-label="Send question"><Send size={16} /></button></div></div></div>
    </>;
  }

  function renderSearch() {
    return <>
      <PageIntro tag="RETRIEVAL" title="Semantic search" description="Search for ideas, methods, and evidence across your indexed documents." />
      <div className="search-bar"><Search size={18} /><input value={query} onChange={event => setQuery(event.target.value)} onKeyDown={event => { if (event.key === 'Enter') searchDocuments(); }} placeholder="Describe what you’re looking for…" /><button className="button primary" disabled={busy || !query.trim()} onClick={searchDocuments}>Search <ArrowRight size={14} /></button></div>
      <div className="section-heading"><h2>Relevant passages {results.length > 0 && <small>· {results.length} retrieved</small>}</h2></div>
      {busy ? <div className="output-card">Searching indexed passages…</div> : results.length ? <div className="results">{results.map((result, index) => <article className="result-card" key={index}><div className="result-source"><FileText size={15} /><b>{String(result.metadata.source || 'Source')}</b>{result.metadata.page != null && <span>Page {String(result.metadata.page)}</span>}</div><p>{result.content}</p>{result.metadata.chunk_index != null && <small>Passage {String(result.metadata.chunk_index)}</small>}</article>)}</div> : <EmptyState title="Search your research" text="Use a natural-language query to retrieve relevant passages from your library." />}
    </>;
  }

  function renderGenerator() {
    const compare = section === 'Compare';
    const summarize = section === 'Summarize';
    const title = summarize ? 'Summarize a paper' : compare ? 'Compare research' : 'Study notes';
    const description = summarize ? 'Get a focused summary from the indexed content of a selected document.' : compare ? 'Explore similarities and differences across two papers.' : 'Create a structured learning aid from one of your documents.';
    return <>
      <PageIntro tag={summarize ? 'DOCUMENT INTELLIGENCE' : compare ? 'CROSS-PAPER ANALYSIS' : 'LEARNING STUDIO'} title={title} description={description} />
      <div className="tool-panel"><div className="tool-header"><div className="tool-badge"><Sparkles size={17} /></div><div><b>{summarize ? 'Document summary' : compare ? 'Paper comparison' : 'Study guide'}</b><p>Generated using your existing FastAPI research pipeline.</p></div></div>
        <div className="form-grid"><label>Document{compare ? ' A' : ''}<select value={selected} onChange={event => setSelected(event.target.value)}><option value="">Select a document</option>{documents.map(name => <option key={name} value={name}>{name}</option>)}</select></label>
          {compare ? <label>Document B<select value={second} onChange={event => setSecond(event.target.value)}><option value="">Select a document</option>{documents.map(name => <option key={name} value={name}>{name}</option>)}</select></label> : null}
          {section === 'Study notes' ? <label>Note format<select value={noteType} onChange={event => setNoteType(event.target.value)}>{['detailed', 'short', 'flashcards', 'interview', 'mcq', 'revision', 'cheatsheet', 'mindmap', 'faq', 'exam'].map(type => <option key={type} value={type}>{type[0].toUpperCase() + type.slice(1)}</option>)}</select></label> : null}
        </div><button className="button primary" disabled={busy || !selected || (compare && (!second || second === selected))} onClick={generate}>{busy ? 'Generating…' : <><Sparkles size={15} />{summarize ? 'Generate summary' : compare ? 'Compare documents' : 'Generate notes'}</>}</button>
      </div>
      {output ? <article className="output-card"><div className="output-heading"><h2>{summarize ? 'Summary' : compare ? 'Comparison' : 'Study notes'}</h2><button className="button secondary small" onClick={() => void navigator.clipboard.writeText(output)}>Copy</button></div><div className="markdown"><ReactMarkdown remarkPlugins={[remarkGfm]}>{output}</ReactMarkdown></div></article> : null}
      {!output && !documents.length ? <EmptyState title="Add a document to begin" text="Upload documents first, then return here to generate grounded insights." action={() => setSection('Documents')} /> : null}
    </>;
  }

  const groups = [...new Set(navigation.map(item => item.group))];
  const content = section === 'Overview' ? renderOverview() : section === 'Documents' ? renderDocuments() : section === 'Research chat' ? renderChat() : section === 'Semantic search' ? renderSearch() : renderGenerator();

  return <main className="app-shell">
    <aside className={`sidebar ${mobileMenu ? 'mobile-open' : ''}`}>
      <div className="brand"><div className="brand-mark"><Sparkles size={18} /></div><div><b>atlas</b><span>RESEARCH WORKSPACE</span></div><button className="icon-button collapse" onClick={() => setMobileMenu(false)} aria-label="Close navigation">×</button></div>
      <button className="workspace-switch"><span className="workspace-avatar">S</span><span className="workspace-meta"><b>Samarth’s workspace</b><small>Personal plan</small></span><span>⌄</span></button>
      <div className="side-nav">{groups.map(group => <div key={group}><div className="nav-label">{group}</div>{navigation.filter(item => item.group === group).map(item => <button key={item.name} className={`nav-item ${section === item.name ? 'active' : ''}`} onClick={() => { setSection(item.name); setMobileMenu(false); setError(''); }}><item.icon size={17} /><span>{item.name}</span>{item.name === 'Documents' && <small>{documents.length}</small>}</button>)}</div>)}</div>
      <div className="sidebar-bottom"><div className="storage"><Activity size={16} /><div><b>Research library</b><small>{documents.length} indexed documents</small></div></div><div className="profile"><div className="profile-avatar">SM</div><div><b>Samarth More</b><small>Researcher</small></div></div></div>
    </aside>
    {mobileMenu && <button className="scrim" onClick={() => setMobileMenu(false)} aria-label="Close menu" />}
    <section className="main-area"><header className="topbar"><div className="top-left"><button className="icon-button mobile-menu" onClick={() => setMobileMenu(true)} aria-label="Open navigation"><Menu size={19} /></button><div className="breadcrumbs"><span>Workspace</span><span>/</span><b>{section}</b></div></div><div className="top-right"><div className="status"><i className={apiOnline === false ? 'offline' : ''} />{apiOnline ? 'API connected' : apiOnline === false ? 'API offline' : 'Connecting'}</div><button className="icon-button" onClick={() => setDark(value => !value)} aria-label="Toggle theme">{dark ? <Sun size={17} /> : <Moon size={17} />}</button><div className="top-avatar">SM</div></div></header>
      <div className="page-scroll"><div className="content">{error && <div className="alert"><span>{error}</span><button onClick={() => setError('')} aria-label="Dismiss"><X size={15} /></button></div>}{content}</div></div>
      <footer className="footer"><span>Atlas Research</span><span>Responses and source metadata provided by your FastAPI service.</span></footer>
    </section>
  </main>;
}

function PageIntro({ tag, title, description }: { tag: string; title: string; description: string }) {
  return <div className="page-intro"><div className="eyebrow"><i /> {tag}</div><h1>{title}</h1><p>{description}</p></div>;
}

function EmptyState({ title, text, action }: { title: string; text: string; action?: () => void }) {
  return <div className="empty-state"><div className="empty-icon"><Files size={20} /></div><h3>{title}</h3><p>{text}</p>{action && <button className="button secondary small" onClick={action}><Plus size={14} /> Upload documents</button>}</div>;
}

function DocumentList({ documents }: { documents: string[] }) {
  return <div className="doc-table">{documents.map(name => <div className="doc-row" key={name}><div className="file-icon"><FileText size={17} /></div><div className="doc-meta"><b>{name}</b><small>Indexed in research library</small></div><span className="badge"><i /> Ready</span></div>)}</div>;
}
