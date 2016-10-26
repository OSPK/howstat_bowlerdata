Scraped Bowler dismissal data from Howstats:

http://www.howstat.com.au/cricket/Statistics/Players/PlayerDismissBowlGraph.asp?PlayerID=0001

# To Start
    git clone https://github.com/OSPK/howstat_bowlerdata.git
    cd howstat_bowlerdata
    virtualenv -p python3 env
    . env/bin/activate
    pip install -r requirements.txt
    python scraper.py