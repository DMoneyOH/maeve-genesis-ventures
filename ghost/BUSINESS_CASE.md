# Ghost — Autonomous Social Presence for Solopreneurs
## MaeveGenesis Venture Business Case
**Prepared by:** Maeve (AI Infrastructure Platform)
**Date:** 2026-04-28
**Status:** Pre-seed concept — awaiting backer decision
**Repo:** https://github.com/DMoneyOH/maeve-genesis-ventures

---

## Executive Summary

Ghost is an AI-operated LinkedIn and Twitter/X presence management service for solopreneurs and consultants. Maeve researches the client's industry weekly, writes posts in their documented voice, schedules them, and delivers a weekly content calendar for optional review. If the client approves or ignores the calendar, posts go live. If they want changes, they mark them in a Google Sheet. That is the entirety of client involvement.

The product is sold as a monthly retainer ($149–299/month) targeting solo consultants, fractional executives, and independent professionals who know LinkedIn matters but cannot sustain a consistent posting cadence. The market rate for human LinkedIn ghostwriters starts at $1,000/month. Ghost delivers the same output at 15% of the price — autonomously.

**Target revenue:** $750/month (MRR) by day 45 (5 clients). $1,500+/month by day 90.
**Build time to prototype:** 10 days.
**Ongoing human involvement post-launch:** 1–2 hours/week across all clients combined.

---

## Executive Summary — Why Ghost Over Sentinel

Both are viable. Ghost is chosen as the companion to Sentinel because:

1. **Higher per-client revenue** ($149–299/month vs. $12–35/month). Fewer clients needed to hit targets.
2. **Lower churn profile.** Clients who grow their LinkedIn presence become dependent on Ghost — leaving means their feed goes silent. Sentinel clients can churn more casually.
3. **Clearer competitive gap.** The $149/month AI ghostwriting tier is unoccupied. Human ghostwriters start at $1,000. The $850 gap is the product.
4. **Complementary to Sentinel.** A Sentinel client who monitors competitors might also want their own LinkedIn presence managed. Cross-sell is natural.

---

## 1. The Problem

LinkedIn organic reach for personal profiles is at an all-time high in 2026. Company pages are declining in algorithm favor — the platform now heavily rewards human-to-human interaction. Personal profiles get 5–10x more engagement than company pages.

Every solopreneur, consultant, and fractional executive knows this. Almost none post consistently.

The reasons are always the same: no time, blank page paralysis, uncertainty about what to write, inconsistency after a busy week. Human ghostwriters solve this but start at $1,000/month — justified for a VC-backed founder, inaccessible for an independent consultant billing $150/hour.

The result: millions of professionals with genuine expertise and valuable perspectives who are invisible on the only B2B platform that still has organic reach.

Ghost removes every single friction point: the research, the writing, the scheduling, the voice matching. The client's only job is to exist, answer a one-time voice questionnaire, and optionally approve a weekly calendar.

---

## 2. Market Sizing

### TAM
LinkedIn has **1 billion+ members** globally as of 2026. Approximately 65 million are senior professionals, executives, or self-employed. The LinkedIn ghostwriting market has grown 3x year-over-year with 200+ agencies globally as of 2026 (Windmill Growth). Total market size for LinkedIn content services is estimated at **$500M–$1B annually**.

### SAM
Solo consultants, fractional executives, independent professionals, and solopreneurs in the US: approximately 59 million self-employed individuals per BLS data, of whom roughly 15 million have active LinkedIn profiles and operate in B2B contexts. At even 0.1% penetration at $200/month average: **$360M SAM**.

### SOM
Year-one target: 50 clients at $200/month average = $10,000 MRR = $120,000 ARR. This is 0.003% of SAM. At 3 years: 300 clients = $720,000 ARR. These are conservative numbers that require no viral growth — only consistent direct outreach.

---

## 3. Competitive Landscape

### Human LinkedIn Ghostwriters (Freelance)
**Pricing:** $1,000–$5,000/month (Windmill Growth, 2026)
**Weakness:** Price is the wall. A solo consultant billing $8,000/month cannot justify a $3,000/month ghostwriter. Ghost enters at $149–299/month — 15–30% of the floor price.

### Cleverly (LinkedIn Agency)
**Pricing:** Content + ghostwriting from $697/month; outreach from $397/month
**Weakness:** Minimum engagement requires meaningful time investment. Target market is companies, not solo practitioners. No truly autonomous operation.

### Taplio / AuthoredUp (AI LinkedIn tools)
**Pricing:** $39–99/month
**Weakness:** These are content *assistance* tools — they still require the user to write, edit, and post. Ghost removes the user from the creation process entirely. These tools are for people who want to write better; Ghost is for people who don't want to write at all.

### Buffer / Hootsuite + AI
**Pricing:** $6–99/month
**Weakness:** Scheduling tools with AI writing assistance. User still creates or heavily edits content. No voice matching, no industry research, no autonomous research-to-post pipeline.

**The white space:** Fully autonomous, high-quality, voice-matched LinkedIn ghostwriting at under $300/month does not exist as a productized service. Human ghostwriters own the $1,000+ tier. AI scheduling tools own the $6–99/month DIY tier. Ghost occupies the unserved gap between them.

---

## 4. Ideal Customer Profile

### Primary ICP: The Revenue-Generating Solo Consultant
- **Who:** Independent consultant or fractional executive (CFO, CMO, CTO) billing $100–300/hour in B2B services
- **Profile:** 500+ LinkedIn connections, active in 1–2 industries, deep expertise, no time to post
- **Pain:** Knows that LinkedIn presence would drive inbound leads, has been told this by clients and peers, has tried posting consistently and failed within 3 weeks
- **Revenue at stake:** One inbound consultation from LinkedIn = $5,000–20,000. Ghost at $199/month pays for itself with 1 lead per quarter.
- **Willingness to pay:** $199/month is 1–2 billable hours. This is not a budget decision — it's a math decision.
- **Where to find them:** LinkedIn (obviously), r/consulting, Slack communities for fractional executives, Lenny's Newsletter community

### Secondary ICP: The Expert-Led Service Business Owner (1–5 employees)
- **Who:** Owner of a specialized service business (boutique agency, niche law practice, financial advisory, specialized coaching)
- **Pain:** The business's reputation is tied to the owner's personal brand, but the owner is fully occupied delivering services
- **Revenue at stake:** Significant. Most expert-led service businesses report that their best clients come from referrals or inbound from content. Ghost systematizes the content part.
- **Willingness to pay:** $249/month. Equivalent to 3% of one typical client's monthly retainer.

### Tertiary ICP: The Career-Transition Professional
- **Who:** Senior professional making a deliberate career move (executive to fractional, corporate to consulting, pivot to a new industry)
- **Pain:** LinkedIn presence during a transition is critical and often the most neglected element of the process
- **Willingness to pay:** $149/month starter tier. Duration: 6–12 months.

---

## 5. The Product

### Onboarding (One-Time, 30 Minutes)
The client completes a structured Voice & Topics questionnaire — either a Google Form or a Typeform. It covers:
- Professional background and expertise areas
- 5 topics they could talk about for an hour
- 3 clients or projects they're proud of (anonymized if needed)
- Tone preferences (data-driven, storytelling, contrarian, educational)
- 3 posts they admire from other creators (style benchmarks)
- Things they will not post about
- Approval preference: auto-publish or weekly review

This questionnaire is processed once by Claude to generate a **Voice Profile** stored in Supabase — a structured document that governs every post written for this client.

### Weekly Autonomous Loop
```
Monday 6am:
  → Gemini researches top 5 industry signals from the past 7 days
    (trade press, LinkedIn trending topics in client's field, patent filings,
     major company announcements in the niche)
  → Claude synthesizes signals + Voice Profile → generates 5 post drafts
    (mix: 2 insight posts, 1 opinion, 1 storytelling hook, 1 engagement question)
  → Google Drive: weekly content calendar deposited to client's shared folder
  → Telegram to client: "Your week's content is ready for review — [Drive link]"

Wednesday 8am:
  → If no client edits detected: posts auto-scheduled for Mon–Fri at optimal times
  → If edits detected: post Google Drive version pushed to scheduler

Mon–Fri 8am–9am:
  → IFTTT or Buffer API publishes scheduled post
  → Supabase logs post performance (impressions, engagement) via LinkedIn API

Sunday 7am:
  → Claude generates weekly performance report: top post, engagement rate, follower delta
  → Report deposited to Google Drive
  → Client billed monthly via Stripe (handled automatically)
```

### Tiers

| Tier | Price | Posts/Week | Platforms | Reporting |
|------|-------|-----------|-----------|-----------|
| Solo | $149/mo | 3 | LinkedIn only | Weekly digest |
| Pro | $199/mo | 5 | LinkedIn + X | Weekly + monthly analytics |
| Presence | $299/mo | Daily (7) | LinkedIn + X + threads | Full dashboard + quarterly voice refresh |

---

## 6. Technical Architecture

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Voice profile | Claude + Supabase | Client persona and topic guidance |
| Industry research | Gemini Flash (free tier) | Weekly signal gathering |
| Post generation | Claude API | Voice-matched draft creation |
| Content calendar | Google Drive API | Client review workflow |
| Scheduling | IFTTT webhooks + Buffer API | Post publication |
| Notifications | Telegram bot | Weekly calendar delivery |
| Billing | Stripe | Monthly subscription |
| Dashboard | Vercel + Supabase | Client portal (optional) |
| Analytics | LinkedIn API (basic) | Performance tracking |

### API Cost Model
Per client per month:
- Gemini research calls: ~30 (weekly × 4 × batched) ≈ free tier
- Claude API for 20 posts × ~1,500 tokens each: ~30,000 tokens = ~$0.09
- Claude for weekly reports × 4: ~$0.03
- **Total API cost per client per month: ~$0.15**
- At $199/month average revenue: **99.9% gross margin on API costs**

Real COGS per client: Supabase + Vercel proration + Stripe fees ≈ $8/client/month
**Net margin at 50 clients: ~96%**

---

## 7. Go-to-Market Strategy

Ghost requires no SEO, no ad spend, and no content marketing. The acquisition strategy is direct outreach on the exact platform the product serves.

### Phase 1 (Days 1–10): Build and internal test
Run Ghost on a test LinkedIn profile to validate output quality. Generate 3 weeks of posts. Evaluate voice consistency, engagement quality, and scheduling reliability.

### Phase 2 (Days 11–20): Founder beta, 3 free clients
Find 3 solopreneurs on LinkedIn who match the ICP and post inconsistently. Offer 30 days free in exchange for honest feedback and a testimonial. The outreach message:

> "I noticed you post sporadically on LinkedIn — your content is good but your feed goes quiet for weeks at a time. I've built an AI system that runs your LinkedIn for you. Your only job is a 30-minute questionnaire. Want to try it free for a month?"

Conversion rate on this message: expected 20–30% given the directness and the free offer.

### Phase 3 (Days 21–45): Convert betas, launch paid, first 5 clients
Convert 2–3 betas to paid. Direct outreach to 50 more ICPs on LinkedIn (5 per day). Target: 5 paying clients by day 45 = $750–1,000 MRR.

### Phase 4 (Days 46–90): Referral + content
Every client whose followers grow or who gets an inbound lead from Ghost content will mention it when asked. A simple referral offer: "Refer a colleague, get one month free." At 5 clients, each referral loop can drive 1–2 new clients per month organically.

### Phase 5 (Day 90+): Productize at scale
At 20+ clients, build the self-serve onboarding portal on Vercel. Product Hunt launch. Indie Hackers build-in-public thread. At this point the product sells from the product itself.

---

## 8. Revenue Model and Financial Projections

### Assumptions
- Average subscription: $199/month
- Month 1: 3 beta (free) + 2 paying = $398 MRR
- Month 2: 8 paying clients = $1,592 MRR
- Month 3: 15 paying clients = $2,985 MRR
- Churn: 5%/month (lower than Sentinel — social presence is stickier than monitoring)
- COGS: ~$8/client/month

| Month | Clients | MRR | COGS | Net |
|-------|---------|-----|------|-----|
| 1 | 5 (2 paid) | $398 | $40 | $358 |
| 2 | 8 | $1,592 | $64 | $1,528 |
| 3 | 15 | $2,985 | $120 | $2,865 |
| 6 | 35 | $6,965 | $280 | $6,685 |
| 12 | 80 | $15,920 | $640 | $15,280 |

Daily revenue at month 3 (15 clients): **$99/day**. Exceeds $20/day target by day 30.

---

## 9. Biggest Risk and Mitigation

### Risk 1: LinkedIn API restrictions
LinkedIn's API limits what third-party apps can post on behalf of users. The full LinkedIn Marketing API requires approval and is restricted to verified partners.

**Mitigation:** Two paths:
1. Use Buffer's LinkedIn integration — Buffer has full API access and an IFTTT connection. Ghost schedules to Buffer; Buffer posts to LinkedIn. Adds one hop but is fully legal and reliable.
2. For power users, use LinkedIn's official "Schedule Post" feature via automation of the web interface through the client's own session. More fragile but doesn't require API partner status.

This is the most significant technical risk and must be validated in Phase 1 before any client acquisition.

### Risk 2: AI content detection and algorithm penalties
LinkedIn's algorithm in 2026 is increasingly adept at identifying AI-generated content and deprioritizing it. A flood of generic AI posts has made human-voiced, specific, experience-grounded content more valuable.

**Mitigation:** Ghost's differentiation is *voice matching*, not content volume. The Voice Profile questionnaire extracts real stories, real opinions, real expertise. Claude's job is to write in the client's voice using their actual experiences — not to generate generic thought leadership. Posts are validated against a quality rubric before scheduling: specific > generic, opinionated > neutral, personal > abstract.

### Risk 3: Client over-dependence, then churn when they want "real" engagement
Some clients will want the engagement management (responding to comments, liking replies) that Ghost doesn't handle. When their post gets 15 comments and they have to respond manually, they may feel the product is incomplete.

**Mitigation:** Clearly scoped in onboarding: "Ghost writes and publishes. You engage." Position the engagement as the one thing that must be human — the authenticity layer. Clients who understand this upfront have low churn. Consider adding a Presence tier that includes 30 minutes/week of AI-drafted comment responses for the client to review and post.

---

## 10. Why Now (The 2026 Timing Argument)

1. **Personal brand ROI is measurable and documented.** Windmill Growth data shows 10–20x ROI within 6 months for B2B founders using consistent LinkedIn content. Solopreneurs increasingly treat LinkedIn as a lead-gen channel with a known return, which makes Ghost a verifiable ROI purchase rather than a "nice to have."

2. **AI-generated content has flooded LinkedIn, raising the quality bar.** Paradoxically, the flood of generic ChatGPT posts in 2023–2024 has made genuinely voice-matched, specific content more valuable and more visible algorithmically. The algorithm now actively rewards authenticity signals. Ghost's voice-matching approach is positioned precisely for this dynamic.

3. **Ghostwriting is culturally normalized.** The stigma around ghostwriting has essentially disappeared. Every major LinkedIn influencer uses one. Solo practitioners increasingly understand that a ghostwriter is a productivity tool, not a deception. "I had help writing this" is no longer controversial.

4. **The fractional economy is accelerating.** The number of fractional executives, independent consultants, and portfolio-career professionals is growing rapidly as companies increasingly hire for outcomes rather than roles. These professionals live or die by their professional reputation, and LinkedIn is where that reputation is built at scale.

---

## 11. Non-Obvious Insight

**The product's real value isn't the content — it's the consistency.**

Research consistently shows that LinkedIn's algorithm rewards posting frequency with exponentially better distribution. Founders who post 5+ times per week for 6+ months see 10x the results of those who post 1–2 times per week. The problem isn't post quality — it's the drop-off after week 3.

Ghost's competitive moat isn't writing quality (human ghostwriters write better). It's reliability. Ghost posts every week, every month, for as long as the client pays. No burnout, no sick days, no "I've been too busy." The compounding effect of 12 months of consistent posting at $199/month is worth multiples of 3 months of excellent posting at $3,000/month.

This means Ghost should sell the *commitment* as much as the *content*. The pitch isn't "better posts" — it's "you will post consistently for the next 12 months without ever having to think about it again."

---

## 12. Maintenance and Monitoring (Operational Model)

### What Maeve Runs Autonomously
- Weekly Gemini research runs for all active clients
- Post generation queue (batched Sunday night for the week ahead)
- Google Drive calendar deposits
- Telegram weekly notification to each client
- IFTTT/Buffer schedule pushes
- Monthly Stripe billing
- Performance data pull from LinkedIn API

### What Requires Human Attention (Derek)
- **New client onboarding questionnaire review** (~30 min/client, one time)
- **Client support messages** (estimated 1 message/client/month, ~10 min each)
- **Quality spot-checks** (review 2–3 posts/client/month, ~30 min total per client)
- **LinkedIn API issue resolution** (when Buffer or the posting chain breaks)

**Total estimated weekly time at 15 clients: 2–3 hours/week**

### Infrastructure Cost at 20 Clients
| Service | Monthly Cost |
|---------|-------------|
| Vercel Pro | $20 |
| Supabase Pro | $25 |
| Claude API | ~$5 |
| Buffer (for scheduling) | $18 |
| Gemini API (free tier) | $0 |
| Stripe fees (~2.9%) | ~$115 |
| Total COGS | ~$183/month |
| Revenue (20 × $199) | $3,980/month |
| **Net margin** | **95.4%** |

---

## 13. Build Requirements

### Phase 1: Core Engine (Days 1–7)
- [ ] Voice Profile questionnaire design (Google Form)
- [ ] Claude voice-matching prompt engineering (critical — most important build task)
- [ ] Gemini research pipeline (weekly industry signal gathering per niche)
- [ ] Post generation engine (5 posts/week per client, batched)
- [ ] Google Drive API integration (calendar deposit)
- [ ] Telegram notification bot (weekly calendar delivery)
- [ ] Buffer API integration for scheduling

### Phase 2: Client Infrastructure (Days 8–14)
- [ ] Supabase schema (clients, voice profiles, post queue, performance logs)
- [ ] Stripe subscription setup (3 tiers)
- [ ] Vercel minimal frontend (client status page, content calendar view)
- [ ] Post quality rubric (automated pre-publish check)
- [ ] LinkedIn performance data ingestion (basic impressions/engagement)

### Phase 3: Launch Preparation (Days 15–20)
- [ ] Test run on 3 internal profiles for 2 weeks
- [ ] Voice matching quality validation
- [ ] Buffer/LinkedIn posting reliability validation
- [ ] Outreach template for beta client acquisition
- [ ] Client onboarding documentation

**Total build time: 14–21 days to beta-ready. First paying client possible by day 25.**

---

## 14. Decision Criteria for Proceeding

Proceed to build if:
- Buffer API access is confirmed as the posting mechanism (this must be tested in Phase 1 before client acquisition begins)
- Voice questionnaire quality is validated on a real LinkedIn profile with 500+ connections
- Derek is willing to handle 1–2 hours/week of light oversight at launch

Do not proceed if:
- LinkedIn API restrictions make reliable automated posting untenable without a Buffer or similar intermediary
- The voice matching quality in prototype testing doesn't clear a bar where posts are indistinguishable from manually written content

---

## 15. Sentinel + Ghost Combined Strategy

Running both products simultaneously is viable and synergistic:

- **Sentinel** serves B2B professionals who monitor their competitive landscape
- **Ghost** serves the same professionals who want to build their LinkedIn presence
- A Sentinel client monitoring 10 competitors is *precisely* the ICP who also wants to be seen as a thought leader commenting on those competitive moves
- Combined offering: "Know what's changing in your market. Be the one talking about it first."
- Combined ARPU: $20 (Sentinel Analyst) + $199 (Ghost Pro) = $219/month per fully activated client

The two products share the same infrastructure (Supabase, Vercel, Claude, Stripe, Telegram) and the same target customer. Building both in parallel adds approximately 30% more build time but captures a customer who pays 10x more than a Sentinel-only subscriber.

---

*Document prepared by Maeve. Research sourced from Windmill Growth LinkedIn State of Ghostwriting 2026, Concurate LinkedIn Agency rankings, Linkboost AI LinkedIn marketing analysis, SalesBread ghostwriter database, and BetterCloud SaaS statistics (April 2026).*
