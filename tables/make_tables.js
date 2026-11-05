const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, BorderStyle, PageOrientation, AlignmentType } = require('docx');
const csv = (p) => { const t = fs.readFileSync(p, 'utf8').trim(); const rows = []; let row = [], f = '', q = false;
  for (let i = 0; i < t.length; i++) { const c = t[i];
    if (q) { if (c === '"' && t[i+1] === '"') { f += '"'; i++; } else if (c === '"') q = false; else f += c; }
    else if (c === '"') q = true; else if (c === ',') { row.push(f); f = ''; } else if (c === '\n') { row.push(f); rows.push(row); row = []; f = ''; } else if (c !== '\r') f += c; }
  row.push(f); rows.push(row); return rows; };
const F = 'Arial', SZ = 18;
const thin = { style: BorderStyle.SINGLE, size: 4, color: '808080' };
const borders = { top: thin, bottom: thin, left: thin, right: thin };
function cell(text, w, bold) {
  return new TableCell({ width: { size: w, type: WidthType.DXA }, borders, margins: { top: 60, bottom: 60, left: 80, right: 80 },
    children: [new Paragraph({ children: [new TextRun({ text, bold: !!bold, font: F, size: SZ })] })] });
}
function makeDoc(num, caption, header, rows, widths, notes, landscape) {
  const total = widths.reduce((a, b) => a + b, 0);
  const table = new Table({ width: { size: total, type: WidthType.DXA }, columnWidths: widths,
    rows: [new TableRow({ tableHeader: true, children: header.map((h, i) => cell(h, widths[i], true)) }),
      ...rows.map(r => new TableRow({ children: r.map((v, i) => cell(v, widths[i], false)) }))] });
  const kids = [new Paragraph({ spacing: { after: 160 }, children: [new TextRun({ text: `Table ${num}. `, bold: true, font: F, size: 22 }), new TextRun({ text: caption, font: F, size: 22 })] }), table];
  for (const n of notes) kids.push(new Paragraph({ spacing: { before: 120 }, children: [new TextRun({ text: n, italics: true, font: F, size: 16 })] }));
  const page = landscape ? { size: { width: 12240, height: 15840, orientation: PageOrientation.LANDSCAPE }, margin: { top: 1080, bottom: 1080, left: 1080, right: 1080 } }
                         : { size: { width: 12240, height: 15840 }, margin: { top: 1080, bottom: 1080, left: 1080, right: 1080 } };
  return new Document({ styles: { default: { document: { run: { font: F, size: SZ } } } }, sections: [{ properties: { page }, children: kids }] });
}
const out = process.argv[2];
const save = (doc, name) => Packer.toBuffer(doc).then(b => fs.writeFileSync(`${out}/${name}`, b));

// Table 1
save(makeDoc(1, 'Adapter architectures. Reported values are as stated in each source, in its own setting; computed values apply the stated bottleneck to LLaMA-2-7B (6.74B parameters).',
  ['Architecture', 'Placement', 'Added parameters', 'Reported result', 'Source'],
  [['Houlsby', 'Two adapters per layer, after attention and after the feed-forward sub-layer', 'Reported: 3.6% per task (BERT). Computed: 0.50% at bottleneck 64', 'Within 0.4% of full fine-tuning on GLUE', 'Houlsby et al. (2019), abstract'],
   ['Pfeiffer', 'One adapter per layer, after the feed-forward sub-layer', 'Computed: 0.25% at bottleneck 64 (half of Houlsby)', 'A single adapter after the feed-forward layer outperformed other placements tested', 'Pfeiffer et al. (2020), Appendix A.2'],
   ['Compacter', 'Adapters with low-rank parameterized hypercomplex multiplication layers', 'Reported: 0.047% of model parameters', 'On par with full fine-tuning on GLUE; better on SuperGLUE and in low-resource settings', 'Mahabadi et al. (2021), abstract']],
  [1500, 2700, 2400, 2500, 1900],
  ['All three place adapters in sequence with the Transformer sub-layers and therefore add inference latency, which Hu et al. (2021, Table 1) report can be significant in online, short-sequence settings. Computed values: analysis/memory_model.py configuration; claim IDs C012, C089 to C092 in data/claims.csv.'], false), 'Table_1.docx');

// Table 2
const t2 = csv(process.argv[3]);
save(makeDoc(2, 'LoRA variants as reported in each primary source. Values compare each variant with LoRA within the same study; because models, tasks, and baselines differ between studies, rows are not comparable with one another.',
  t2[0], t2.slice(1), [1300, 2700, 2300, 2900, 2100, 1900],
  ['Sources and locations are given per row; full claim-level records are in data/claims.csv.'], true), 'Table_2.docx');

// Table 3
save(makeDoc(3, 'Quantization methods discussed in Section V, with results as reported by each source.',
  ['Method', 'Type', 'Quantized', 'Reported quality', 'Reported cost', 'Source'],
  [['GPTQ', 'Post-training', 'Weights, 3 to 4 bits', '4-bit WikiText2 perplexity 8.34 to 8.37 (OPT-175B), 8.11 to 8.21 (BLOOM-176B)', 'About 4.2 GPU hours for OPT-175B on one A100', 'Frantar et al. (2023), Tables 2 and 3'],
   ['AWQ', 'Post-training', 'Weights, 3 to 4 bits', 'Perplexity equal to or lower than GPTQ on LLaMA and Llama-2 (e.g. 5.60 vs 5.69, Llama-2-7B INT4)', 'Calibration set of 16 sequences vs 192 for GPTQ', 'Lin et al. (2024), Table 4, Fig. 8a'],
   ['SmoothQuant', 'Post-training', 'Weights and activations, 8 bits (W8A8)', 'Negligible accuracy loss (authors)', 'Up to 1.56x speedup and 2x memory reduction vs FP16', 'Xiao et al. (2023), abstract'],
   ['QLoRA (NF4)', 'Frozen base quantized during fine-tuning', 'Frozen base weights, 4 bits', 'Matches 16-bit full fine-tuning and 16-bit LoRA on GLUE, Super-NaturalInstructions, MMLU', 'Double quantization saves about 0.37 bits per parameter', 'Dettmers et al. (2023), Sections 3 and 4'],
   ['EfficientQAT', 'Quantization-aware training', 'Weights, 2 to 4 bits', '2-bit Llama-2-70B: average accuracy 69.48 vs 72.41 at full precision', '41 hours on one A100-80GB for 2-bit Llama-2-70B', 'Chen et al. (2025), abstract']],
  [1400, 1700, 1800, 3200, 2600, 2200],
  ['Mixed-precision training (Micikevicius et al., 2018), listed in the previous version of this table, is not a quantization method and is discussed in Section 5.1.'], true), 'Table_3.docx');

// Table 4
const t4 = csv(process.argv[4]);
const h4 = ['Method', 'Rank', 'Targets', 'FlashAttention', 'Gradient checkpointing', 'Trainable parameters (%)', 'Model states (GB)', 'Activations (GB)', 'Total, batch 4, seq 2048 (GB)', 'Total, batch 1, seq 512 (GB)'];
save(makeDoc(4, 'Modeled peak training memory for LLaMA-2-7B in bf16, computed by analysis/memory_model.py from the assumptions in analysis/memory_assumptions.json.',
  h4, t4.slice(1).map(r => r.slice(0, 10)), [1600, 600, 1200, 1400, 1500, 1300, 1150, 1300, 1400, 1400],
  ['Model states follow Rajbhandari et al. (2020); QLoRA storage follows Dettmers et al. (2023); activations follow Korthikanti et al. (2023) and are an upper bound for LoRA and QLoRA. The model reproduces the 6.9 GB QLoRA footprint of Dettmers et al. (2023, Figure 6) to within 0.1 GB, and its activation and logit terms match measured LoRA memory growth reported by Dbouk et al. (2026) to within a few percent (analysis/activation_check.md). CUDA context, allocator fragmentation, and framework buffers are excluded. Accuracy is deliberately omitted; see Section 8.3. Configuration IDs for each row are in tables/table4a_memory.csv.'], true), 'Table_4.docx');
