# Overleaf and arXiv Upload Instructions

## Files Included

Your LaTeX paper now includes all 5 figures with proper captions:

1. **Figure 1**: Dataset Construction Pipeline (`secure-code-2-image1.png`)
2. **Figure 2**: Four-Turn Conversational Format (`secure-code-2-image2.png`)
3. **Figure 3**: Coverage Snapshot (`secure-code-2-image3.png`)
4. **Figure 4**: Weekly Compliance Progress (`chart1_compliance_progress.png`)
5. **Figure 5**: Dataset Comparison (`chart2_dataset_comparison.png`)

## Upload Package

**Location**:
- ZIP: `/Users/scott/perfecxion/datasets/securecode/v2/docs/paper/securecode-v2-arxiv-package.zip` (16 MB)
- TAR.GZ: `/Users/scott/perfecxion/datasets/securecode/v2/docs/paper/securecode-v2-arxiv-package.tar.gz` (16 MB)

**Contents**:
- `secure-code-v2.tex` (main LaTeX file with all figures)
- `secure-code-2-image1.png` (6.3 MB)
- `secure-code-2-image2.png` (4.9 MB)
- `secure-code-2-image3.png` (4.5 MB)
- `chart1_compliance_progress.png` (235 KB)
- `chart2_dataset_comparison.png` (228 KB)

**Total size**: ~16 MB

## Overleaf Upload Instructions

### Option 1: Upload Compressed Package (Recommended)

1. Go to [Overleaf](https://www.overleaf.com)
2. Click "New Project" → "Upload Project"
3. Upload `securecode-v2-arxiv-package.zip` (or `.tar.gz`)
4. Overleaf will automatically extract all files
5. Set `secure-code-v2.tex` as the main document
6. Compile with pdfLaTeX or XeLaTeX

### Option 2: Manual File Upload

1. Go to [Overleaf](https://www.overleaf.com)
2. Click "New Project" → "Blank Project"
3. Upload `secure-code-v2.tex`
4. Upload all 5 PNG files (drag and drop into project root)
5. Compile with pdfLaTeX or XeLaTeX

## arXiv Upload Instructions

### Prepare Your Submission

1. **Extract the package** (if needed):
   ```bash
   cd /Users/scott/perfecxion/datasets/securecode/v2/docs/paper
   unzip securecode-v2-arxiv-package.zip
   # OR
   tar -xzf securecode-v2-arxiv-package.tar.gz
   ```

2. **Verify all files are present**:
   ```bash
   ls -lh *.tex *.png
   ```

### Upload to arXiv

1. Go to [arXiv.org](https://arxiv.org/submit)
2. Log in with your arXiv account
3. Click "Start New Submission"
4. **Metadata**:
   - Title: "SecureCode v2.0: A Production-Grade Dataset for Training Security-Aware Code Generation Models"
   - Authors: Scott Thornton
   - Abstract: (copy from paper)
   - Primary category: **cs.CR** (Cryptography and Security)
   - Secondary categories: **cs.SE** (Software Engineering), **cs.LG** (Machine Learning)

5. **Upload Files**:
   - Select "Upload Files" tab
   - Upload the `.zip` or `.tar.gz` package OR upload individual files:
     - `secure-code-v2.tex`
     - All 5 PNG files
   - arXiv will automatically detect the main `.tex` file

6. **Process and Preview**:
   - Click "Process Files"
   - Wait for arXiv to compile your paper
   - Download and review the PDF preview
   - Verify all 5 figures appear correctly

7. **Submit**:
   - If preview looks good, click "Submit"
   - **Note**: You'll need an endorsement for cs.CR category
   - Your endorsement code: **YF9OXP**

### arXiv Endorsement

Since you need an endorsement for cs.CR, forward the endorsement email to:
- Your thesis advisor (if applicable)
- A colleague who has published 3+ papers in cs.* categories in the last 5 years
- A researcher in your field whose work relates to AI security

They can endorse you using code **YF9OXP**.

## Image Format Requirements

### arXiv Requirements ✅
- ✅ PNG format accepted
- ✅ Images are high resolution (6.3MB, 4.9MB, 4.5MB for main figures)
- ✅ Total package size ~16MB (well under arXiv's 50MB limit)

### Overleaf Requirements ✅
- ✅ All images in project root directory
- ✅ Relative paths used in `\includegraphics{}`
- ✅ No subdirectories needed

## Troubleshooting

### If figures don't appear in Overleaf:
1. Verify all PNG files are uploaded to project root
2. Check that filenames match exactly (case-sensitive)
3. Recompile the project (Ctrl+S or Cmd+S)
4. Try switching compiler (pdfLaTeX ↔ XeLaTeX)

### If arXiv compilation fails:
1. Check the arXiv processing log for errors
2. Ensure all image files were uploaded
3. Verify no absolute paths in `\includegraphics{}`
4. Make sure `\usepackage{graphicx}` is in the preamble

### If images are too large:
All images are already optimized:
- Main figures: 4.5-6.3 MB (acceptable for academic papers)
- Charts: 227-235 KB (very efficient)
- Total: 16 MB (well under arXiv limit)

## Citation Information

Once published on arXiv, update the BibTeX citation with the arXiv ID:

```bibtex
@misc{thornton2025securecode,
  title={SecureCode v2.0: A Production-Grade Dataset for Training Security-Aware Code Generation Models},
  author={Thornton, Scott},
  year={2025},
  month={December},
  publisher={perfecXion.ai},
  eprint={XXXX.XXXXX},  # Add your arXiv ID here
  archivePrefix={arXiv},
  primaryClass={cs.CR},
  url={https://perfecxion.ai/articles/securecode-v2-dataset-paper.html},
  note={Dataset: https://huggingface.co/datasets/scthornton/securecode-v2}
}
```

## Next Steps

1. ✅ Upload package to Overleaf to verify compilation
2. ✅ Review PDF output to ensure all figures render correctly
3. ✅ Get endorsement for cs.CR category (code: YF9OXP)
4. ✅ Submit to arXiv
5. ✅ Update paper URLs with arXiv link once published
6. ✅ Update CITATION.bib with arXiv ID

## Support

If you encounter any issues:
- **Overleaf**: Check their [LaTeX documentation](https://www.overleaf.com/learn)
- **arXiv**: Email help@arxiv.org or check [submission help](https://info.arxiv.org/help/submit.html)
