# Podcast Update

Update existing podcast episodes with pronunciation fixes or script improvements, regenerating only the changed audio chunks.

## When to Use This Skill

Use this skill when:
- User says: "Update episode pronunciation", "Fix pronunciation in episode", "Update episode script"
- Need to add/fix pronunciation tags in an existing episode
- Making accuracy or grammar corrections to published episodes
- Want to regenerate only changed chunks (not the entire episode)

**Key Benefit**: Smart chunk regeneration - only regenerates what changed, saving time and API costs.

## What This Skill Handles

### 1. Pronunciation Updates
- Add new term to PRONUNCIATION_GUIDE.md
- Update all occurrences in the episode script with proper phoneme tags
- Identify which chunks changed
- Regenerate only affected chunks
- Preserve cached chunks that didn't change

### 2. Script Updates
- Fix accuracy issues (fact corrections, updated statistics)
- Grammar improvements
- Clarity enhancements
- Identify which chunks changed
- Regenerate only affected chunks

## Update Workflow

### Phase 1: Identify Episode & Update Type

**Ask user**:
1. Which episode number? (e.g., "00004")
2. What type of update?
   - **Pronunciation fix**: Add/update pronunciation for a term
   - **Script edit**: Accuracy, grammar, or clarity improvements

### Phase 2: For Pronunciation Updates

**Steps**:
1. **Get pronunciation details**:
   - Term to fix (e.g., "Vercel", "PostgreSQL")
   - Correct pronunciation (e.g., "vur-SELL", "post-gres-Q-L")
   - IPA notation (or help user create it)

2. **Update PRONUNCIATION_GUIDE.md**:
   - Add to appropriate section if new
   - Update existing entry if correction
   - Include IPA, SSML tag example, notes

3. **Update episode script**:
   - Find all occurrences of the term
   - Add `<phoneme alphabet="ipa" ph="...">Term</phoneme>` tags
   - Show user which lines changed

4. **Estimate regeneration**:
   - Identify which chunks contain the updated term
   - Show count: "X out of Y chunks will be regenerated"
   - Estimate cost savings vs full regeneration

5. **Preserve metadata before regeneration**:
   - **CRITICAL**: Backup the metadata .txt file first
   - `cp output_latest/00XXX-name.txt /tmp/00XXX-name-metadata-backup.txt`
   - The generate script creates placeholder metadata - we'll restore the real one after

6. **Regenerate chunks**:
   - Run `generate_podcast.py` WITHOUT `--force` flag
   - System auto-detects changed chunks
   - Regenerate only affected chunks

7. **Restore metadata**:
   - **CRITICAL**: Restore the backed-up metadata file
   - `cp /tmp/00XXX-name-metadata-backup.txt output_latest/00XXX-name.txt`
   - Update duration if it changed (from ffprobe output)

8. **Report results**:
   - How many chunks regenerated
   - How many chunks reused from cache
   - Cost saved by smart regeneration
   - Location of updated files

### Phase 3: For Script Updates

**Steps**:
1. **Make script edits**:
   - User provides the changes (Edit tool or manual)
   - OR skill helps identify and fix issues

2. **Show changes**:
   - Display old vs new text
   - Identify affected line numbers

3. **Estimate regeneration**:
   - Show which chunks changed
   - Estimate cost savings

4. **Preserve metadata before regeneration**:
   - **CRITICAL**: Backup the metadata .txt file first
   - `cp output_latest/00XXX-name.txt /tmp/00XXX-name-metadata-backup.txt`
   - The generate script creates placeholder metadata - we'll restore the real one after

5. **Regenerate chunks**:
   - Run `generate_podcast.py` WITHOUT `--force`
   - Smart chunk detection

6. **Restore metadata**:
   - **CRITICAL**: Restore the backed-up metadata file
   - `cp /tmp/00XXX-name-metadata-backup.txt output_latest/00XXX-name.txt`
   - Update duration if it changed (from ffprobe output)

7. **Report results**:
   - Regeneration summary
   - Updated file locations

## Pronunciation Guide Format

When adding to PRONUNCIATION_GUIDE.md:

```markdown
### [Category Name]

| Term | Pronunciation | SSML Tag | Notes |
|------|--------------|----------|-------|
| Term | /IPA/ | `<phoneme alphabet="ipa" ph="IPA">Term</phoneme>` | "human readable" |
```

**Categories**:
- Cloud Providers & Services
- Platform as a Service (PaaS)
- Container & Orchestration
- Databases
- Infrastructure as Code
- Observability & Monitoring
- Networking & CDN
- Protocols & Standards
- Compliance & Security
- Acronyms & Abbreviations
- Hardware & Storage
- Languages & Formats

## IPA Notation Help

Common IPA patterns for tech terms:

**Vowels**:
- `æ` = "a" in "cat" (Azure: ˈæʒɚ)
- `ɛ` = "e" in "bed" (Vercel: vɝˈsɛl)
- `ɪ` = "i" in "bit" (Redis: ˈrɛdɪs)
- `oʊ` = "o" in "go" (Heroku: hɛˈroʊku)
- `u` = "oo" in "boot" (Kubernetes: kubɚˈnɛtiz)
- `ɚ` = "er" in "better" (Vercel: vɝˈsɛl)

**Consonants**:
- `ʒ` = "s" in "measure" (Azure: ˈæʒɚ)
- `ʃ` = "sh" in "ship" (Elasticsearch: ɪˌlæstɪkˈsɜrtʃ)
- `ŋ` = "ng" in "sing" (not common in tech terms)
- `θ` = "th" in "think" (Prometheus: prəˈmiθiəs)

**Stress markers**:
- `ˈ` = primary stress (before syllable): Kuberˈnetes
- `ˌ` = secondary stress (before syllable): ˌKuberˈnetes

**If unsure**: Use phonetic spelling like "vur-SELL" and ask Claude to convert to IPA.

## Cost Savings Examples

**Example 1: Pronunciation fix**
- Episode: 00004 (65 chunks total)
- Term updated: "Vercel" (9 occurrences across 6 chunks)
- Result: Regenerated 6/65 chunks, saved ~$0.30
- Time saved: ~5 minutes vs full regeneration

**Example 2: Script accuracy fix**
- Episode: 00005 (55 chunks total)
- Updated: 3 statistics in 2 chunks
- Result: Regenerated 2/55 chunks, saved ~$0.28
- Time saved: ~8 minutes vs full regeneration

## Quality Checks

Before finalizing updates:

**For Pronunciation**:
- [ ] Term added/updated in PRONUNCIATION_GUIDE.md
- [ ] IPA notation is correct
- [ ] All occurrences in script tagged
- [ ] Phoneme tags properly formatted (no syntax errors)
- [ ] Example pronunciation provided (human-readable)

**For Script Updates**:
- [ ] Changes improve accuracy/clarity
- [ ] No new errors introduced
- [ ] Numbers still spelled out
- [ ] Speaker names still correct format
- [ ] Pause tags not accidentally removed

**For Regeneration**:
- [ ] Backed up metadata .txt file before regeneration
- [ ] Used generate_podcast.py WITHOUT --force
- [ ] Verified only changed chunks regenerated
- [ ] Checked cache summary shows reuse
- [ ] Restored metadata .txt file after regeneration
- [ ] Updated duration in metadata if it changed
- [ ] Updated files exist in output_latest/

## Common Mistakes to Avoid

### ❌ Using --force flag
**Wrong**: `generate_podcast.py script.txt --force`
**Right**: `generate_podcast.py script.txt`

The chunking system auto-detects changes. Using `--force` regenerates ALL chunks unnecessarily.

### ❌ Forgetting to preserve metadata
**Wrong**: Regenerate and lose carefully crafted metadata (title/description/summary)
**Right**: Backup metadata .txt before regeneration, restore after

The generate script creates placeholder metadata. For minor updates (pronunciation fixes, small edits), preserve the existing metadata.

### ❌ Forgetting PRONUNCIATION_GUIDE.md
**Wrong**: Only update the script
**Right**: Update PRONUNCIATION_GUIDE.md first, then script

The guide is the source of truth for future episodes.

### ❌ Incomplete phoneme tags
**Wrong**: `<phoneme>Vercel</phoneme>`
**Right**: `<phoneme alphabet="ipa" ph="vɝˈsɛl">Vercel</phoneme>`

### ❌ Not testing pronunciation
**Wrong**: Update and regenerate entire episode to test
**Right**: Generate just chunk 1 first to verify pronunciation sounds correct

## Testing Pronunciation Before Full Regeneration

To test a pronunciation without regenerating the whole episode:

```bash
# 1. Update just the first occurrence in the script
# 2. Run generation - it will regenerate just that chunk
python3 scripts/generate_podcast.py ../docs/podcasts/scripts/00XXX-name.txt

# 3. Listen to the regenerated chunk
# 4. If good, update all other occurrences
# 5. Run generation again - regenerates remaining changed chunks
```

## Output Format

**After completion, report**:

```markdown
# Episode Update Complete: 00XXX

## Changes Made

**Type**: Pronunciation fix for "Vercel"

**PRONUNCIATION_GUIDE.md**:
- Updated Vercel: /ˈvɝsəl/ → /vɝˈsɛl/ ("VER-sul" → "vur-SELL")

**Script Updates**:
- Found 9 occurrences across 6 chunks
- Updated lines: 1, 23, 29, 31, 33, 43, 87, 99, 121, 123

## Regeneration Summary

- **Total chunks**: 65
- **Regenerated**: 6 (only changed chunks)
- **Cached**: 59 (reused from previous generation)
- **Cost saved**: ~$0.30
- **Time saved**: ~5 minutes

## Updated Files

- Script: `docs/podcasts/scripts/00004-paas-showdown-episode.txt`
- Guide: `podcast-generator/PRONUNCIATION_GUIDE.md`
- Audio: `podcast-generator/output_latest/00004-paas-showdown-episode.mp3`
- Video: `podcast-generator/output_latest/00004-paas-showdown-episode.mp4`

## Status

✅ Pronunciation updated
✅ Chunks regenerated
✅ Ready for publishing

**Next steps**: Episode page and published audio already include the fix (if episode was already published, you may want to re-upload the MP3/MP4).
```

---

## Instructions for Claude

When this skill is invoked:

1. **Ask for episode number and update type**:
   ```
   Which episode needs updating? (e.g., 00004)
   What type of update?
   - Pronunciation fix
   - Script edit (accuracy/grammar)
   ```

2. **For pronunciation updates**:
   - Get term and correct pronunciation
   - Ask user to confirm IPA notation (or help generate it)
   - Update PRONUNCIATION_GUIDE.md in correct category
   - Find all occurrences in episode script
   - Update script with phoneme tags
   - Show which chunks will be affected

3. **For script edits**:
   - Help user make edits or guide them through Edit tool
   - Identify changed line numbers
   - Show which chunks affected

4. **Estimate before regenerating**:
   ```
   Changes affect 6 out of 65 chunks
   Estimated regeneration time: ~2 minutes
   Estimated cost savings: ~$0.30 (vs full regeneration)

   Proceed with regeneration? [Y/n]
   ```

5. **Preserve metadata**:
   ```bash
   # Backup metadata BEFORE regeneration
   cp podcast-generator/output_latest/00XXX-name.txt /tmp/00XXX-name-metadata-backup.txt
   ```

6. **Regenerate smartly**:
   ```bash
   cd podcast-generator
   python3 scripts/generate_podcast.py ../docs/podcasts/scripts/00XXX-name.txt
   ```

   **NEVER use --force flag** (defeats smart chunking)

7. **Restore metadata**:
   ```bash
   # Restore metadata AFTER regeneration
   cp /tmp/00XXX-name-metadata-backup.txt podcast-generator/output_latest/00XXX-name.txt

   # Update duration if needed (get from ffprobe)
   ffprobe -v quiet -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 output_latest/00XXX-name.mp3
   # Then update Duration: field in the .txt file
   ```

8. **Monitor and report**:
   - Watch for "Regenerated X/Y chunks, reused Y from cache"
   - Report cost savings
   - Confirm updated files exist

7. **Handle errors**:
   - If validation timeout (like we saw): Note that chunks exist and can be combined manually
   - If pronunciation sounds wrong: Help adjust IPA notation
   - If too many chunks affected: Ask if script change was too broad

**Key principle**: Smart regeneration saves time and money. Only regenerate what changed.
