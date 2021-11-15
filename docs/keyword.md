# Keyword API

## Example
### Input
/api/keyword?sentence=$input

$input = 
I've had a trouble with my daily life because the amount of time I spend with my family increased due to coronavirus. Actually, my father, Kazuki, has behaved violently to me. After drinking,  he always come into my room and give me a shout. Nowadays even though he don't get drunk, he messes with me. If my behaviour is unfavorable, he punches and kicks me. I hope that the days like before could come back to us and I could go back to school as soon as possible. Help me.

### Output
`
    {
    "keyword":[
        {
            "id":1,
            "keyword_jp":"いじめ",
            "keyword_en":"Bullying"
        },
        {
            "id":2,
            "keyword_jp":"蹴る",
            "keyword_en":"kick"
        }
        ]
    }
`