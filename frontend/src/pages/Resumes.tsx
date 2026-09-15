import React, { useEffect, useMemo, useRef, useState } from 'react';
import { FileText, Sparkles, UploadCloud, CheckCircle2, XCircle, Loader2, FileUp } from 'lucide-react';
import { GlobalWorkerOptions, getDocument } from 'pdfjs-dist';
import mammoth from 'mammoth/mammoth.browser';
import { resumeApi } from '../api/resumes';
import type { ResumeFile, ResumeProposal } from '../types/resume';

GlobalWorkerOptions.workerSrc = new URL('pdfjs-dist/build/pdf.worker.min.mjs', import.meta.url).toString();

const defaultResumeText = `Senior Python engineer with FastAPI, PostgreSQL, and Docker. Built backend APIs and collaborated across product teams.`;

export const Resumes: React.FC = () => {
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const [resumeText, setResumeText] = useState(defaultResumeText);
  const [selectedFileName, setSelectedFileName] = useState<string | null>(null);
  const [isDraggingOver, setIsDraggingOver] = useState(false);
  const [resumes, setResumes] = useState<ResumeFile[]>([]);
  const [selectedResumeId, setSelectedResumeId] = useState<string | null>(null);
  const [proposals, setProposals] = useState<ResumeProposal[]>([]);
  const [loading, setLoading] = useState(false);
  const [loadingResumes, setLoadingResumes] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const extractPdfText = async (file: File): Promise<string> => {
    const arrayBuffer = await file.arrayBuffer();
    const pdf = await getDocument({ data: arrayBuffer }).promise;
    const pages: string[] = [];

    for (let pageNumber = 1; pageNumber <= pdf.numPages; pageNumber += 1) {
      const page = await pdf.getPage(pageNumber);
      const textContent = await page.getTextContent();
      const text = textContent.items
        .map((item: any) => ('str' in item ? item.str : ''))
        .join(' ');
      pages.push(text);
    }

    return pages.join('\n\n').trim();
  };

  const extractDocxText = async (file: File): Promise<string> => {
    const arrayBuffer = await file.arrayBuffer();
    const result = await mammoth.extractRawText({ arrayBuffer });
    return result.value.trim();
  };

  const readTextFile = async (file: File) => {
    const validTextMimeTypes = [
      'text/plain',
      'text/markdown',
      'text/csv',
      'application/json',
      'application/xml',
      'text/xml',
    ];

    const isTextLike = validTextMimeTypes.includes(file.type) || /\.(txt|md|csv|json|xml)$/i.test(file.name);
    const isPdf = file.type === 'application/pdf' || /\.pdf$/i.test(file.name);
    const isDocx = file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' || /\.docx$/i.test(file.name);

    if (!isTextLike && !isPdf && !isDocx) {
      setError('Unsupported file type. Please use TXT, MD, DOCX, or PDF.');
      return;
    }

    try {
      let fileText = '';

      if (isPdf) {
        fileText = await extractPdfText(file);
      } else if (isDocx) {
        fileText = await extractDocxText(file);
      } else {
        const reader = new FileReader();
        fileText = await new Promise<string>((resolve, reject) => {
          reader.onload = () => resolve(typeof reader.result === 'string' ? reader.result : '');
          reader.onerror = () => reject(new Error('The selected file could not be read.'));
          reader.readAsText(file);
        });
      }

      const cleanedText = fileText.trim() || defaultResumeText;
      setResumeText(cleanedText);
      setSelectedFileName(file.name);
      setSuccess(`Loaded ${file.name}. You can review and upload it below.`);
      setError(null);
    } catch (err: any) {
      setError(err?.message || 'The selected file could not be read. Please try again.');
    }
  };

  const handleFileSelect = (file: File | null | undefined) => {
    if (!file) return;
    void readTextFile(file);
  };

  const fetchResumes = async () => {
    try {
      setLoadingResumes(true);
      const data = await resumeApi.list();
      setResumes(data);
      if (data.length > 0 && !selectedResumeId) {
        setSelectedResumeId(data[0].id);
      }
    } catch (err: any) {
      setError(err.message || 'Unable to load your uploaded resumes.');
    } finally {
      setLoadingResumes(false);
    }
  };

  useEffect(() => {
    void fetchResumes();
  }, []);

  const selectedResume = useMemo(
    () => resumes.find((resume) => resume.id === selectedResumeId) ?? null,
    [resumes, selectedResumeId]
  );

  const handleUpload = async () => {
    if (!resumeText.trim()) {
      setError('Please paste some resume text before uploading.');
      return;
    }

    setLoading(true);
    setError(null);
    setSuccess(null);

    try {
      const resolvedFileName = selectedFileName || `resume-${Date.now()}.txt`;
      const uploaded = await resumeApi.upload({
        filename: resolvedFileName,
        content_type: selectedFileName?.toLowerCase().endsWith('.txt') ? 'text/plain' : 'text/plain',
        content: resumeText,
      });

      setSelectedResumeId(uploaded.id);
      const extracted = await resumeApi.extract(uploaded.id);
      setProposals(extracted.proposals);
      await fetchResumes();
      setSuccess('Resume uploaded and extracted successfully.');
    } catch (err: any) {
      setError(err.message || 'Unable to upload and extract the resume.');
    } finally {
      setLoading(false);
    }
  };

  const handleReview = async (proposalId: string, decision: 'accepted' | 'rejected') => {
    try {
      setError(null);
      const updated = await resumeApi.reviewProposal(proposalId, decision);
      setProposals((current) =>
        current.map((proposal) => (proposal.id === updated.id ? { ...proposal, decision: updated.decision } : proposal))
      );
    } catch (err: any) {
      setError(err.message || 'Unable to update the proposal review.');
    }
  };

  const getDecisionTone = (decision: ResumeProposal['decision']) => {
    switch (decision) {
      case 'accepted':
        return 'border-emerald-500/30 bg-emerald-500/10 text-emerald-200';
      case 'rejected':
        return 'border-rose-500/30 bg-rose-500/10 text-rose-200';
      default:
        return 'border-amber-500/30 bg-amber-500/10 text-amber-200';
    }
  };

  return (
    <div className="space-y-6 max-w-6xl mx-auto pb-12">
      <div>
        <p className="text-xs uppercase tracking-widest text-indigo-400 font-bold">Module 3: Resume Ingestion</p>
        <h1 className="text-3xl font-bold text-white mt-2">Resume upload & extraction</h1>
        <p className="text-slate-400 mt-2">Paste or upload a resume and review AI-generated profile proposals before they become trusted facts.</p>
      </div>

      {(error || success) && (
        <div
          className={`p-3 rounded-xl border text-sm ${error ? 'border-rose-500/30 bg-rose-500/10 text-rose-200' : 'border-emerald-500/30 bg-emerald-500/10 text-emerald-200'}`}
          role="alert"
        >
          {error || success}
        </div>
      )}

      <div className="grid xl:grid-cols-[1.4fr_0.8fr] gap-6">
        <section className="glass-panel p-6 rounded-2xl border border-white/10">
          <div className="flex items-center gap-3 mb-4">
            <UploadCloud className="w-5 h-5 text-indigo-400" />
            <h2 className="text-lg font-semibold text-white">Resume content</h2>
          </div>

          <div
            onDragOver={(event) => {
              event.preventDefault();
              setIsDraggingOver(true);
            }}
            onDragLeave={() => setIsDraggingOver(false)}
            onDrop={(event) => {
              event.preventDefault();
              setIsDraggingOver(false);
              const file = event.dataTransfer.files?.[0];
              handleFileSelect(file);
            }}
            className={`mb-4 rounded-2xl border border-dashed p-4 transition ${
              isDraggingOver ? 'border-indigo-400 bg-indigo-500/10' : 'border-white/15 bg-slate-900/40'
            }`}
          >
            <div className="flex flex-col items-center justify-center gap-3 text-center">
              <div className="w-12 h-12 rounded-full bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-300">
                <FileUp className="w-5 h-5" />
              </div>
              <div>
                <p className="text-sm font-medium text-white">Drag and drop a resume here</p>
                <p className="text-xs text-slate-400 mt-1">Supports TXT, MD, DOCX, and PDF files.</p>
              </div>
              <button
                type="button"
                onClick={() => fileInputRef.current?.click()}
                className="inline-flex items-center gap-2 px-3 py-2 rounded-lg border border-white/10 bg-white/5 text-sm text-slate-200 hover:bg-white/10"
              >
                <UploadCloud className="w-4 h-4" />
                Browse files
              </button>
              <input
                ref={fileInputRef}
                type="file"
                className="hidden"
                accept=".txt,.md,.csv,.json,.xml,.pdf,.docx,text/plain,text/markdown,text/csv,application/json,application/xml,text/xml,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                onChange={(event) => handleFileSelect(event.target.files?.[0])}
              />
            </div>
          </div>

          {selectedFileName && (
            <div className="mb-3 rounded-lg border border-emerald-500/20 bg-emerald-500/10 px-3 py-2 text-sm text-emerald-200">
              Loaded file: {selectedFileName}
            </div>
          )}

          <textarea
            value={resumeText}
            onChange={(event) => setResumeText(event.target.value)}
            rows={14}
            className="w-full input-field resize-y"
            placeholder="Paste a resume here..."
          />

          <div className="mt-4 flex items-center justify-between gap-3">
            <span className="text-sm text-slate-400">{resumeText.length} characters</span>
            <button onClick={handleUpload} disabled={loading} className="btn-primary inline-flex items-center gap-2">
              {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Sparkles className="w-4 h-4" />}
              {loading ? 'Processing...' : 'Upload & extract'}
            </button>
          </div>
        </section>

        <aside className="glass-panel p-6 rounded-2xl border border-white/10">
          <div className="flex items-center gap-3 mb-4">
            <FileText className="w-5 h-5 text-indigo-400" />
            <h2 className="text-lg font-semibold text-white">Resumes</h2>
          </div>

          {loadingResumes ? (
            <div className="text-sm text-slate-400">Loading your uploads...</div>
          ) : resumes.length === 0 ? (
            <p className="text-sm text-slate-400">No resumes uploaded yet.</p>
          ) : (
            <div className="space-y-3">
              {resumes.map((resume) => (
                <button
                  key={resume.id}
                  onClick={() => setSelectedResumeId(resume.id)}
                  className={`w-full text-left p-3 rounded-xl border transition ${selectedResume?.id === resume.id ? 'border-indigo-500/30 bg-indigo-500/10' : 'border-white/10 bg-white/5 hover:border-white/20'}`}
                >
                  <div className="flex justify-between gap-2">
                    <span className="font-medium text-white truncate">{resume.filename}</span>
                    <span className="text-[10px] uppercase tracking-wide text-slate-400">{resume.status}</span>
                  </div>
                  <div className="mt-1 text-xs text-slate-400">{new Date(resume.created_at).toLocaleDateString()}</div>
                </button>
              ))}
            </div>
          )}
        </aside>
      </div>

      <section className="glass-panel p-6 rounded-2xl border border-white/10">
        <div className="flex items-center gap-3 mb-5">
          <Sparkles className="w-5 h-5 text-indigo-400" />
          <h2 className="text-lg font-semibold text-white">Extraction review</h2>
        </div>

        {!selectedResume && !proposals.length ? (
          <p className="text-sm text-slate-400">Upload a resume to generate structured proposals for review.</p>
        ) : (
          <div className="space-y-4">
            {selectedResume && (
              <div className="p-3 rounded-xl border border-white/10 bg-slate-900/60 text-sm text-slate-300">
                Selected file: <span className="text-white font-medium">{selectedResume.filename}</span>
              </div>
            )}

            {proposals.length === 0 ? (
              <p className="text-sm text-slate-400">No extraction proposals yet. Upload a resume to generate them.</p>
            ) : (
              proposals.map((proposal) => (
                <div key={proposal.id} className="rounded-xl border border-white/10 bg-white/5 p-4">
                  <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-3 mb-3">
                    <div>
                      <div className="text-[10px] uppercase tracking-wider text-indigo-400 font-bold">{proposal.proposal_type}</div>
                      <div className="text-lg font-semibold text-white">{proposal.proposed_value}</div>
                    </div>
                    <div className={`inline-flex items-center px-2.5 py-1 rounded-full border text-xs font-medium ${getDecisionTone(proposal.decision)}`}>
                      {proposal.decision}
                    </div>
                  </div>

                  <div className="text-sm text-slate-300 mb-3">
                    <span className="font-medium text-white">Source:</span> {proposal.source_excerpt || 'Extracted from uploaded resume content'}
                  </div>

                  <div className="flex flex-wrap gap-3">
                    <button
                      onClick={() => handleReview(proposal.id, 'accepted')}
                      className="inline-flex items-center gap-2 px-3 py-2 rounded-lg bg-emerald-500/15 border border-emerald-500/30 text-emerald-200 text-sm font-medium hover:bg-emerald-500/20"
                    >
                      <CheckCircle2 className="w-4 h-4" /> Accept
                    </button>
                    <button
                      onClick={() => handleReview(proposal.id, 'rejected')}
                      className="inline-flex items-center gap-2 px-3 py-2 rounded-lg bg-rose-500/15 border border-rose-500/30 text-rose-200 text-sm font-medium hover:bg-rose-500/20"
                    >
                      <XCircle className="w-4 h-4" /> Reject
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        )}
      </section>
    </div>
  );
};
