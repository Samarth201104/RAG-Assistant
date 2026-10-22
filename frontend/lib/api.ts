const API_URL = (process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000').replace(/\/$/, '');
export type ApiEnvelope<T> = { success: boolean; message: string; response?: T; data?: Record<string, any> };
export type Citation = { source: string; page: number; chunk: number };
export type ChatResult = { question: string; answer: string; citations: Citation[]; retrieved_chunks: number };
async function request<T>(path: string, init?: RequestInit): Promise<T> {
  let response: Response;
  try { response = await fetch(API_URL + path, { ...init, signal: init?.signal ?? AbortSignal.timeout(120000) }); }
  catch (error) { console.error('API network error', error); throw new Error('The research service is unavailable. Check that the backend is running, then try again.'); }
  if (!response.ok) { const detail = await response.json().catch(() => null); console.error('API error', response.status, detail); throw new Error(response.status === 404 ? 'That endpoint or document could not be found.' : 'Unable to complete your request. Please try again.'); }
  return response.json() as Promise<T>;
}
const json = (body: unknown): RequestInit => ({ method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
export const api = {
  health: () => request<{status:string}>('/health'),
  documents: async (): Promise<string[]> => { const [pdf,img,indexed] = await Promise.all([request<ApiEnvelope<any>>('/upload/pdfs'),request<ApiEnvelope<any>>('/upload/images'),request<ApiEnvelope<any>>('/upload/documents')]); return [...(pdf.data?.documents ?? []),...(img.data?.images ?? []),...(indexed.data?.documents ?? [])].filter((v,i,a): v is string=>typeof v==='string'&&a.indexOf(v)===i); },
  upload: async (files: File[]) => { const pdfs=files.filter(f=>f.type==='application/pdf'||f.name.toLowerCase().endsWith('.pdf')); const images=files.filter(f=>!pdfs.includes(f)); const send=async(list:File[],kind:'pdf'|'image')=>{if(!list.length)return null;const form=new FormData();list.forEach(f=>form.append('files',f));return request<ApiEnvelope<any>>('/upload/'+kind,{method:'POST',body:form});}; return Promise.all([send(pdfs,'pdf'),send(images,'image')]); },
  remove: (filename:string) => request('/upload/document/'+encodeURIComponent(filename),{method:'DELETE'}),
  ask: (question:string) => request<ApiEnvelope<ChatResult>>('/query',json({question,top_k:5})),
  search: (question:string) => request<ApiEnvelope<{query:string;retrieved_chunks:number;documents:{content:string;metadata:Record<string,unknown>}[]}>>('/query/retrieve',json({question,top_k:8})),
  summarize: (filename:string) => request<ApiEnvelope<Record<string,unknown>>>('/summarize',json({filename})),
  compare: (document_1:string,document_2:string) => request<ApiEnvelope<Record<string,unknown>>>('/compare',json({document_1,document_2})),
  notes: (filename:string,note_type:string) => request<ApiEnvelope<Record<string,unknown>>>('/notes',json({filename,note_type})),
};
