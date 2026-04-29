import React, { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import {
  Sparkles,
  Upload,
  Target,
  MessageSquare,
  Download,
  BarChart3,
  CheckCircle2,
  Loader2,
  UserSearch,
  Rocket,
  ShieldCheck,
  FileText,
  Brain,
} from 'lucide-react';
import './styles.css';

type Category = {
  matched: string[];
  missing: string[];
  score: number;
};

type Analysis = {
  ats_score: number;
  summary: string;
  keyword_gap: {
    matched_keywords: string[];
    missing_keywords: string[];
  };
  category_coverage?: Record<string, Category>;
  improved_bullets: string[];
  ai_generated_bullets?: string[];
  ai_interview_questions?: string[];
  ai_star_answers?: string[];
  ai_recruiter_summary?: string;
  action_plan?: string[];
  resume_quality?: {
    metric_strength: number;
    section_strength: number;
    jd_terms_detected: string[];
  };
};

const API_URL =
  import.meta.env.VITE_API_URL ||
  'https://ai-career-copilot-i5qw.onrender.com/api';

function scoreLabel(score: number) {
  if (score >= 80) return 'Strong Match';
  if (score >= 65) return 'Good Match';
  if (score >= 45) return 'Needs Targeting';
  return 'Major Rewrite Needed';
}

function AnimatedScore({ score }: { score: number }) {
  const [displayScore, setDisplayScore] = useState(0);

  useEffect(() => {
    let start = 0;
    const duration = 900;
    const stepTime = 16;
    const increment = score / (duration / stepTime);

    const timer = setInterval(() => {
      start += increment;

      if (start >= score) {
        setDisplayScore(score);
        clearInterval(timer);
      } else {
        setDisplayScore(Math.round(start));
      }
    }, stepTime);

    return () => clearInterval(timer);
  }, [score]);

  return <div className="score">{displayScore}</div>;
}

function App() {
  const [enteredApp, setEnteredApp] = useState(false);
  const [resumeText, setResumeText] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const [includeAts, setIncludeAts] = useState(true);
  const [includeBullets, setIncludeBullets] = useState(true);
  const [includeInterview, setIncludeInterview] = useState(true);
  const [includeStar, setIncludeStar] = useState(true);
  const [includeRecruiterSummary, setIncludeRecruiterSummary] = useState(true);
  const [wantsCoverLetter, setWantsCoverLetter] = useState(false);

  async function parseResume(file: File) {
    const formData = new FormData();
    formData.append('file', file);

    setError('');

    try {
      const res = await fetch(`${API_URL}/parse-resume`, {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) throw new Error('Could not parse resume PDF');

      const data = await res.json();
      setResumeText(data.text);
    } catch (e: any) {
      setError(e.message || 'Could not parse resume PDF');
    }
  }

  async function analyze() {
    setLoading(true);
    setError('');
    setAnalysis(null);

    try {
      const res = await fetch(`${API_URL}/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          resume_text: resumeText,
          job_description: jobDescription,
        }),
      });

      if (!res.ok) {
        throw new Error('Please add a resume and job description with enough text.');
      }

      const data = await res.json();
      setAnalysis(data);
    } catch (e: any) {
      setError(e.message || 'Something went wrong');
    } finally {
      setLoading(false);
    }
  }

  function exportReport() {
    if (!analysis) return;

    const lines = [
      'AI Career Copilot Report',
      `ATS Score: ${analysis.ats_score}/100 - ${scoreLabel(analysis.ats_score)}`,
      '',
      'Summary:',
      analysis.summary,
      '',
      'AI Recruiter Summary:',
      analysis.ai_recruiter_summary || 'Not available',
      '',
      'Matched Keywords:',
      analysis.keyword_gap.matched_keywords.join(', ') || 'None',
      '',
      'Missing Keywords:',
      analysis.keyword_gap.missing_keywords.join(', ') || 'None',
      '',
      'ATS-Based Resume Bullet Suggestions:',
      ...analysis.improved_bullets.map((x) => `- ${x}`),
      '',
      'AI Personalized Resume Bullets:',
      ...(analysis.ai_generated_bullets || []).map((x) => `- ${x}`),
      '',
      'Priority Action Plan:',
      ...(analysis.action_plan || []).map((x) => `- ${x}`),
      '',
      'AI Personalized Interview Questions:',
      ...(analysis.ai_interview_questions || []).map((x) => `- ${x}`),
      '',
      'AI Personalized STAR Answers:',
      ...(analysis.ai_star_answers || []).map((x) => `- ${x}`),
    ];

    const blob = new Blob([lines.join('\n')], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');

    a.href = url;
    a.download = 'ai-career-copilot-report.txt';
    a.click();

    URL.revokeObjectURL(url);
  }

  if (!enteredApp) {
    return (
      <main className="welcome">
        <div className="orb orb-one" />
        <div className="orb orb-two" />
        <div className="orb orb-three" />

        <section className="welcomeCard">
          <div className="badge premiumBadge">
            <Sparkles size={16} />
            Powered by Gemini AI
          </div>

          <h1>AI Career Copilot</h1>

          <p className="welcomeSubtitle">
            Your personal AI recruiter, resume strategist, and interview coach.
          </p>

          <div className="welcomeFeatures">
            <div>
              <ShieldCheck size={20} />
              ATS Match Scoring
            </div>
            <div>
              <Brain size={20} />
              Personalized AI Coaching
            </div>
            <div>
              <FileText size={20} />
              Resume Bullet Rewrites
            </div>
          </div>

          <button className="launchButton" onClick={() => setEnteredApp(true)}>
            <Rocket size={19} />
            Launch Career Copilot
          </button>

          <p className="welcomeNote">
            Built with React, TypeScript, FastAPI, Gemini API, Vercel, and Render.
          </p>
        </section>
      </main>
    );
  }

  return (
    <main className="app">
      <section className="hero fade-up">
        <div className="badge">
          <Sparkles size={16} />
          Gemini-powered AI career platform
        </div>

        <h1>AI Career Copilot</h1>

        <p>
          Upload your resume, paste a job description, choose your outputs, and
          generate ATS insights plus personalized AI interview preparation.
        </p>
      </section>

      <section className="grid">
        <div className="card fade-up delay-1">
          <h2>
            <Upload size={20} />
            Resume
          </h2>

          <input
            type="file"
            accept="application/pdf"
            onChange={(e) => {
              const file = e.target.files?.[0];
              if (file) parseResume(file);
            }}
          />

          <textarea
            value={resumeText}
            onChange={(e) => setResumeText(e.target.value)}
            placeholder="Paste resume text or upload PDF..."
          />
        </div>

        <div className="card fade-up delay-2">
          <h2>
            <Target size={20} />
            Job Description
          </h2>

          <textarea
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            placeholder="Paste the full job description here..."
          />

          <div className="optionPanel">
            <h3>Choose outputs</h3>

            <label>
              <input
                type="checkbox"
                checked={includeAts}
                onChange={(e) => setIncludeAts(e.target.checked)}
              />
              ATS match report
            </label>

            <label>
              <input
                type="checkbox"
                checked={includeRecruiterSummary}
                onChange={(e) => setIncludeRecruiterSummary(e.target.checked)}
              />
              AI recruiter summary
            </label>

            <label>
              <input
                type="checkbox"
                checked={includeBullets}
                onChange={(e) => setIncludeBullets(e.target.checked)}
              />
              Resume bullet rewrites
            </label>

            <label>
              <input
                type="checkbox"
                checked={includeInterview}
                onChange={(e) => setIncludeInterview(e.target.checked)}
              />
              Interview questions
            </label>

            <label>
              <input
                type="checkbox"
                checked={includeStar}
                onChange={(e) => setIncludeStar(e.target.checked)}
              />
              STAR answers
            </label>

            <div className="coverToggle">
              <span>Need a cover letter?</span>
              <div>
                <button
                  type="button"
                  className={!wantsCoverLetter ? 'toggleActive' : 'toggleButton'}
                  onClick={() => setWantsCoverLetter(false)}
                >
                  No
                </button>
                <button
                  type="button"
                  className={wantsCoverLetter ? 'toggleActive' : 'toggleButton'}
                  onClick={() => setWantsCoverLetter(true)}
                >
                  Yes
                </button>
              </div>
            </div>

            {wantsCoverLetter && (
              <p className="miniNote">
                Cover letter generation will be added as a separate action so the
                app stays fast and avoids unnecessary AI calls.
              </p>
            )}
          </div>

          <button onClick={analyze} disabled={loading}>
            {loading ? (
              <>
                <Loader2 className="spinner" size={18} />
                Generating AI analysis...
              </>
            ) : (
              <>
                <Sparkles size={18} />
                Analyze Match
              </>
            )}
          </button>

          {error && <p className="error">{error}</p>}
        </div>
      </section>

      {analysis && (
        <section className="results fade-up">
          {includeAts && (
            <div className="scoreCard">
              <h2>
                <BarChart3 size={22} />
                ATS Match Score
              </h2>

              <AnimatedScore score={analysis.ats_score} />

              <div className="scoreLabel">{scoreLabel(analysis.ats_score)}</div>

              <p>{analysis.summary}</p>

              <button className="secondary" onClick={exportReport}>
                <Download size={18} />
                Export Report
              </button>
            </div>
          )}

          {includeRecruiterSummary && analysis.ai_recruiter_summary && (
            <div className="card result-card aiCard">
              <h2>
                <UserSearch size={20} />
                AI Recruiter Summary
              </h2>
              <p>{analysis.ai_recruiter_summary}</p>
            </div>
          )}

          {includeAts && (
            <>
              <div className="grid">
                <ResultCard
                  title="Matched Keywords"
                  items={analysis.keyword_gap.matched_keywords}
                />

                <ResultCard
                  title="Missing Keywords"
                  items={analysis.keyword_gap.missing_keywords}
                />
              </div>

              {analysis.category_coverage && (
                <CategoryCoverage categories={analysis.category_coverage} />
              )}

              {analysis.resume_quality && (
                <div className="grid">
                  <Metric
                    title="Quantified Impact Strength"
                    value={analysis.resume_quality.metric_strength}
                  />

                  <Metric
                    title="Resume Section Completeness"
                    value={analysis.resume_quality.section_strength}
                  />
                </div>
              )}

              <ResultCard
                title="Priority Action Plan"
                items={analysis.action_plan || []}
                icon={<CheckCircle2 size={20} />}
              />
            </>
          )}

          {includeBullets && (
            <>
              <ResultCard
                title="ATS-Based Resume Bullet Suggestions"
                items={analysis.improved_bullets}
              />

              {analysis.ai_generated_bullets &&
                analysis.ai_generated_bullets.length > 0 && (
                  <ResultCard
                    title="AI Personalized Resume Bullets"
                    items={analysis.ai_generated_bullets}
                    icon={<Sparkles size={20} />}
                  />
                )}
            </>
          )}

          {includeInterview &&
            analysis.ai_interview_questions &&
            analysis.ai_interview_questions.length > 0 && (
              <ResultCard
                title="AI Personalized Interview Questions"
                items={analysis.ai_interview_questions}
                icon={<MessageSquare size={20} />}
              />
            )}

          {includeStar &&
            analysis.ai_star_answers &&
            analysis.ai_star_answers.length > 0 && (
              <ResultCard
                title="AI Personalized STAR Answers"
                items={analysis.ai_star_answers}
                icon={<Sparkles size={20} />}
              />
            )}

          {wantsCoverLetter && (
            <div className="card result-card comingSoonCard">
              <h2>
                <FileText size={20} />
                Cover Letter Generator
              </h2>
              <p>
                Smart choice. Cover letter generation is prepared in the UI and
                will be connected as a separate Gemini action next.
              </p>
            </div>
          )}
        </section>
      )}

      <footer className="footer">
        Built by Likith Kumar Tarala · Powered by Gemini AI · React + FastAPI
      </footer>
    </main>
  );
}

function ResultCard({
  title,
  items,
  icon,
}: {
  title: string;
  items: string[];
  icon?: React.ReactNode;
}) {
  return (
    <div className="card result-card">
      <h2>
        {icon}
        {title}
      </h2>

      <ul>
        {items.length ? (
          items.map((item, i) => <li key={i}>{item}</li>)
        ) : (
          <li>None found</li>
        )}
      </ul>
    </div>
  );
}

function Metric({ title, value }: { title: string; value: number }) {
  return (
    <div className="card metric">
      <h2>{title}</h2>

      <div className="metricValue">{value}%</div>

      <div className="bar">
        <span style={{ width: `${value}%` }} />
      </div>
    </div>
  );
}

function CategoryCoverage({
  categories,
}: {
  categories: Record<string, Category>;
}) {
  return (
    <div className="card result-card">
      <h2>Skill Category Coverage</h2>

      <div className="categories">
        {Object.entries(categories).map(([name, data]) => (
          <div key={name} className="category">
            <div className="categoryTop">
              <strong>{name}</strong>
              <span>{data.score}%</span>
            </div>

            <div className="bar">
              <span style={{ width: `${data.score}%` }} />
            </div>

            <small>
              Matched: {data.matched.join(', ') || 'None'} | Missing:{' '}
              {data.missing.join(', ') || 'None'}
            </small>
          </div>
        ))}
      </div>
    </div>
  );
}

createRoot(document.getElementById('root')!).render(<App />);