# citation_check.md — every reference in `paper/latex/references.bib` and how it was confirmed

Checked on 15 November 2026 with scripts in a scratch folder (not in the repository):

- **Crossref**: `https://api.crossref.org/works/<DOI>`: title, authors, year, venue, volume, pages compared with the entry.
- **DataCite**: `https://api.datacite.org/dois/<DOI>` for the Zenodo DOI (Zenodo DOIs are not in Crossref).
- **Semantic Scholar**: `graph/v1/paper/search`, unauthenticated, at most 1 request per second. Most
  requests returned HTTP 429 (rate limit), also on a slower second pass. Five returned results; two of them
  matched an entry (Stamer 2024, Verschuur et al. 2022). So Semantic Scholar confirmed almost nothing, and Crossref, DataCite, OpenAlex or the publisher's page were
  used instead, as the brief allows.
- **OpenAlex**: search and abstracts (`api.openalex.org/works`) to find candidates and read abstracts for the
  claims made about new works.
- **Page**: an HTTP GET of the URL returned status 200 and, where the page has one, the expected title.
- **Earlier pass**: the work was opened in the research passes of 13 and 14 November 2026 (`research/LITERATURE.md`,
  `research/STEP1_RESEARCH.md`, `paper/NUMBERS.md`). For grey literature with no DOI this is the main evidence;
  the GET only shows the address still resolves.

No candidate was dropped for failing a check: every work considered for addition was confirmed. Searches that
could not run (Semantic Scholar for Middle Corridor academic work) were replaced by OpenAlex searches.

## Already in the paper (kept; none found wrong)

| Key | Reference | Check | Result |
|---|---|---|---|
| adb2023ais | Kim, Basu Das, Pundit, Magnata, Mariasingham, Chico (2023), ADB Briefs 244 | Crossref 10.22617/BRF230082-2 | Title, year, publisher match. Crossref splits one author as "Basu, Sanchita"; kept "Basu Das" as on the ADB page. |
| adb2024tradeflows | ADB (2024), Trade Flows and Transport Routes in the CAREC Region Amid External Shocks | Page (PDF, 200) + earlier pass | Resolves. |
| aktau2022strategy | Aktau port, Development strategy 2022 to 2032, p. 7 | Page (PDF, 200) + earlier pass (re-opened 14 Nov) | Resolves. |
| arslanalp2019big | Arslanalp, Marini, Tumbarello (2019), IMF WP 19/275 | Crossref | Match. |
| arslanalp2021tracking | Arslanalp, Koepke, Verschuur (2021), IMF WP 21/225 | Crossref | Match. |
| arslanalp2025nowcasting | Arslanalp et al. (2025), IMF WP 25/93 | Crossref | Match (Crossref writes "Mo Choi, Seung"; the paper's "Choi, Seung Mo" is the same person). |
| arslanalp2026nowcasting | Arslanalp et al. (2026), IMF WP 26/99 | Crossref | Match. |
| arxiv2023genai | arXiv blog, 31 Jan 2023 | Page (200, title matches) | Match. |
| carec2022cpmm | CAREC CPMM Annual Report 2022 | Page (PDF, 200) + earlier pass | Resolves. |
| carec2024cpmm | CAREC CPMM Annual Report 2024 | Page (PDF, 200) + earlier pass | Resolves. |
| cerdeiro2020world | Cerdeiro, Komaromi, Liu, Saeed (2020), IMF WP 20/57 | Crossref; OpenAlex | Match. |
| ebrd2023sustainable | EBRD (2023), Sustainable transport connections between Europe and Central Asia | Page (PDF, 200) + earlier pass | Resolves. |
| gfw2026vendor | Global Fishing Watch, Data vendor transition | Page (200, title matches) | Match. |
| gondauri2026bsmcii | Gondauri, Guramishvili (2026), BSMCII, Zenodo | DataCite 10.5281/zenodo.21282793 | Title, both authors, 2026, Zenodo match. |
| jia2019estimating | Jia, Prakash, Smith (2019), IJSTL 11(1) 25-40 | Crossref | Match. Abstract only. |
| lechthaler2022kiel | Lechthaler, Stamer (2022), SUERF Policy Brief 418 | Page (200, title matches) | Match. |
| oecd2023realising | OECD (2023), Realising the Potential of the Middle Corridor | Crossref 10.1787/635ad854-en | Match. |
| oecd2025enhancing | OECD (2025), Enhancing the Competitiveness of the Trans-Caspian Transport Corridor in Central Asia | Crossref 10.1787/f261e7fa-en | Match. |
| paolo2024satellite | Paolo et al. (2024), Nature 625, 85-91 | Crossref | Match (all ten authors). |
| portwatch2026dailyports | IMF PortWatch, Daily_Ports_Data item | ArcGIS item JSON (200) + earlier pass | Resolves. Note now names Kpler, as the FAQ asks. |
| portwatch2026faq | IMF PortWatch FAQ, ArcGIS item 640b69a4... | ArcGIS item JSON (200) + earlier pass (re-opened 14 Nov) | Resolves. |
| ssrn2026genai | SSRN policy on generative AI | Page (200, title matches) | Match. |
| stamer2024thinking | Stamer (2024), IJF 40(4) 1336-1358 | Crossref; S2 | Match. Abstract only. |
| titr2026chart | TITR association home-page chart | Page (200, title "TITR - Trans-Caspian International Transport Route") + earlier pass | Resolves; chart values not re-read today. |
| verschuur2021global | Verschuur, Koks, Hall (2021), PLoS ONE 16(4) e0248818 | Crossref | Match. |
| worldbank2023middle | World Bank (2023), Middle Trade and Transport Corridor | Page (OKR handle, 200) + earlier pass | Resolves. |
| worldbank2026integration | World Bank (2026), Integration: World-Class Trade Logistics Along the Trans-Caspian Transport Corridor | Page (200, title matches) | Match. |
| wu2026caspianshock | Wu (2026), EPINOVA Policy Brief PB-44 | Crossref 10.67037/epinova.pb.2026.044 | Match. |

## Added in this version

| Key | Reference | Check | What the paper says about it, and its basis |
|---|---|---|---|
| verschuur2022ports | Verschuur, Koks, Hall (2022), Nature Communications 13, 4351 | Crossref; S2 (one of the three searches that ran) | PortWatch's port database grew from a model of port-level trade flows. Basis: `research/LITERATURE.md` (PDF opened 13 Nov). |
| komaromi2022supply | Komaromi, Cerdeiro, Liu (2022), IMF WP 22/59 | Crossref (issue 059, March 2022) | AIS used to measure shipping delays and port congestion. Basis: abstract (OpenAlex). |
| adland2017ais | Adland, Jia, Strandenes (2017), Maritime Policy & Management 44(5) 657-665 | Crossref | AIS crude exports align with customs in aggregate, differ by country and period (pipelines, transshipment). Basis: abstract (OpenAlex). |
| yang2019big | Yang, Wu, Wang, Jia, Li (2019), Transport Reviews 39(6) 755-773 | Crossref; OpenAlex | AIS uses include trade flow estimation. Basis: abstract. |
| vanderwielen2024optimising | van der Wielen, McGurk, Barrett (2024), Statistical Journal of the IAOS 40(2) 421-434 | Crossref; OpenAlex | AIS tested for official port-visit statistics. Basis: abstract. |
| hutten2026high | Hütten (2026), Geomatics 6(1) 10 | Crossref; OpenAlex | Open terrestrial AIS used to map port activity in Tokyo Bay. Basis: abstract. |
| torres2012sentinel | Torres et al. (2012), Remote Sensing of Environment 120, 9-24 (21 authors) | Crossref | Cited for the Sentinel-1 mission only. Basis: bibliographic record (no abstract retrieved). |
| greidanus2017sumo | Greidanus et al. (2017), Remote Sensing 9(3) 246 | Crossref | SUMO is a pixel-based CFAR detector with land masking. Basis: abstract, recorded in `research/LITERATURE.md`. |
| santamaria2017mass | Santamaria et al. (2017), Remote Sensing 9(7) 678 | Crossref | SUMO run over the Sentinel-1 archive of the Mediterranean, matched to AIS. Basis: abstract, `research/LITERATURE.md`. |
| paolo2022xview3 | Paolo et al. (2022), NeurIPS 35, 37604-37616 | Crossref 10.52202/068431-2726; arXiv 2206.00897 page (200, title matches) | Benchmark of detectors on Sentinel-1 for dark vessels. Basis: arXiv abstract page, `research/LITERATURE.md`. |
| bai1997estimation | Bai (1997), Review of Economics and Statistics 79(4) 551-563 | Crossref; OpenAlex abstract | Least-squares estimation of a change point. |
| wilson1927probable | Wilson (1927), JASA 22(158) 209-212 | Crossref | Source of the Wilson interval used in `research/sar_label_eval.py`. |
| hyndman2006another | Hyndman, Koehler (2006), IJF 22(4) 679-688 | Crossref; abstract on the first author's publication page | Mean absolute scaled error divides by the error of a naive forecast. |
| palu2023future | Palu, Hilmola (2023), Logistics 7(3) 39 | Crossref; OpenAlex | Review built from papers, policy addresses and UN/ADBI studies. Basis: abstract. |
| nurseiit2025attractiveness | Nurseiit (2025), Journal of Eurasian Studies 17(1) 167-182 | Crossref (issued October 2025) | Uses the ADB time-cost-distance method and the LPI. Basis: abstract. |
| zhumanov2024trans | Zhumanov, Kegenbekov, Tolujevs (2024), Transport and Telecommunication Journal 25(1) 11-19 | Crossref; OpenAlex | Simulation modelling of route infrastructure. Basis: abstract. |
| song2026paperorchestra | Song, Song, Pfister, Yoon (2026), PaperOrchestra, arXiv:2604.05018 (cs.AI) | arXiv abstract page (title, authors, 6 April 2026) | Cited in the AI-use statement only. The community skill pack (github.com/ar9av/paperorchestra, MIT licence) was read as a reference; none of its code was run. |

## Not added

- Crisp (2004) CFAR review and the UN AIS Handbook: still not opened (`research/OPEN_QUESTIONS.md` item 16).
- Other corridor papers found on OpenAlex (geopolitics overviews, a 5G-IoT logistics simulation, legal studies):
  not about measuring traffic; left out to keep the related work on point.
- Gwangyang PortWatch query figures: not reproducible (service refused requests on 14 November); not cited.

## Not verified today

- Grey-literature contents (World Bank, EBRD, CAREC, ADB, TITR chart, Aktau strategy) were not re-read; the GET
  only confirms the address resolves. Their use in the paper rests on the earlier passes.
- Semantic Scholar did not confirm the existing entries because of rate limiting.
