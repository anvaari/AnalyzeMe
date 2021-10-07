
# Analyze FireFox History
This is part of AnalyzeMe project and its aim is to analyze your Firefox history. In this version it create 2 plot and 1 CSV.
Plots:
- Sites with highest frecency (What is frecency? See [Read More](#Read\ More) section)
- Sites you visit most

CSV:
- Phrases you search in google. Also contain language of search (English, Persian or mixed), date of search and freauency of search.

## How does it work?
Firefox save your history in sqlite database. AnalyzeMe-Firefox get it as an input and make lot of plot and CSV from your browsing history :)
AnalyzeMe-Firefox also works fine with persian language.
Code is fully commented and you can learn more by reading source code.

## Usage
### Prerequisites
Install them using venv and pip :)
1. Clone the project
2. `cd path/to/AnalyzeMe/FireFox History`
3. Create a virtual environment : `python -m venv vevn`
4. Activate it : `source venv/bin/activate`
5. Update pip : `pip install --upgrade pip`
6. Install dependecies : `pip install -r requirements.txt`

### Analyzing 
`analyze.py ` uses `sqlite2csv.py` to convert sqlite tables to pandas.DataFrame. Both can use as an module or individually. Here I explaine usage in individual mode.

**analyze.py** : 
- see `python analyze.py -h` 
You can move your firefox history file (places.sqlite) in code path or you can specify path to that with `--db`.
Default output folder is code path but you can specify that with `--output`.
Example: 
```bash
python analyze.py --db ~/Data/places.sqlite --output ./output
```

**sqlite2csv.py** :
- see `python sqlite2.py -h`
It export places, history_visit and origin tables from places.sqlite as csv
You can move your firefox history file (places.sqlite) in code path or you can specify path to that with `--db`.
Default output folder is code path but you can specify that with `--output`.
Example: 
```bash
python sqlite2.py --db ~/Data/places.sqlite --output ./output
```



## Known issue
- I wanted to plot the sites information with their favicon on the top of their bar. But up to now I can't handle this using matplotlib. So the favicons show in messy way. **I will pay 2000 Satoshi for who fix this :)**
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement". Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (git checkout -b feature/AmazingFeature)
3. Commit your Changes (git commit -m 'Add some AmazingFeature')
4. Push to the Branch (git push origin feature/AmazingFeature)
5. Open a Pull Request

## Acknowledgments
I use many open source project in AnalyzeMe-Firefox, many of them are so popular and I appreciate for their great works. But I wanna mention some of them here :)
- [speech2text-Shenasa](https://github.com/shenasa-ai/speech2text) I use their clean text module to clean and refine perisan text.
- [favicon](https://github.com/scottwernervt/favicon) I use it to find favicons of sites.
- [serpextract](https://github.com/Parsely/serpextract) I use it to extract search phrases from url.
- [hazm](https://github.com/sobhe/hazm) I use their stopwords.dat file to detect stopwords.

## Read more
Some resources which helped me :
[Frecency in origins](https://developer.mozilla.org/en-US/docs/Mozilla/Tech/Places/Frecency_algorithm)
[Visit_Type in places](https://forensicswiki.xyz/wiki/index.php?title=Mozilla_Firefox_3_History_File_Format)
https://developer.mozilla.org/en-US/docs/Mozilla/Tech/Places/Database
https://wiki.mozilla.org/Browser_History


How to force matplotlib to save fig exact as it show : [here](https://kavigupta.org/2019/05/18/Setting-the-size-of-figures-in-matplotlib/)

