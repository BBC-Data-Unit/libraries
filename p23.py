#!/usr/bin/env python

import scraperwiki
import requests
import urllib2
import lxml.etree
#This library is to count frequencies in a list
from collections import Counter

#URL lists and base URL at the bottom of scraper


#This takes a row of XML and splits out the value, the top and left attributes
def cleanrow(row):
    if '"' in row:
        top = row.split('top="')[1].split('"')[0]
    else:
        top = ""
    if '"' in row:
        left = row.split('left="')[1].split('"')[0]
    else:
        left = ""
    if '"' in row:
        figure = row.split('</text>')[0].split('">')[1].replace('<i>','').replace('</i>','')
    else:
        figure = ""
    all3 = [top, left, figure, row]
    return all3

#Define a new function called 'scrapepdf' with 1 parameters: 'pdfurl' 
def scrapepdf(pdfurl):
    #use the .urlopen function from urllib library (imported at the start of this scraper) to open 
    #and the .read method to read into new variable 'pdfdata'
    pdfdata = urllib2.urlopen(pdfurl).read()
    #convert to an XML object so we can scrape using lxml.etree
    xmldata = scraperwiki.pdftoxml(pdfdata)
    #these lines throw up an error:
    #ValueError: Unicode strings with encoding declaration are not supported. Please use bytes input or XML fragments without declaration.
    #root = lxml.etree.fromstring(xmldata)
    
    #PAGE 23
    #Split to grab the pages with volunteer data. This needs to be put in separate function
    volunteerspage = xmldata.split('B5: Volunteers')[1].split('SECTION C: WORKLOAD')[0]
    pagelines = volunteerspage.split('<text')
    print "NUMBER OF LINES", len(pagelines)
    linecount = -1
    '''
    for page in pagelines:
        linecount = linecount+1
        print linecount,': ', page
    '''
    print 'first300', volunteerspage[:300]
    print 'LAST 1000', volunteerspage[-2000:]
    avghrspervol = pagelines[-13]
    volunteerstable = pagelines[-17]
    volunteerhrs = pagelines[-9]
    print 'avghrspervol', avghrspervol
    print 'volunteerstable', volunteerstable
    print 'volunteerhrs', volunteerhrs
    #print 'THIS SHOULD SAY VOLUNTEERS', pagelines[1344]
    print 'THIS SHOULD SAY 2009-2010', pagelines[-52]
    print 'THIS SHOULD SAY 2009-2010', pagelines[-52].split("<")[0].split(">")[1]
    if pagelines[-52].split("<")[0].split(">")[1] == '2009-10':
        print "YES IT IS"
    else:
        print "NO IT ISN'T"
    tablerows = []
    tabletops = []
    tablelefts = []
    rowindex = -1
    print "RUNNING CLEANROW"
    '''
    for row in pagelines:
        rowindex = rowindex+1
        print "GRABBING", rowindex
        print row
        print rowindex, cleanrow(row)
        print "THENUM", rowindex, cleanrow(row)[0]
        print "IS THIS A NUM", cleanrow(row)[0].isdigit()
        if cleanrow(row)[0].isdigit():
            print "INTEGER", rowindex, int(cleanrow(row)[0])
            if int(cleanrow(row)[0]) > 850 and int(cleanrow(row)[0]) < 1000 and int(cleanrow(row)[1]) < 159:
                tablerows.append(row)
                tabletops.append(int(cleanrow(row)[0]))
                tablelefts.append(int(cleanrow(row)[1]))
    print "grabbed", len(tablerows), " rows"
    for row in tablerows:
        #left=81 in Barnsley on the years so grab those
        int(cleanrow(row)[1])
    print tablerows
    print tabletops
    #See https://stackoverflow.com/questions/3172173/most-efficient-way-to-calculate-frequency-of-values-in-a-python-list
    print(Counter(tabletops))
    print(Counter(tablelefts))
	#To find volunteers table on p23
    print "RUNNING VOLHISTORY"
    years = ['2009-10','2010-11','2011-12','2012-13','2013-14']
    #These are the indexes of years 2009-10, 2010-11 etc.
    yearsindexes = [1411, 1401, 1397, 1405, 1391]
    #These are the indexes of the averages for those years, should be same across all (data hygiene)
    volaverages = [1413, 1403, 1399, 1407, 1393]
    volnumbers = []
    avenumbers = []
    '''
    '''
    for pos in yearsindexes:
        volnumbers.append(pagelines[pos])
        #This cleans it up but doesn't go anywhere
        volsbyyear = cleanrow(pagelines[pos])
        print 'IS THIS THE NUM', volsbyyear[2]
        print 'TOP', volsbyyear[0]
        print 'LEFT', volsbyyear[1]
    for pos in volaverages:
        avenumbers.append(pagelines[pos])
        avevolsbyyear = cleanrow(pagelines[pos])
        print 'IS THIS THE AVE', avevolsbyyear[2]
        print 'TOP', avevolsbyyear[0]
        print 'LEFT', avevolsbyyear[1]
    volrecord = {}
    indexno = 0
    items = range(0,5)
    for item in items:
        indexno = indexno+1
        uniqueid = pdfurl+years[item]
        record['indexno'] = indexno
        record['year'] = years[item]
        record['volsbyyeartxt'] = volnumbers[item]
        record['avenumberstxt'] = avenumbers[item]
        record['volnumber'] = cleanrow(volnumbers[item])[2]
        record['volnumber_Yposition'] = cleanrow(volnumbers[item])[0]
        record['volnumber_LEFTposition'] = cleanrow(volnumbers[item])[1]
        record['avenumber'] = cleanrow(avenumbers[item])[2]
        record['avenumber_Yposition'] = cleanrow(avenumbers[item])[0]
        record['avenumber_LEFTposition'] = cleanrow(avenumbers[item])[1]
        record['pdfurl'] = pdfurl
        print record
        scraperwiki.sql.save(['uniqueid'],record)
    #convert into an lxml object
    '''

record = {}
pdfurl = 'http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles/barking%20and%20dagenham.pdf'

#scrapepdf('http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202013/bournemouth.pdf')


#The PDFs themselves are at these URLs
for201314 = 'http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/'
#Each list of PDF names has been scraped using Outwit

pdflist14 = ['bexley.pdf','bath-and-north-east-somerset.pdf','barking-and-dagenham.pdf','barnet.pdf','bedford.pdf','barnsley.pdf','bournemouth.pdf','bracknell-forest.pdf','brent.pdf','blackpool.pdf','blackburn-with-darwen.pdf','brighton-and-hove.pdf','bolton.pdf','bristol.pdf','bromley.pdf','bury.pdf','buckinghamshire.pdf','cheshire-east.pdf','cambridgeshire.pdf','calderdale.pdf','central-bedfordshire.pdf','cheshire-west-and-chester.pdf','camden.pdf','cornwall.pdf','coventry.pdf','croydon.pdf','darlington.pdf','cumbria.pdf','derby.pdf','devon.pdf','derbyshire.pdf','doncaster.pdf','durham.pdf','ealing.pdf','dudley.pdf','east-sussex.pdf','dorset.pdf','essex.pdf','gateshead.pdf','enfield.pdf','gloucestershire.pdf','greenwich.pdf','hammersmith-and-fulham.pdf','hackney.pdf','halton.pdf','hampshire.pdf','harrow.pdf','hartlepool.pdf','herefordshire.pdf','hillingdon.pdf','havering.pdf','hertfordshire.pdf','isle-of-wight.pdf','hounslow.pdf','islington.pdf','kent.pdf','kingston-upon-hull.pdf','kensington-and-chelsea.pdf','lambeth.pdf','lancashire.pdf','kingston-upon-thames.pdf','lewisham.pdf','leicester.pdf','lincolnshire.pdf','leeds.pdf','luton.pdf','leicestershire.pdf','medway.pdf','newcastle-upon-tyne.pdf','milton-keynes.pdf','merton.pdf','newham.pdf','northamptonshire.pdf','north-lincolnshire.pdf','north-somerset.pdf','north-east-lincolnshire.pdf','north-tyneside.pdf','northumberland.pdf','manchester.pdf','nottingham.pdf','north-yorkshire.pdf','nottinghamshire.pdf','oldham.pdf','oxfordshire.pdf','poole.pdf','portsmouth.pdf','redbridge.pdf','peterborough.pdf','plymouth.pdf','reading.pdf','richmond-upon-thames.pdf','redcar-and-cleveland.pdf','rochdale.pdf','salford.pdf','sandwell.pdf','sefton.pdf','sheffield.pdf','shropshire.pdf','somerset.pdf','slough.pdf','solihull.pdf','southampton.pdf','south-tyneside.pdf','southend-on-sea.pdf','south-gloucestershire.pdf','southwark.pdf','staffordshire.pdf','st-helens.pdf','stoke-on-trent.pdf','stockton-on-tees.pdf','stockport.pdf','sunderland.pdf','sutton.pdf','suffolk.pdf','surrey.pdf','swindon.pdf','torbay.pdf','tameside.pdf','tower-hamlets.pdf','telford-and-wrekin.pdf','thurrock.pdf','wandsworth.pdf','warrington.pdf','wakefield.pdf','walsall.pdf','waltham-forest.pdf','trafford.pdf','west-berkshire.pdf','westminster.pdf','warwickshire.pdf','wigan.pdf','west-sussex.pdf','wolverhampton.pdf','wiltshire.pdf','wirral.pdf','windsor-and-maidenhead.pdf','worcestershire.pdf','york.pdf']

testlist = ['http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles/city%20of%20london.pdf','http://www.cipfa.org/~/media/files/services/research and statistics/cipfastats library profiles/bath and north east somerset', 'http://www.cipfa.org/~/media/files/services/research and statistics/cipfastats library profiles/bedford']
testlist14 = [ 'http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/barnsley.pdf']
testbexley = ['http://www.cipfa.org/~/media/files/services/research%20and%20statistics/cipfastats%20library%20profiles%202014/bexley.pdf']
'''
for item in testbexley:
    print 'SCRAPING', item
    scrapepdf(item.replace(' ','%20'))
'''


for item in pdflist14:
    print 'SCRAPING', for201314+item
    scrapepdf(for201314+item)

