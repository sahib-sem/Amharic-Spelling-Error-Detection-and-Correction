# Amharic Grammarly - Spelling Error Detection System and Suggestion

## Objective

Amharic Grammarly detects and suggests corrections for misspelled Amharic words using both contextual and non-contextual methods.

## Data

Two datasets:
1. **Dictionary**: Words with frequencies.
2. **Corpus**: Amharic text for next word prediction.

## Preprocessing

- `dictionary.txt`: Preprocessed and sorted.
- Corpus: Normalization using `etnltk` for character and short-form expansion.

## Algorithms

1. **Non-Contextual Correction**: Edit Distance (Levenshtein distance).
   - Operations: Insertion, deletion, swapping, or replacing characters.

2. **Contextual Correction**: LSTM for next word prediction.
   - Architecture: Embedding, LSTM layers, fully connected layers.

## Limitations

- LSTM vocabulary (46,000 words) vs Dictionary (450,000 words).

## Combining Suggestions

1. Identify misspelled words.
2. Run edit distance for suggestions.
3. Use LSTM for context-based predictions.
4. Combine suggestions based on probabilities.

## Backend

Fastapi backend with endpoint `/spellcheck/suggestion` for spellcheck suggestions.
