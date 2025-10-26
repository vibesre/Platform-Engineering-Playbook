#!/bin/bash
# Batch extract dialogue from all podcast documentation files

DOCS_DIR="../docs/podcasts"
OUTPUT_DIR="../content/podcast-episodes"

# Create output directory
mkdir -p "$OUTPUT_DIR"

echo "🎙️  Batch Dialogue Extraction"
echo "============================"
echo "Source: $DOCS_DIR"
echo "Output: $OUTPUT_DIR"
echo ""

# Counter
count=0

# Process all markdown files
for doc in "$DOCS_DIR"/*.md; do
    if [ -f "$doc" ]; then
        basename=$(basename "$doc" .md)
        output_file="$OUTPUT_DIR/${basename}-dialogue.md"
        
        echo "📄 Processing: $basename"
        python3 scripts/extract_dialogue.py "$doc" -o "$output_file"
        
        ((count++))
    fi
done

echo ""
echo "✅ Extracted $count episode dialogues"
echo ""
echo "Next steps:"
echo "1. Review extracted dialogues in $OUTPUT_DIR"
echo "2. Generate podcasts: python3 scripts/generate_podcast.py $OUTPUT_DIR --batch"