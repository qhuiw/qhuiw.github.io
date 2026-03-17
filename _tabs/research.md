---
layout: page
title: Research
icon: fas fa-book-open
permalink: /research/
order: 2
---

<style>
.section-title {
  margin-top: 1.5rem;
  margin-bottom: 1rem;
}

.pub-list {
  display: grid;
  gap: 1.5rem;
  margin-top: 1rem;
}

.pub-item {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid var(--main-border-color, #e5e5e5);
  border-radius: 0.75rem;
  background: var(--card-bg, #fff);
}

.pub-thumb {
  width: 100%;
  display: block;
}

.pub-thumb img {
  width: 100%;
  height: auto;
  border-radius: 0.5rem;
  object-fit: cover;
  display: block;
}

.pub-body {
  width: 100%;
}

.pub-title {
  margin: 0 0 0.35rem 0;
  font-size: 1.05rem;
}

.pub-title-text {
  color: var(--link-color);
  font-weight: 500;
  text-decoration: underline;
}

.pub-meta {
  margin: 0 0 0.55rem 0;
  font-size: 0.9rem;
  opacity: 0.8;
}

.pub-abstract {
  margin: 0;
  line-height: 1.6;
}

.pub-links {
  margin-top: 0.7rem;
  font-size: 0.92rem;
}

.talk-deck-list {
  display: grid;
  gap: 1.5rem;
  margin-top: 1rem;
}

.talk-deck-item {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid var(--main-border-color, #e5e5e5);
  border-radius: 0.75rem;
  background: var(--card-bg, #fff);
}

.talk-deck-thumb {
  width: 100%;
  display: block;
}

.talk-deck-thumb img {
  width: 100%;
  height: auto;
  border-radius: 0.5rem;
  object-fit: cover;
  display: block;
}

.talk-deck-body {
  width: 100%;
}

.talk-deck-title {
  margin: 0 0 0.35rem 0;
  font-size: 1.05rem;
}

.talk-deck-title-text {
  color: var(--link-color);
  font-weight: 500;
  text-decoration: underline;
}

.talk-deck-meta {
  margin: 0 0 0.55rem 0;
  font-size: 0.9rem;
  opacity: 0.8;
}

.talk-deck-description {
  margin: 0;
  line-height: 1.6;
}

.abstract-keyword {
  font-weight: 600;
  color: var(--heading-color, inherit);
  background: color-mix(in srgb, var(--link-color) 16%, transparent);
  padding: 0 0.25rem;
  border-radius: 0.25rem;
}

.talk-deck-links {
  margin-top: 0.7rem;
  font-size: 0.92rem;
}

</style>

<h2 class="section-title">Publications</h2>

<div class="pub-list">

  <article class="pub-item">
    <div class="pub-thumb">
      <!-- <img src="/assets/img/publications/paper-2025-BulletCT.png" alt="Preview image of BulletCT paper"> -->
      <iframe src="/assets/publications/usenixsecurity25-wang-nan.pdf" alt="Preview of BulletCT paper" width="100%" height="500px">
      </iframe>
    </div>

    <div class="pub-body">
      <h3 class="pub-title">
        <span class="pub-title-text">
          <b>BulletCT</b>: Towards More Scalable Ring Confidential Transactions With Transparent Setup
        </span>
      </h3>
      <p class="pub-meta">Nan Wang, <b>Qianhui Wang</b>, Dongxi Liu, Muhammed F. Esgin, Alsharif Abuadbba • USENIX Security 2025</p>
      <p class="pub-abstract">
        <!-- Short abstract: one paragraph (2-4 sentences) describing the main problem, method, and key result. -->
        <span class="abstract-keyword">TL;DR:</span> BulletCT is a new Ring Confidential Transaction (RingCT) signature scheme in the discrete logarithm setting that does not require a trusted setup. It achieves greater scalability than state-of-the-art RingCT schemes. BulletCT features a novel K-out-of-N proof for strong anonymity and a tag proof that leverages permutation constraints to achieve linkability. Additionally, we identify key limitations in applying Any-out-of-N proofs to RingCT and address a critical flaw in prior constructions. 
      </p>
      <p class="pub-links">
        <a href="https://www.usenix.org/system/files/usenixsecurity25-wang-nan.pdf" target="_blank" rel="noopener">Paper</a> |
        <a href="https://eprint.iacr.org/2025/188" target="_blank" rel="noopener">ePrint</a> |
        <!-- <a href="https://arxiv.org/abs/xxxx.xxxxx" target="_blank" rel="noopener">arXiv</a> | -->
        <a href="https://zenodo.org/records/14642722" target="_blank" rel="noopener">Code</a>
      </p>
    </div>
  </article>

</div>

<h2 class="section-title">Talks</h2>

<div class="talk-deck-list">

  <article class="talk-deck-item">
    <div class="talk-deck-thumb">
      <iframe src="/assets/slides/20260310-cascade-temporal-armmte.pdf" alt="Preview of cascade talk" width="100%" height="500px">
      </iframe>
    </div>

    <div class="talk-deck-body">
      <h3 class="talk-deck-title">
        <span class="talk-deck-title-text">
        
          Enhancing Temporal Safety of CHERI-enabled Language Runtimes with ARM Memory Tagging Extension (MTE)
          <!-- Enhancing Temporal Memory Safety for C/C++ with ARM MTE: A Case Study of CHERI-MTE -->
        </span>
      </h3>
      <p class="talk-deck-meta">CASCADE showcase • 2026 March</p>
      <p class="talk-deck-description">
        <span class="abstract-keyword">Abstract:</span> Using capability instructions for memory access enables deterministic traps of out-of-bounds and use-after-reallocation errors in the CHERI-enabled languages. However, benchmarking the CHERI-enabled CPython allocators reveals very prominent overheads due to the current CHERI temporal safety mechanism, which discourages industrial adoption. While sources of overheads could be the less-than-optimal revoker design, complex interaction of the quarantine and runtime allocator behaviours, we are motivated to explore adding ARM's memory tagging extension (MTE) to recolour freed memory allocations for immediate reuse. This approach aims to reduce the amount of memory quarantined and the frequency of revocation sweeps that installs bulk of memory and runtime overheads currently.
      </p>
      <p class="talk-deck-links">
        <!-- <a href="/assets/slides/20260310-cascade-temporal-armmte.pdf" target="_blank" rel="noopener">Slides (.pdf)</a> | -->
        <a href="/assets/slides/20260310-cascade-temporal-armmte.pptx" target="_blank" rel="noopener">Slides (animated .pptx)</a>
      </p>
    </div>
  </article>

  <article class="talk-deck-item">
    <div class="talk-deck-thumb">
      <iframe src="/assets/slides/20260220-wics-hwsw-interface.pdf" alt="Preview of wics talk" width="100%" height="500px">
      </iframe>
      <!-- <a href="/assets/slides/20260220-wics-hwsw-interface.pptx" target="_blank" rel="noopener">
        <img src="" alt="Slide preview image of talk deck 2">
      </a> -->
    </div>

    <div class="talk-deck-body">
      <h3 class="talk-deck-title">
        <span class="talk-deck-title-text">
          Hardware-Software Interface: How it contributes to better computer security
        </span>
      </h3>
      <p class="talk-deck-meta">Woman in CS seminar • 2026 Feb</p>
      <p class="talk-deck-description">
        <!-- Short summary of this talk in 1-2 sentences. -->
        <span class="abstract-keyword">Abstract:</span> Modern computer security relies heavily on software-based defences, including analysis tools that look for potential bugs and patches that fix reported vulnerabilities. Although safer programming languages and improved system designs have significantly reduced many risks, memory safety problems still remain as a major security concern, accounting for over 70% of serious vulnerabilities in Microsoft and Chromium codebases. In this talk, we explore how rethinking the boundary between hardware and software opens up exciting new opportunities for stronger security guarantees. We show how this interface represents a design space full of trade-offs, and how the design approach requires piecing together multiple layers of the computer to build a secure and practical system.
      </p>
      <p class="talk-deck-links">
        <a href="/assets/slides/20260220-wics-hwsw-interface.pptx" target="_blank" rel="noopener">Slides (animated .pptx)</a>
      </p>
    </div>
  </article>

  <article>
    <div class="talk-deck-thumb">
      <iframe src="/assets/slides/20221030-amd.pdf" alt="Preview of amd talk" width="100%" height="500px">
      </iframe>
    </div>

    <div class="talk-deck-body">
      <h3 class="talk-deck-title">
        <span class="talk-deck-title-text">
          Algorithmic Mechanism Design: A New Frontier in Algorithmic Game Theory
        </span>
      </h3>
      <p class="talk-deck-meta">Advanced Algorithms video tutorial • 2022 Oct</p>
      <p class="talk-deck-description">
        <!-- Short summary of this talk in 1-2 sentences. -->
        <span class="abstract-keyword">Abstract:</span> Algorithmic mechanism design is a subfield of algorithmic game theory that focuses on designing algorithms and mechanisms to achieve desired outcomes in strategic settings. It combines techniques from computer science, economics, and game theory to create efficient and effective solutions for various problems, such as auctions, resource allocation, and social choice. In this talk, we will explore the fundamental concepts of algorithmic mechanism design, including incentive compatibility, social welfare maximisation, and computational complexity. We will also introduce some of the latest research developments in this exciting field and their applications in real-world scenarios.
      </p>
      <p class="talk-deck-links">
        <a href="/assets/slides/20221030-amd.pptx" target="_blank" rel="noopener">Slides (.pptx)</a>
      </p>
    </div>
  </article>
  More to come...

</div>