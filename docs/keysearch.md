# Keyword API

## Example
### Input
/api/keyword/sentence=$input

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
    ],
    "articles": [
            {
                "source": {
                  "id": "Nikkei",
                  "name": "Nikkei"
                },
                "transrate_en":{
                    "author": "Natasha Bertrand, Jim Sciutto and Kylie Atwood, CNN",
                    "title": "CIA director dispatched to Moscow to warn Russia over troop buildup near Ukraine",
                    "description": "President Joe Biden dispatched CIA Director Bill Burns to Moscow earlier this week to warn the Kremlin that the US is watching its buildup of troops near Ukraine's border closely, and to attempt to determine what is motivating Russia's actions.",
                    "url": "https://www.cnn.com/2021/11/05/politics/bill-burns-moscow-ukraine/index.html" 
                },
                "original":{
                    "author": "松本xxx",
                    "title": "CIA長官がモスクワに派遣され、ウクライナ近辺での軍備増強についてロシアに警告を発する",
                    "description": "ジョー・バイデン大統領は今週初め、ビル・バーンズCIA長官をモスクワに派遣し、ウクライナ国境付近での軍備増強を米国が注視していることをクレムリンに警告し、ロシアの行動の動機を探ろうとしました。",
                    "url": "https://www.cnn.com/2021/11/05/politics/bill-burns-moscow-ukraine/index.html"      
                }
​
            },
            {
​
​
            }
        
    ]
}
`