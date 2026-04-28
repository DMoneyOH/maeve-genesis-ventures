# Pulse — Automated Niche Intelligence Newsletters
## MaeveGenesis Venture Business Case
**Prepared by:** Maeve (AI Infrastructure Platform)
**Date:** 2026-04-28
**Status:** Pre-seed concept — awaiting backer decision
**Repo:** https://github.com/DMoneyOH/maeve-genesis-ventures

---

## Executive Summary

Pulse is an AI-operated subscription newsletter service that monitors a specific professional niche 24/7, synthesizes signals from dozens of sources, and delivers a weekly briefing to paid subscribers. The product is curation and interpretation, not content creation. Maeve watches things professionals don't have time to watch and charges for that vigilance.

Unlike general AI newsletters or broad tech digests, Pulse targets narrow professional niches where practitioners pay for pre-filtered intelligence: municipal bond attorneys tracking SEC rule changes, commercial drone operators monitoring FAA airspace updates, food safety compliance officers watching FDA guidance shifts. The narrower the niche, the higher the willingness to pay and the lower the competition.

**Target revenue:** $500/month MRR by day 45. $2,000+/month by day 90.
**Build time to prototype:** 5 days.
**Ongoing human involvement post-launch:** Near zero after niche selection.

---

## 1. The Problem

Every professional niche generates more signal than any practitioner can track. Regulatory bodies publish updates. Trade publications run stories. Research papers cite new findings. Competitor companies file patents. Job boards signal industry hiring trends. Conference agendas telegraph where the field is heading.

The practitioners who stay current gain competitive advantage. The ones who fall behind make expensive mistakes — missed compliance deadlines, outdated advice to clients, failure to spot emerging opportunities.

The existing solutions are inadequate:

- **Google Alerts** delivers unfiltered noise. Practitioners get dozens of irrelevant hits per keyword.
- **Trade publications** cover niches broadly but require reading multiple sources daily.
- **Industry associations** publish newsletters weekly or monthly at best, often behind paywalls, always written by humans with editorial lag.
- **General AI newsletters** (The Rundown, TLDR) cover technology broadly — useless to a food safety attorney or an FAA drone compliance specialist.

The gap: a continuously monitored, AI-synthesized briefing that covers exactly one professional niche in depth, delivered weekly, priced for individual practitioners rather than enterprises.

---

## 2. Market Sizing

### TAM
The global newsletter and email marketing industry was valued at $7.5 billion in 2025 (Statista) and growing at 13.3% CAGR. The paid newsletter segment specifically — where readers pay directly for curated content — is growing faster at approximately 25% CAGR per Substack's published figures, driven by the creator economy shift. Total paid newsletter TAM: approximately **$1.2 billion by 2026**.

### SAM
Professional niche newsletters targeting B2B practitioners represent the highest ARPU segment of the paid newsletter market. Practitioners in regulated or complex industries — legal, compliance, finance, healthcare, engineering — pay $50–500/year for curated intelligence. The SAM for AI-generated professional niche newsletters is nascent but growing rapidly; conservatively estimated at **$150M** based on adjacent market comparables (Politico Pro subscribers at $3,000/year, Bloomberg Law at $500/year, specialized legal newsletters at $200–400/year).

### SOM
Year-one target: 3 niches × 150 subscribers each at $12/month = 450 subscribers = **$5,400/month MRR**. This requires finding 150 paying subscribers per niche — a realistic target given tight community concentration in professional niches (most have a single dominant Slack group, LinkedIn community, or annual conference).

---

## 3. Competitive Landscape

### The Rundown AI / TLDR
**Pricing:** Free (ad-supported) or $8/month
**Weakness:** Covers AI broadly. No depth in any specific professional niche. The breadth is the weakness — a drone compliance attorney learns nothing actionable from a general AI newsletter.

### Politico Pro
**Pricing:** $3,000–10,000/year (enterprise)
**Weakness:** Enterprise pricing excludes individual practitioners. Covers policy broadly rather than narrow professional niches. Human editorial team means lag and editorial bias.

### Bloomberg Law / Westlaw Alerts
**Pricing:** $500–2,000/year
**Weakness:** Legal-only, document-retrieval-focused rather than synthesized intelligence. No interpretation layer — delivers documents, not analysis.

### Niche Human-Written Newsletters (e.g., Matt Levine's Money Stuff, Lenny's Newsletter)
**Pricing:** $0–200/year
**Weakness:** Single author, single perspective, human production rate. Cannot cover more than one niche. Extremely difficult to replicate at scale. Pulse's advantage is running 10 niches simultaneously with the same infrastructure cost.

**White space:** No product exists at the $10–20/month price point that provides AI-synthesized, niche-specific professional intelligence with daily monitoring and weekly delivery. Pulse owns this position.

---

## 4. Ideal Customer Profile

### Primary ICP: The Solo or Small-Firm Compliance Professional
- **Who:** Independent compliance consultant, solo regulatory attorney, or compliance officer at a company under 100 employees
- **Pain:** Must stay current on regulatory changes in their specific domain but cannot justify enterprise intelligence tools at $3,000+/year
- **Job to be done:** "Tell me every relevant regulatory update, enforcement action, and industry development in my specific compliance domain this week so I can advise clients accurately"
- **Willingness to pay:** $15/month is trivial — one hour of their billing rate. The math is obvious.
- **Niche examples:** HIPAA compliance, FDA food safety, FAA drone regulations, FTC advertising law, OSHA safety standards

### Secondary ICP: The Independent Professional in a Complex Industry
- **Who:** Independent financial advisor, specialized insurance broker, independent engineer in a regulated discipline
- **Pain:** Industry moves fast. Staying current on best practices, regulatory changes, and market developments is a full-time job within a full-time job.
- **Willingness to pay:** $12–20/month. Especially high if the newsletter covers their exact specialty.

### Tertiary ICP: The Corporate Practitioner Without Enterprise Tool Budget
- **Who:** Mid-level attorney, compliance analyst, or policy professional at a mid-sized company whose department doesn't have the budget for Politico Pro or Bloomberg Law
- **Willingness to pay:** $15/month on a personal credit card, expensed or not.

---

## 5. The Product

### Niche Selection Criteria (Maeve-applied)
The right niche has five characteristics:
1. A regulatory or standards body that publishes updates regularly (FDA, FAA, SEC, OSHA, FTC, CFPB, EPA, state bar associations)
2. A professional community with a clear gathering point (LinkedIn group, Slack, annual conference)
3. Active discussion volume — enough signals to synthesize weekly
4. No dominant existing newsletter at under $25/month
5. Practitioners who bill hourly and for whom staying current is a professional requirement

**Target niches for launch:**
- FAA drone/UAS compliance (pilot community, operators, operators' legal counsel)
- FDA food safety compliance (food safety officers, FSMA compliance consultants)
- FTC advertising and privacy law (solo and small-firm marketing attorneys, in-house counsel at DTC brands)

### Weekly Autonomous Loop
```
Daily (2am):
  → Gemini scrapes 15–25 sources per niche:
    RSS feeds (regulatory bodies, trade press, law firm blogs)
    Reddit communities (r/drones, r/foodsafety, r/legaladvice filtered)
    LinkedIn trending posts in niche communities
    Google News alerts via RSS
    Federal Register API (for regulatory niches)
    Patent filing feeds (for technology niches)
  → New items stored in SQLite with source, date, content hash
  → Items tagged by significance: regulatory_change, enforcement_action,
    industry_trend, research, opinion

Sunday night:
  → Claude synthesizes week's signals into structured briefing:
    Top story (most significant development)
    Regulatory updates (any rule changes, guidance, enforcement)
    Industry news (3–5 items with 2-sentence analysis each)
    What to watch (forward-looking signals)
    Quick links (5 items not covered in depth)
  → Briefing quality-checked against word count and section completeness
  → Sent via Gmail API to all subscribers for that niche

Monthly:
  → Stripe billing processed automatically
  → Subscriber count reported to Telegram
  → Unsubscribers removed from send list
```

### Sample Briefing Excerpt (FAA Drone Compliance)

```
PULSE: FAA DRONE COMPLIANCE BRIEF
Week of April 28, 2026

TOP STORY
FAA published a notice of proposed rulemaking for Remote ID enforcement
penalties, raising maximum fines from $1,100 to $4,500 per violation.
Comment period opens May 15. If you operate commercially without Remote
ID compliance, this is the week to audit your fleet.

REGULATORY UPDATES
• LAANC expansion: 12 new airports added to authorization network,
  including 3 in Class B airspace. Full list and effective date: [link]
• FAA Safety Team (FAAST) published updated guidance on night operations
  under Part 107.29 waivers — notable change to documentation requirements.

INDUSTRY NEWS
• Amazon Prime Air received expanded operational authorization in 5 new
  metro areas. Signals accelerating commercial BVLOS regulatory pathway.
• DJI's new Enterprise firmware update affects Remote ID broadcasting
  for Matrice 350 RTK — update required by June 1 for Part 107 compliance.
• [3 more items...]

WHAT TO WATCH
The proposed urban air mobility (UAM) corridor framework circulating at
FAA is expected to reach NPRM stage Q3 2026. Operators in metro markets
should begin tracking now.
```

### Pricing
| Tier | Price | Delivery | Archive |
|------|-------|----------|---------|
| Subscriber | $12/mo | Weekly email | 90 days |
| Professional | $19/mo | Weekly email + Telegram alerts for breaking changes | Full archive |

---

## 6. Technical Architecture

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Source monitoring | Python + feedparser + requests | RSS, Federal Register API, Reddit API |
| Storage | SQLite | Signal deduplication and history |
| Synthesis | Claude API | Weekly briefing generation |
| Delivery | Gmail API | Newsletter sending |
| Subscriptions | Substack or Beehiiv free tier | Subscriber management + payment |
| Breaking alerts | Telegram bot | Professional tier notifications |
| Scheduling | systemd timer | Daily scrape, Sunday synthesis |
| Billing | Beehiiv Stripe integration or direct Stripe | Monthly subscriptions |

### API Cost Model
Per niche per month:
- Claude API for 4 weekly syntheses × ~3,000 tokens each: ~12,000 tokens = ~$0.036
- At $12/month × 150 subscribers = $1,800/month revenue
- **API cost per niche per month: < $1**
- Gross margin: >99% on AI costs

Real COGS: Beehiiv Pro ($42/month for up to 1,000 subscribers) or Gmail API (free under 500/day) + Supabase + Stripe fees
Net margin at 450 subscribers across 3 niches: approximately 97%

---

## 7. Go-to-Market Strategy

### No SEO Required
Pulse's entire distribution strategy is community-based.

**Phase 1 (Days 1–7): Build and test**
Build the pipeline for one niche (FAA drone compliance). Generate 3 sample issues. Validate quality against practitioner standards — share with 5 practitioners in the niche for feedback before launch.

**Phase 2 (Days 8–21): Free trial seeding**
Post in niche communities with a free 4-week trial offer:
- r/drones, r/dji, r/uavs (FAA niche)
- LinkedIn groups for the specific compliance community
- The dominant Slack or Discord for the niche
One post: "I built an AI that monitors FAA regulatory changes and sends a weekly briefing. Free for the first month — here's a sample issue."

**Phase 3 (Days 22–45): Convert to paid + launch niches 2 and 3**
At 4-week mark, trial subscribers convert to paid ($12/month) or cancel. Target 30% conversion rate = ~45 paying subscribers per niche from 150 trial signups. Simultaneously seed niches 2 and 3 using the same pattern.

**Phase 4 (Day 45+): Referral and compounding**
Every issue footer: "Forward this to a colleague — they get their first issue free." Professional communities are tight; one respected practitioner recommending Pulse drives 5–10 new subscribers.

---

## 8. Revenue Model and Financial Projections

### Assumptions
- 3 niches at launch
- 150 trial signups per niche (conservative for a tight professional community)
- 30% trial-to-paid conversion = 45 paying subscribers per niche
- Average subscription: $14/month
- Monthly churn: 5% (professional tools have lower churn than consumer)

| Month | Niches | Subscribers | MRR | Net (after COGS) |
|-------|--------|-------------|-----|------------------|
| 1 | 1 | 20 paid | $280 | $238 |
| 2 | 2 | 65 paid | $910 | $868 |
| 3 | 3 | 130 paid | $1,820 | $1,760 |
| 6 | 5 | 320 paid | $4,480 | $4,346 |
| 12 | 8 | 700 paid | $9,800 | $9,506 |

Daily revenue at month 3 (130 subscribers): **$60/day**. Exceeds target by day 60.

---

## 9. Biggest Risk and Mitigation

### Risk 1: Content quality fails the practitioner standard
A drone compliance attorney who receives a Pulse briefing with a factual error about FAA regulations will unsubscribe and warn their community. One bad issue in a tight professional network can destroy the subscriber base.

**Mitigation:** The synthesis prompt includes explicit instructions to cite sources for all regulatory claims, flag uncertainty clearly, and never extrapolate beyond what sources state. A pre-send quality check compares claimed regulatory citations against the source URLs actually scraped that week. Any issue that cannot cite every regulatory claim is held for manual review.

### Risk 2: Niche is too small
Some niches that seem viable have only 500 total practitioners globally — not enough to reach 150 subscribers.

**Mitigation:** Niche viability pre-screening before building. Required: active LinkedIn group with 2,000+ members OR active subreddit with 5,000+ members OR annual conference with 500+ attendees. Maeve runs this screen before any pipeline is built.

### Risk 3: Free alternatives emerge
A well-funded player (Bloomberg, Politico) could launch a cheaper niche product.

**Mitigation:** Pulse's advantage is speed and specificity. A media company taking 6–12 months to build a product loses to Pulse already operating in the niche. At 3 years in, 8 niches with strong subscriber bases and community integration is a defensible position.

---

## 10. Why Now (2026 Timing)

1. **The paid newsletter market has hit mainstream.** Substack crossed 5 million paid subscribers in 2025. The cultural norm of paying for curated information is established — practitioners no longer balk at $15/month for a professional newsletter.

2. **AI synthesis quality crossed the practitioner threshold.** Claude's ability to synthesize regulatory documents accurately and write professional-grade analysis reached a quality level in 2025 that makes AI-generated compliance briefings credible to practitioners. This was not true in 2023–2024.

3. **Regulatory complexity is accelerating.** Every major agency (FAA, FDA, FTC, SEC, CFPB) published a record number of rules, proposed rules, and guidance documents in 2025. The monitoring burden on individual practitioners has never been higher. The timing is structural, not cyclical.

---

## 11. Non-Obvious Insight

**The real product is peace of mind, not information.**

The practitioners who pay for Pulse aren't paying because they can't find the information elsewhere. They're paying because Pulse removes the anxiety of wondering whether they missed something important. The unsubscribe trigger isn't "I found a better information source." It's "I haven't needed this for three months."

This means retention is maximized not by increasing volume but by maintaining the signal quality that makes practitioners trust they won't miss a critical development. One important catch per month — a regulatory change, an enforcement action, an emerging trend — justifies the subscription for a full year.

Pulse's growth strategy should lean into this: testimonials that say "I found out about X from Pulse two weeks before my clients asked me about it" convert better than feature lists. The peace of mind angle is also what drives referrals — practitioners recommend Pulse to colleagues not because the newsletter is well-written but because it made them look prepared.

---

## 12. Build Requirements

### Phase 1: Core Pipeline (Days 1–5)
- [ ] RSS/feed scraper for 15–25 sources per niche
- [ ] Federal Register API integration for regulatory niches
- [ ] SQLite deduplication and signal storage
- [ ] Claude synthesis prompt (regulatory-grade citation requirements)
- [ ] Gmail API delivery
- [ ] systemd timer for daily scrape + Sunday synthesis

### Phase 2: Subscriber Infrastructure (Days 6–10)
- [ ] Beehiiv free tier setup (subscriber management, basic analytics)
- [ ] Stripe subscription via Beehiiv
- [ ] Telegram bot for Professional tier breaking alerts
- [ ] Unsubscribe handling

### Phase 3: Launch Prep (Days 11–14)
- [ ] 3 sample issues generated and practitioner-reviewed
- [ ] Community seeding posts drafted
- [ ] Free trial onboarding sequence

**Total build time: 14 days to launch-ready. First paying subscriber possible by day 21.**

---

## 13. Decision Criteria for Proceeding

Proceed if:
- Niche selection passes the viability screen (2,000+ LinkedIn group OR 5,000+ subreddit)
- 3 sample issues pass practitioner review (share with 5 practitioners before launch)
- Beehiiv or equivalent handles subscriber management without code

Do not proceed if:
- Sample issue quality doesn't meet practitioner standard on first test
- Target niche has an existing dominant newsletter at under $20/month

---

*Document prepared by Maeve. Research sourced from Statista newsletter market data, Substack published subscriber figures, Politico Pro and Bloomberg Law pricing pages, and Federal Register API documentation (April 2026).*
