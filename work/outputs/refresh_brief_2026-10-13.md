# Refresh Scout — weekly brief (2026-10-13)

Top-10 refresh candidates (decision-support only; directional signals, not causal claims). Human approval required — this agent cannot publish anything.

Portfolio: 30000 pages scored | base declining rate: 0.5421 | P@10 vs declining label: 0.2

| rank | page | score | reasons | signals (observed) | suggested action |
|---|---|---|---|---|---|
| 1 | `content_9532f197bb…` | 0.941 | page_one_decay_risk|low_engagement_visible_page | impr90d=309192, upd_age=104d, pos=2.0, ctr=0.87% | refresh |
| 2 | `content_4d1fe5b32d…` | 0.935 | page_one_decay_risk|low_engagement_visible_page | impr90d=97999, upd_age=104d, pos=2.5, ctr=0.52% | refresh |
| 3 | `content_07f2e7a6f3…` | 0.934 | page_one_decay_risk|low_engagement_visible_page | impr90d=101078, upd_age=104d, pos=2.7, ctr=0.85% | refresh |
| 4 | `content_e5ae436f9a…` | 0.934 | page_one_decay_risk|low_ctr_visible_page|low_engagement_visible_page | impr90d=117741, upd_age=104d, pos=3.0, ctr=0.45% | refresh_and_review_ctr |
| 5 | `content_3430a8b945…` | 0.934 | page_one_decay_risk|low_ctr_visible_page|low_engagement_visible_page | impr90d=152617, upd_age=104d, pos=3.3, ctr=0.29% | refresh_and_review_ctr |
| 6 | `content_cbd9311830…` | 0.933 | page_one_decay_risk|low_ctr_visible_page|low_engagement_visible_page | impr90d=145292, upd_age=104d, pos=3.3, ctr=0.46% | refresh_and_review_ctr |
| 7 | `content_9c195417f6…` | 0.933 | page_one_decay_risk|low_engagement_visible_page | impr90d=79146, upd_age=104d, pos=2.5, ctr=0.73% | refresh |
| 8 | `content_ba2acb4ebd…` | 0.932 | page_one_decay_risk|low_engagement_visible_page | impr90d=142072, upd_age=104d, pos=3.6, ctr=0.83% | refresh |
| 9 | `content_79b2565407…` | 0.931 | page_one_decay_risk|low_ctr_visible_page|low_engagement_visible_page | impr90d=148737, upd_age=104d, pos=3.7, ctr=0.48% | refresh_and_review_ctr |
| 10 | `content_adddad3925…` | 0.931 | page_one_decay_risk|low_engagement_visible_page | impr90d=129239, upd_age=104d, pos=3.6, ctr=0.55% | refresh |

## Guardrail screens
- Injection flags: 0 (none — no embedded instructions followed)
- Label-derived columns excluded from scoring inputs; used only to derive the eval metric above.
- `avg_position == 0` treated as no-data throughout.

_Uncertain cases:_ pages with conflicting/missing signals keep the `general_refresh_review` code and `monitor` action rather than a confident pick.
