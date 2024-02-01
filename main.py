from typing import Union

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from SpellCheck import SpellCheck

spl = SpellCheck()

class GetSpellingErrorRequest(BaseModel):
    text: str = ""

class NextWordSuggestionRequest(BaseModel):
    text: str = ""

class NextWordSuggestion(BaseModel):
    next_word: str = ""

class NextWordSuggestionTopCounts(BaseModel):
    possible_next_words: list[str] = []

class GetSpellingErrorSuggestionResponse(BaseModel):
    suggestions : dict[str, list[str]] = {}

app = FastAPI()

@app.post("/next_word")

def get_next_word(request: NextWordSuggestionRequest) -> NextWordSuggestion:
        
        text = request.text

        nxt_word = spl.next_words(text)

        if not nxt_word:

            raise HTTPException(status_code=400, detail="The context is not in the vocabulary(one or more of the last 3 words are misselled)")
        
        return NextWordSuggestion(next_word=nxt_word)

    
@app.post("/next_word/all/{k}")
def get_next_word_top_counts(request: NextWordSuggestionRequest, k: int) -> NextWordSuggestionTopCounts:
        
        text = request.text

        poss_nxt_word = spl.next_words_top_counts(text, k)

        if not poss_nxt_word:
                
            raise HTTPException(status_code=400, detail="The context is not in the vocabulary(one or more of the last 3 words are misselled)")

      
        
        return NextWordSuggestionTopCounts(possible_next_words=poss_nxt_word)


@app.post("/spellcheck/suggestion")

def get_spelling_error_suggestion(request: GetSpellingErrorRequest) -> GetSpellingErrorSuggestionResponse:
    
    text = request.text

    if not text:

        raise HTTPException(status_code=400, detail="The text is empty")

    return GetSpellingErrorSuggestionResponse(suggestions=spl.suggestion(text))


 
