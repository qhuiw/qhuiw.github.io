---
layout: page
title: Research
icon: fas fa-book-open
permalink: /research/
order: 2
---

<h2 class="section-title">Publications</h2>

<div class="pub-list">
  {% capture bulletct_links %}
    <a href="https://www.usenix.org/system/files/usenixsecurity25-wang-nan.pdf" target="_blank" rel="noopener">Paper</a> |
    <a href="https://eprint.iacr.org/2025/188" target="_blank" rel="noopener">ePrint</a> |
    <a href="https://zenodo.org/records/14642722" target="_blank" rel="noopener">Code</a>
  {% endcapture %}

  {% include research/publication-card.html
    preview_pdf="/assets/publications/usenixsecurity25-wang-nan.pdf#page=1&view=FitH"
    preview_alt="Preview of BulletCT paper"
    title_html="<b>BulletCT</b>: Towards More Scalable Ring Confidential Transactions With Transparent Setup"
    meta_html="Nan Wang, <b>Qianhui Wang</b>, Dongxi Liu, Muhammed F. Esgin, Alsharif Abuadbba • USENIX Security 2025"
    summary="BulletCT is a new Ring Confidential Transaction (RingCT) signature scheme in the discrete logarithm setting that does not require a trusted setup. It achieves greater scalability than state-of-the-art RingCT schemes. BulletCT features a novel K-out-of-N proof for strong anonymity and a tag proof that leverages permutation constraints to achieve linkability. Additionally, we identify key limitations in applying Any-out-of-N proofs to RingCT and address a critical flaw in prior constructions."
    links_html=bulletct_links
  %}

</div>

<h2 class="section-title">Talks</h2>

<div class="talk-deck-list">
  {% capture cascade_links %}
    <a href="/assets/slides/20260310-cascade-temporal-armmte.pptx" target="_blank" rel="noopener">Slides (animated .pptx)</a> |
     <a href="https://www.cl.cam.ac.uk/research/cascade/events/2026-03-10-showcase/video/qianhui.mp4" target="_blank" rel="noopener">Recording</a>
  {% endcapture %}

  {% include research/talk-card.html
    preview_pdf="/assets/slides/20260310-cascade-temporal-armmte.pdf#page=1&view=FitH"
    preview_alt="Preview of cascade talk"
    title="Enhancing Temporal Safety of CHERI-enabled Language Runtimes with ARM Memory Tagging Extension (MTE)"
    meta="CASCADE showcase • 2026 March"
    description="Using capability instructions for memory access enables deterministic traps of out-of-bounds and use-after-reallocation errors in the CHERI-enabled languages. However, benchmarking the CHERI-enabled CPython allocators reveals very prominent overheads due to the current CHERI temporal safety mechanism, which discourages industrial adoption. While sources of overheads could be the less-than-optimal revoker design, complex interaction of the quarantine and runtime allocator behaviours, we are motivated to explore adding ARM's memory tagging extension (MTE) to recolour freed memory allocations for immediate reuse. This approach aims to reduce the amount of memory quarantined and the frequency of revocation sweeps that installs bulk of memory and runtime overheads currently."
    links_html=cascade_links
  %}

  {% capture wics_links %}
    <a href="/assets/slides/20260220-wics-hwsw-interface.pptx" target="_blank" rel="noopener">Slides (animated .pptx)</a> |
    <a href="https://youtu.be/wRuxT7aGuEw?list=PLstyePOvf2d3h-Fz6T1s9m9ye2IpEqtTL" target="_blank" rel="noopener">Recording</a>
  {% endcapture %}

  {% include research/talk-card.html
    preview_pdf="/assets/slides/20260220-wics-hwsw-interface.pdf#page=1&view=FitH"
    preview_alt="Preview of WICS talk"
    title="Hardware-Software Interface: How it contributes to better computer security"
    meta="Woman in CS seminar • 2026 Feb"
    description="Modern computer security relies heavily on software-based defences, including analysis tools that look for potential bugs and patches that fix reported vulnerabilities. Although safer programming languages and improved system designs have significantly reduced many risks, memory safety problems still remain as a major security concern, accounting for over 70% of serious vulnerabilities in Microsoft and Chromium codebases. In this talk, we explore how rethinking the boundary between hardware and software opens up exciting new opportunities for stronger security guarantees. We show how this interface represents a design space full of trade-offs, and how the design approach requires piecing together multiple layers of the computer to build a secure and practical system."
    links_html=wics_links
  %}

  {% capture amd_links %}
    <a href="/assets/slides/20221030-amd.pptx" target="_blank" rel="noopener">Slides (.pptx)</a>
  {% endcapture %}

  {% include research/talk-card.html
    preview_pdf="/assets/slides/20221030-amd.pdf#page=1&view=FitH"
    preview_alt="Preview of AMD talk"
    title="Algorithmic Mechanism Design: A New Frontier in Algorithmic Game Theory"
    meta="Advanced Algorithms video tutorial • 2022 Oct"
    description="Algorithmic mechanism design is a subfield of algorithmic game theory that focuses on designing algorithms and mechanisms to achieve desired outcomes in strategic settings. It combines techniques from computer science, economics, and game theory to create efficient and effective solutions for various problems, such as auctions, resource allocation, and social choice. In this talk, we will explore the fundamental concepts of algorithmic mechanism design, including incentive compatibility, social welfare maximisation, and computational complexity. We will also introduce some of the latest research developments in this exciting field and their applications in real-world scenarios."
    links_html=amd_links
  %}

  More to come...

</div>