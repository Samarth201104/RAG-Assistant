const API_URL = (process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000').replace(/\/$/, '');

export type ApiEnvelope<T> = {
  success: boolean;
  message: string;
  response?: T;
  data?: Record<string, unknown>;
};
export type Citation = { source: string; page: number; chunk: number };
export type ChatResult = { question: string; answer: string; citations: Citation[]; retrieved_chunks: number };
export type SearchResponse = {
  query: string;
  retrieved_chunks: number;
  documents: { content: string; metadata: Record<string, unknown> }[];
};
export type DeleteResponse = { remaining_documents: string[] };

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  let response: Response;
  try {
    response = await fetch(API_URL + path, {
      ...init,
      signal: init?.signal ?? AbortSignal.timeout(120000),
    });
  } catch (error) {
    console.error('API network error', error);
    if (error instanceof DOMException && error.name === 'TimeoutError') {
      throw new Error('The request took too long. Please try again.');
    }
    throw new Error('The research service is unavailable. Check that the backend is running, then try again.');
  }

  if (!response.ok) {
    const detail = await response.json().catch(() => null);
    console.error('API error', response.status, detail);
    if (response.status === 404) throw new Error('That endpoint or document could not be found. Refresh the document list and try again.');
    if (response.status === 400 || response.status === 422) throw new Error('The backend could not process this request. Check the selected document and try again.');
    throw new Error('Unable to complete your request. The backend may be temporarily unavailable. Please try again.');
  }

  let payload: unknown;
  try {
    payload = await response.json();
  } catch (error) {
    console.error('Malformed API response', error);
    throw new Error('The backend returned an unreadable response. Please try again.');
  }

  if (payload && typeof payload === 'object' && 'success' in payload && payload.success === false) {
    console.error('API operation was not successful', payload);
    throw new Error('The backend could not complete that operation. Please try again.');
  }
  return payload as T;
}

const json = (body: unknown): RequestInit => ({
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(body),
});

export const api = {
  health: () => request<{ status: string }>('/health'),
  // The document workspace represents the Chroma index; disk uploads remain on disk after unindexing.
  documents: async (): Promise<string[]> => {
    const result = await request<ApiEnvelope<{ documents?: string[] }>>('/upload/documents');
    const documents = result.data?.documents;
    if (!Array.isArray(documents) || documents.some(name => typeof name !== 'string')) {
      console.error('Unexpected indexed document response', result);
      throw new Error('The backend returned an unexpected document list. Please refresh and try again.');
    }
    return documents;
  },
  upload: async (files: File[]) => {
    const pdfs = files.filter(file => file.type === 'application/pdf' || file.name.toLowerCase().endsWith('.pdf'));
    const images = files.filter(file => !pdfs.includes(file));
    const send = async (batch: File[], kind: 'pdf' | 'image') => {
      if (!batch.length) return null;
      const form = new FormData();
      batch.forEach(file => form.append('files', file));
      return request<ApiEnvelope<Record<string, unknown>>>(`/upload/${kind}`, { method: 'POST', body: form });
    };
    return Promise.all([send(pdfs, 'pdf'), send(images, 'image')]);
  },
  remove: (filename: string) => request<ApiEnvelope<DeleteResponse>>(
    `/upload/document/${encodeURIComponent(filename)}`,
    { method: 'DELETE' },
  ),
  ask: (question: string) => request<ApiEnvelope<ChatResult>>('/query', json({ question, top_k: 5 })),
  search: (question: string) => request<ApiEnvelope<SearchResponse>>('/query/retrieve', json({ question, top_k: 8 })),
  summarize: (filename: string) => request<ApiEnvelope<Record<string, unknown>>>('/summarize', json({ filename })),
  compare: (document_1: string, document_2: string) => request<ApiEnvelope<Record<string, unknown>>>('/compare', json({ document_1, document_2 })),
  notes: (filename: string, note_type: string) => request<ApiEnvelope<Record<string, unknown>>>('/notes', json({ filename, note_type })),
};
